import argparse
import json
import logging
import os
import tempfile
import time
import zipfile
from dataclasses import asdict
from fnmatch import fnmatch
from typing import Tuple

from pypanther.vendor.panther_analysis_tool import cli_output
from pypanther.vendor.panther_analysis_tool.backend.client import (
    BackendError,
    BulkUploadMultipartError,
    BulkUploadParams,
)
from pypanther.vendor.panther_analysis_tool.backend.client import Client as BackendClient
from pypanther.vendor.panther_analysis_tool.backend.client import (
    FeatureFlagsParams,
    FeatureFlagWithDefault,
)
from pypanther.vendor.panther_analysis_tool.constants import ENABLE_CORRELATION_RULES_FLAG
from pypanther.vendor.panther_analysis_tool.util import convert_unicode

IGNORE_FOLDERS = [".mypy_cache", "pypanther", "panther_analysis", ".git", "__pycache__"]


def run(backend: BackendClient, args: argparse.Namespace) -> Tuple[int, str]:
    with tempfile.NamedTemporaryFile() as tmp:
        with zipfile.ZipFile(tmp, "w") as zip_out:
            logging.info(f"Writing to temporary zip file at {tmp.name}")

            for root, dir, files in os.walk("."):
                for bad in IGNORE_FOLDERS:
                    if bad in dir:
                        dir.remove(bad)

                for file in files:
                    if not fnmatch(file, "*.py"):
                        continue

                    filepath = os.path.join(root, file)

                    zip_out.write(
                        filepath,
                        arcname=filepath,
                    )
        return upload_zip(backend, args, archive=tmp.name)


def upload_zip(backend: BackendClient, args: argparse.Namespace, archive: str) -> Tuple[int, str]:
    # extract max retries we should handle
    max_retries = 10
    if args.max_retries > 10:
        logging.warning("max_retries cannot be greater than 10, defaulting to 10")
    elif args.max_retries < 0:
        logging.warning("max_retries cannot be negative, defaulting to 0")
        max_retries = 0

    with open(archive, "rb") as analysis_zip:
        logging.info("Uploading items to Panther")

        upload_params = BulkUploadParams(zip_bytes=analysis_zip.read())
        retry_count = 0

        while True:
            try:
                response = backend.async_bulk_upload(upload_params)

                resp_dict = asdict(response.data)
                flags_params = FeatureFlagsParams(
                    flags=[FeatureFlagWithDefault(flag=ENABLE_CORRELATION_RULES_FLAG)]
                )
                try:
                    if not backend.feature_flags(flags_params).data.flags[0].treatment:
                        del resp_dict["correlation_rules"]
                # pylint: disable=broad-except
                except BaseException:
                    del resp_dict["correlation_rules"]

                logging.info("API Response:\n%s", json.dumps(resp_dict, indent=4))
                return 0, cli_output.success("Upload succeeded")

            except BackendError as be_err:
                err = cli_output.multipart_error_msg(
                    BulkUploadMultipartError.from_jsons(convert_unicode(be_err)),
                    "Upload failed",
                )
                if be_err.permanent is True:
                    return 1, f"Failed to upload to Panther: {err}"

                if max_retries - retry_count > 0:
                    logging.debug("Failed to upload to Panther: %s.", err)
                    retry_count += 1

                    # typical bulk upload takes 30 seconds, allow any currently running one to complete
                    logging.debug(
                        "Will retry upload in 30 seconds. Retries remaining: %s",
                        max_retries - retry_count,
                    )
                    time.sleep(30)

                else:
                    logging.warning("Exhausted retries attempting to perform bulk upload.")
                    return 1, f"Failed to upload to Panther: {err}"

            # PEP8 guide states it is OK to catch BaseException if you log it.
            except BaseException as err:  # pylint: disable=broad-except
                return 1, f"Failed to upload to Panther: {err}"
