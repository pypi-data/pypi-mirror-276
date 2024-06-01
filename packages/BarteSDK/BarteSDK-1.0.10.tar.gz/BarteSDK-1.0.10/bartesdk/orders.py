from .base import BaseAPI

class ordersAPI(BaseAPI):
    def __init__(self, api_key, env="prd", api_version="v1"):
        path = "orders"
        super().__init__(api_key, env, api_version, path)