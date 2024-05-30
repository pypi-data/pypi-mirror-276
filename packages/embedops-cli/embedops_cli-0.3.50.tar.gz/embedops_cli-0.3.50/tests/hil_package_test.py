import os
import pytest
import shutil
import zipfile
from pathlib import Path
from embedops_cli.hil.hil_extras import HILExtra, hil_get_extras
from embedops_cli.hil.hil_package import create_hil_package
from embedops_cli.hil.hil_types import (
    HILExtrasException,
)


@pytest.fixture(autouse=True)
def temp_directory_fixture():

    """
    cd into our test directory and then cd back out
    """

    current_dir = os.getcwd()
    os.chdir("tests/file_fixtures/fake_repo_extras")

    yield

    os.chdir(current_dir)


def test_package_extras_local():

    extras = hil_get_extras("tests/hil_config_yaml/hil_package_test.yml", True) 
    out_file = "package_out.zip"

    assert create_hil_package(extras, "hil", {}, out_file) == True

    extracted_dir = "package_extracted"
    shutil.unpack_archive(out_file, extracted_dir)

    # Test that the proper files/folders made it into the package
    assert os.path.isdir(extracted_dir)
    assert os.path.isfile(os.path.join(extracted_dir, "ci_file_at_root.hex"))
    assert os.path.isdir(os.path.join(extracted_dir, "ci_dir_at_root"))
    assert os.path.isfile(os.path.join(extracted_dir, "file/in/folder.hex"))
    assert os.path.isdir(os.path.join(extracted_dir, "dir/in/folder"))
    assert os.path.isfile(os.path.join(extracted_dir, "python/module/.embedops.external_module"))

    # Delete archive
    Path(out_file).unlink()
    shutil.rmtree(extracted_dir)


def test_package_extras_ci():

    extras = hil_get_extras("tests/hil_config_yaml/hil_package_test.yml", False)
    print(f"{extras[0].source} {extras[0].dest}")
    out_file = "package_out.zip"

    assert create_hil_package(extras, "hil", {}, out_file) == True

    extracted_dir = "package_extracted"
    shutil.unpack_archive(out_file, extracted_dir)

    # Test that the proper files/folders made it into the package
    assert os.path.isdir(extracted_dir)
    assert os.path.isfile(os.path.join(extracted_dir, "ci_file_at_root.hex"))
    assert os.path.isdir(os.path.join(extracted_dir, "ci_dir_at_root"))
    assert os.path.isfile(os.path.join(extracted_dir, "file/in/folder.hex"))
    assert os.path.isdir(os.path.join(extracted_dir, "dir/in/folder"))
    assert os.path.isfile(os.path.join(extracted_dir, "python/module/.embedops.external_module"))

    # Delete archive
    Path(out_file).unlink()
    shutil.rmtree(extracted_dir)


def test_package_extras_artifacts_local():

    extras = hil_get_extras("tests/hil_config_yaml/hil_package_test_artifacts.yml", True)
    print(f"{extras[0].source} {extras[0].dest}")
    out_file = "package_out.zip"

    assert create_hil_package(extras, "hil", {}, out_file) == True

    extracted_dir = "package_extracted"
    shutil.unpack_archive(out_file, extracted_dir)

    # Test that the proper files/folders made it into the package
    assert os.path.isdir(extracted_dir)
    assert os.path.isfile(os.path.join(extracted_dir, "artifacts", "file_at_root.hex"))

    # Delete archive
    Path(out_file).unlink()
    shutil.rmtree(extracted_dir)


def test_package_extras_artifacts_ci():

    extras = hil_get_extras("tests/hil_config_yaml/hil_package_test_artifacts.yml", False)
    print(f"{extras[0].source} {extras[0].dest}")
    out_file = "package_out.zip"

    assert create_hil_package(extras, "hil", {}, out_file) == True

    extracted_dir = "package_extracted"
    shutil.unpack_archive(out_file, extracted_dir)

    # Test that the proper files/folders made it into the package
    assert os.path.isdir(extracted_dir)
    assert os.path.isfile(os.path.join(extracted_dir, "artifacts", "file_at_root.hex"))

    # Delete archive
    Path(out_file).unlink()
    shutil.rmtree(extracted_dir)