from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado


class RouteHandler(APIHandler):
    # Route handler for the /skillsnetwork_jupyter_extension/config endpoint.
    # A single endpoint that returns various URLs.
    
    @property
    def config(self):
        return self.settings["sn_config"]
    
    @tornado.web.authenticated
    def get(self):
        self.finish({
            "ATLAS_BASE_URL": self.config.atlas_base_url,
            "SN_FILE_LIBRARY_URL": self.config.sn_file_library_url,
            "SN_V2_FILE_LIBRARY_URL": self.config.sn_v2_file_library_url,
            "AWB_BASE_URL": self.config.awb_base_url
        })


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]

    # Prepend the base_url so that it works in a JupyterHub setting
    url_path = 'skillsnetwork_jupyter_extension'
    handler_url_path = url_path_join(base_url, url_path, 'config')
    handlers = [(handler_url_path, RouteHandler)]
    web_app.add_handlers(host_pattern, handlers)
