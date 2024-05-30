import os
import pytest
import shutil
from pathlib import Path
from embedops_cli.hil.hil_extras import HILExtra, hil_get_extras
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


#
# Tests specifically around the hil_extras YAML key 
# 

def test_yaml_no_extras():

    """Test that no hil_extras key gives an empty list"""

    extras = hil_get_extras("tests/hil_config_yaml/hil_extras_no_extras.yml", True)
    assert extras == []

def test_file_not_exist():

    """Test that a non-existent file gives an error"""

    with pytest.raises(HILExtrasException):
        extras, artifact = hil_get_extras("tests/hil_config_yaml/hil_extras_file_not_exist.yml", True)

def test_ci_file_not_exist():

    """Test that a non-existent file with separate CI source gives an error"""

    with pytest.raises(HILExtrasException) as exc_info:
        extras, _ = hil_get_extras("tests/hil_config_yaml/hil_extras_ci_file_not_exist.yml", False)

    assert "does not exist" in exc_info.value.fix_message

def test_dir_not_exist():

    """Test that a non-existent directory gives an error"""

    with pytest.raises(HILExtrasException) as exc_info:
        extras, _ = hil_get_extras("tests/hil_config_yaml/hil_extras_dir_not_exist.yml", True)

    assert "does not exist" in exc_info.value.fix_message

def test_file_has_external_module():

    """Test that a file with external_module set to True gives an error"""

    with pytest.raises(HILExtrasException) as exc_info:
        extras, _ = hil_get_extras("tests/hil_config_yaml/hil_extras_file_has_external_module.yml", True)

    assert "has external_module set" in exc_info.value.fix_message

def test_valid_local():

    """Test a valid YAML in local mode"""

    extras = hil_get_extras("tests/hil_config_yaml/hil_extras_valid.yml", True)

    assert extras[0].source == "file_at_root.hex"
    assert extras[0].external_module == False

    assert extras[1].source == "dir_at_root"
    assert extras[1].external_module == False

    assert extras[2].source == "ci_file_at_root.hex"
    assert extras[2].external_module == False

    assert extras[3].source == "ci/folder"
    assert extras[3].external_module == False

    assert extras[4].source == "python/module"
    assert extras[4].external_module == True

    assert extras[5].source == "ci_python/module"
    assert extras[5].external_module == True

    # Assert each extra had the dest equal to the source, since this is local mode
    for e in extras:
        assert e.source == e.dest


def test_valid_ci():

    """Test a valid YAML in CI mode"""

    extras = hil_get_extras("tests/hil_config_yaml/hil_extras_valid.yml", False)
   
    assert extras[0].source == "file_at_root.hex"
    assert extras[0].dest   == "file_at_root.hex"
    assert extras[0].external_module == False

    assert extras[1].source == "dir_at_root"
    assert extras[1].dest   == "dir_at_root"
    assert extras[1].external_module == False

    assert extras[2].source == "artifacts/ci_file_at_root.hex"
    assert extras[2].dest   == "ci_file_at_root.hex"
    assert extras[2].external_module == False

    assert extras[3].source == "artifacts/ci/folder"
    assert extras[3].dest   == "ci/folder"
    assert extras[3].external_module == False

    assert extras[4].source == "python/module"
    assert extras[4].dest   == "python/module"
    assert extras[4].external_module == True

    assert extras[5].source == "artifacts/ci_python/module"
    assert extras[5].dest   == "ci_python/module"
    assert extras[5].external_module == True


#
# Test specifically around the hil_artifacts legacy YAML key
#

def test_artifacts_local():

    """Test that an artifact is retrieved correctly in local mode"""

    extras = hil_get_extras("tests/hil_config_yaml/hil_extras_artifacts_at_root.yml", True)
   
    assert len(extras) == 1
    assert extras[0].source == "ci_file_at_root.hex"
    assert extras[0].dest   == "artifacts/ci_file_at_root.hex"
    assert extras[0].external_module == False


def test_artifacts_ci_at_root():

    """Test that an artifact is retrieved correctly in CI mode
    when artifacts is at artifacts/"""

    extras = hil_get_extras("tests/hil_config_yaml/hil_extras_artifacts_at_root.yml", False)
    
    assert len(extras) == 1
    assert extras[0].source == "artifacts/ci_file_at_root.hex"
    assert extras[0].dest   == "artifacts/ci_file_at_root.hex"
    assert extras[0].external_module == False


def test_artifacts_ci_nested():

    """Test that an artifact is retrieved correctly in CI mode
    when artifact is nested inside artifacts/"""

    extras = hil_get_extras("tests/hil_config_yaml/hil_extras_artifacts_nested.yml", False)
    
    assert len(extras) == 1
    assert extras[0].source == "artifacts/can/you/find/me/file_at_root.hex"
    assert extras[0].dest   == "artifacts/file_at_root.hex"
    assert extras[0].external_module == False


#
# A single test when both are present (invalid)
#

def test_both_extras_artifacts():

    """Test that having both keys throws an error"""
    
    with pytest.raises(HILExtrasException) as exc_info:
        extras, artifact = hil_get_extras("tests/hil_config_yaml/hil_both_extras_artifacts.yml", True)

    assert "hil_artifacts and hil_extras cannot be defined at the same time" in exc_info.value.fix_message

