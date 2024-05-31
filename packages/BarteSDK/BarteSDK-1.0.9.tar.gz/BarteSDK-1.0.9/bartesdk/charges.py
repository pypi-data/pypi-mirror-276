from .base import BaseAPI

class chargesAPI(BaseAPI):
    def __init__(self, api_key, env="prd", api_version="v1"):
        path = "charges"
        super().__init__(api_key, env, api_version, path)