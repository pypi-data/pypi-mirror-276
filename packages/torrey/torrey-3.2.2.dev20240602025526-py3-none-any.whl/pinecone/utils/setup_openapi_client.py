from .user_agent import get_user_agent
from config import ConfigBuilder

def setup_openapi_client(api_client_klass, api_klass, config, openapi_config, pool_threads, api_version=None, master_config=None):
    # It is important that we allow the user to pass in a reference to api_client_klass
    # instead of creating a direct dependency on ApiClient because plugins have their
    # own ApiClient implementations. Even if those implementations seem like they should
    # be functionally identical, they are not the same class and have references to 
    # different copies of the ModelNormal class. Therefore cannot be used interchangeably.
    # without breaking the generated client code anywhere it is relying on isinstance to make
    # a decision about something.

    if master_config:
        openapi_config = ConfigBuilder.build_openapi_config(master_config, openapi_config=openapi_config)

    api_client = api_client_klass(
        configuration=openapi_config, 
        pool_threads=pool_threads
    )
    api_client.user_agent = get_user_agent(config)
    extra_headers = config.additional_headers or {}
    for key, value in extra_headers.items():
        api_client.set_default_header(key, value)
    
    for key, value in master_config.items():
        api_client.set_default_header(key, value)

    if api_version:
        api_client.set_default_header("X-Pinecone-API-Version", api_version)
    client = api_klass(api_client)
    return client

def build_plugin_setup_client(config, openapi_config, pool_threads):
    def setup_plugin_client(api_client_klass, api_klass, api_version, master_config=None):
        return setup_openapi_client(api_client_klass, api_klass, config, openapi_config, pool_threads, api_version, master_config)
    return setup_plugin_client
