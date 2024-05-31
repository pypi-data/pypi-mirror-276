from .base import BaseAPI

class paymentlinksAPI(BaseAPI):
    def __init__(self, api_key, env="prd", api_version="v1"):
        path = "payment-links"
        super().__init__(api_key, env, api_version, path)