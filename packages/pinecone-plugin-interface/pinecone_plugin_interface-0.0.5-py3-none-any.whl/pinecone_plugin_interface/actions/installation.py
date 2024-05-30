from typing import List
from ..plugin_metadata import PluginMetadata
from ..logging import logger

def install_plugins(target, plugins: List[PluginMetadata], plugin_client_builder):
    for plugin in plugins:
        if not isinstance(plugin, PluginMetadata):
            raise Exception("object must be an instance of PluginMetadata")
        try:
            logger.info(f"Installing plugin {plugin.namespace} into {target.__class__.__name__}")
            
            openapi_api_class = plugin.openapi_api_class
            openapi_ApiClient = plugin.openapi_api_client_class
            if openapi_api_class is None:
                openapi_client = None
            else:
                api_version = plugin.api_version
                if openapi_ApiClient is None:
                    raise Exception("invalid plugin: openapi_api_client_class must be provided if openapi_client_class is provided")
                openapi_client = plugin_client_builder(openapi_ApiClient, openapi_api_class, api_version)
            
            impl = plugin.implementation_class
            setattr(target, plugin.namespace, impl(target.config, openapi_client))
        except Exception as e:
            # We want to display some troubleshooting information but not interrupt
            # execution of the main program in a way that would prevent non-plugin
            # related functionality from working when a broken plugin is present.
            logger.exception(f"Error while installing plugin {plugin.namespace}: {e}")
            continue