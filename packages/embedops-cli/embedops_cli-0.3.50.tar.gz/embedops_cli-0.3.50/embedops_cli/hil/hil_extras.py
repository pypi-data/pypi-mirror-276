"""Functions to support HIL extras feature"""
import os
from dynaconf import Dynaconf
from dynaconf.utils.boxing import DynaBox
from embedops_cli.hil.hil_types import (
    HILExtrasException,
)

# YAML key names
CI_SOURCE_KEY = "ci_source"
EXTERNAL_MODULE_KEY = "external_module"


class HILExtra:

    """Represents a single HIL extra item"""

    def __init__(self, source: str, dest: str, external_module: bool):

        """Create an extra instance"""
        self.source = source
        self.dest = dest
        self.external_module = external_module


def hil_get_extras(hil_config_path: str, local: bool) -> list[HILExtra]:

    """
    Main function for retrieving additional items spec from
    HIL YAML config. Returns a list of additional items used
    for creating the HIL execution package.
    """

    hil_extras = _get_hil_extras(hil_config_path)
    hil_artifacts = _get_hil_artifacts(hil_config_path)

    # Disallow both being specified at the same time
    if hil_artifacts is not None and hil_extras is not None:
        raise HILExtrasException(
            (
                "hil_artifacts and hil_extras cannot be defined"
                " at the same time. It is recommended to use hil_extras instead."
            )
        )

    # If neither is present, return an empty list
    if hil_artifacts is None and hil_extras is None:
        return []

    # hil_extras was specified
    if hil_extras is not None:

        extras = []

        for extra in hil_extras:

            # Simple string item that has no attributes
            if isinstance(extra, str):
                src = extra
                dst = extra
                external_module = False
            # Complex item with attributes
            elif isinstance(extra, DynaBox):
                src = list(extra.keys())[0]
                dst = src
                attrs = extra[src]

                # Use the CI path if non-local and provided
                if CI_SOURCE_KEY in attrs and local is False:
                    src = attrs[CI_SOURCE_KEY]

                external_module = attrs.get(EXTERNAL_MODULE_KEY, False)

            else:
                # Unrecognized type
                raise HILExtrasException(f"Extra {extra} has an invalid YAML format.")

            # First, ensure src exists
            if not os.path.isfile(src) and not os.path.isdir(src):
                raise HILExtrasException(f"Extra {src} does not exist.")

            if not os.path.isdir(src) and external_module:
                raise HILExtrasException(
                    f"Extra {extra} has external_module set, but is not a directory."
                )

            extras.append(HILExtra(src, dst, external_module))

        return extras

    # hil_artifacts was specified
    artifacts_extra = _get_artifacts_extra(hil_artifacts, local)
    return [artifacts_extra]


def _get_artifacts_extra(artifacts, local):

    # Maintain backwards compatibility with hil_artifacts in the YAML
    dst = os.path.join("artifacts", os.path.basename(artifacts))

    artifacts_extra = HILExtra(artifacts, dst, False)

    # Perform CI conversion to source, if necessary
    if local is False:
        artifacts_dir = os.path.join(os.getcwd(), "artifacts")
        file_name = os.path.basename(artifacts_extra.source)

        for root, _, files in os.walk(artifacts_dir):
            if file_name in files:
                absolute_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(absolute_path)
                artifacts_extra.source = relative_path

    # Make sure the artifact exists
    if not os.path.isfile(artifacts_extra.source):
        raise HILExtrasException(f"Artifact {artifacts_extra.source} does not exist.")

    return artifacts_extra


def _get_hil_extras(hil_config_path):
    """get hil_extras from .embedops/hil/config.yml

    Returns:
        str: the value stored in <repo_root>/.embedops/hil/config.yml:hil_extras or None
    """
    dot_eo = Dynaconf(
        load_dotenv=False,
        settings_files=[hil_config_path],
        silent_errors=True,
    )
    dot_eo.configure(
        LOADERS_FOR_DYNACONF=[
            "dynaconf.loaders.yaml_loader",
        ]
    )
    return dot_eo.get("hil_extras")


def _get_hil_artifacts(hil_config_path):
    """get hil_artifacts from .embedops/hil/config.yml

    Returns:
        str: the value stored in <repo_root>/.embedops/hil/config.yml:hil_artifacts or None
    """
    dot_eo = Dynaconf(
        load_dotenv=False,
        settings_files=[hil_config_path],
        silent_errors=True,
    )
    dot_eo.configure(
        LOADERS_FOR_DYNACONF=[
            "dynaconf.loaders.yaml_loader",
        ]
    )
    return dot_eo.get("hil_artifacts")
