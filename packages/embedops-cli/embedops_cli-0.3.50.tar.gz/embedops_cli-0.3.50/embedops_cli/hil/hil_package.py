"""
The hil_package library includes functions for creating and extracting HIL execution packages.
These packages are ZIP-based and contain the build artifacts, HIL tests, and metadata for a
given HIL run.
"""
import os
import json
import shutil
import tempfile
from pathlib import Path
from embedops_cli.utilities import logging_setup, requests
from embedops_cli.hil.hil_extras import HILExtra

_logger = logging_setup(__name__)

# The fixed name of the HIL manifest file within the execution package
HIL_MANIFEST_NAME = "hil_manifest.json"

# The fixed name of the user's hil root folder within the execution package
HIL_ROOT_FOLDER_NAME = "hil"

# Marker file used to denote a directory that needs to be added to Python path
HIL_EXTERNAL_MODULE_MARKER_NAME = ".embedops.external_module"

# Passed to the shutil.make_archive tool
HIL_ARCHIVE_FORMAT = "zip"

# Regex that matches the HIL results folder names
HIL_RESULTS_FOLDER_NAME_PATTERN = (
    "hil_results_[0-9][0-9][0-9][0-9]_[0-9][0-9]_[0-9][0-9]"
    "_[0-9][0-9]H_[0-9][0-9]M_[0-9][0-9]S"
)


def create_hil_package(
    extras: list[HILExtra],
    hil_directory: str,
    manifest_data: dict,
    out_path: str,
) -> bool:
    """

    Build a HIL execution package archive. The inputs are copied to a temporary directory
    prior to zipping.

    :param extras: A list of extras to include in the package (files or directories)
    :param hil_directory: Path to the repository's hil root directory
    :param manifest_data: Dictionary of data that will be inserted into the package's
    manifest JSON file (eg, Git data)
    :param out_path: Full output path of the package, including the file name
    :return: True if success; False otherwise
    """

    with tempfile.TemporaryDirectory() as tmp_dir:
        _logger.debug(f"creating execution package")

        # Process additional items
        for extra in extras:

            dest = os.path.join(tmp_dir, extra.dest)

            if os.path.isdir(extra.source):

                # Intermediate directories will be created
                shutil.copytree(extra.source, dest)

            if os.path.isfile(extra.source):

                # To start, create the parent directory structure if it doesn't exist
                dest_parent = os.path.dirname(dest)
                os.makedirs(dest_parent, exist_ok=True)
                shutil.copyfile(extra.source, dest)

            # If this directory is a Python external modules path, create a marker file
            if extra.external_module:
                Path(os.path.join(dest, HIL_EXTERNAL_MODULE_MARKER_NAME)).touch()

        # Copy the entire hil root folder
        shutil.copytree(
            hil_directory,
            os.path.join(tmp_dir, HIL_ROOT_FOLDER_NAME),
            ignore=shutil.ignore_patterns(HIL_RESULTS_FOLDER_NAME_PATTERN),
        )

        # Write the manifest file
        with open(
            os.path.join(tmp_dir, HIL_MANIFEST_NAME), "w", encoding="utf-8"
        ) as m_file:
            json.dump(manifest_data, m_file, indent=4)

        # Create the actual archive file
        out_archive_path = os.path.splitext(out_path)[0]
        shutil.make_archive(out_archive_path, HIL_ARCHIVE_FORMAT, tmp_dir)

    # Only return success if the outfile exists
    if os.path.isfile(out_path):
        return True

    return False


def upload_hil_package(package_path: str, url: str) -> bool:
    """
    Upload a HIL package ZIP to the given S3 bucket pre-signed URL. This function assumes
    that the file exists.
    """
    _logger.debug(f"Starting upload of HIL package")

    headers = {
        "Content-Type": "application/zip",
        "x-amz-server-side-encryption": "AES256",
    }

    with open(package_path, "rb") as archive_file:
        data = archive_file.read()
        response = requests.put(
            url,
            headers=headers,
            data=data,
            timeout=60,
        )

        _logger.debug(f"HIL package upload response: {str(response)}\n")

    return response.status_code
