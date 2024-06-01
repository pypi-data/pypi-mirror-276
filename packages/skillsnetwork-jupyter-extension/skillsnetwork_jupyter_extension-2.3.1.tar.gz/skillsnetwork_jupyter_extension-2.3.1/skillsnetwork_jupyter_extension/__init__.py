try:
    from ._version import __version__
except ImportError:
    # Fallback when using the package in dev mode without installing
    # in editable mode with pip. It is highly recommended to install
    # the package from a stable release or in editable mode: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
    import warnings
    warnings.warn("Importing 'skillsnetwork_jupyter_extension' outside a proper installation.")
    __version__ = "dev"
from .handlers import setup_handlers

import os

from traitlets import Unicode
from traitlets.config import Configurable


def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": "skillsnetwork_jupyter_extension"
    }]


def _jupyter_server_extension_points():
    return [{
        "module": "skillsnetwork_jupyter_extension"
    }]


class SkillsNetworkAuthoringExtension(Configurable):
  """
  Configuration options for skillsnetwork_jupyter_extension
  """
  atlas_base_url = Unicode(
        default_value=os.environ.get("ATLAS_BASE_URL", "https://author.skills.network/atlas"),
        config=True,
        help="The base URL for the lab file version management service (AKA Atlas)"
  )
  sn_file_library_url = Unicode(
        default_value=os.environ.get("SN_FILE_LIBRARY_URL", "https://author-ide.skills.network/file-library"),
        config=True,
        help="The URL for the sn-file-library ui"
  )
  sn_v2_file_library_url = Unicode(
        default_value=os.environ.get("SN_V2_FILE_LIBRARY_URL", "https://author-files.skills.network"),
        config=True,
        help="The URL for the sn-file-library-v2 ui"
  )
  awb_base_url = Unicode(
        default_value=os.environ.get("AWB_BASE_URL", "https://author.skills.network"),
        config=True,
        help="The URL for Author Workbench"
  )


def _load_jupyter_server_extension(server_app):
    """Registers the API handler to receive HTTP requests from the frontend extension.

    Parameters
    ----------
    server_app: jupyterlab.labapp.LabApp
        JupyterLab application instance
    """
    sn_config = SkillsNetworkAuthoringExtension(config=server_app.config)
    server_app.web_app.settings["sn_config"] = sn_config

    setup_handlers(server_app.web_app)
    name = "skillsnetwork_jupyter_extension"
    server_app.log.info(f"Registered {name} server extension")
