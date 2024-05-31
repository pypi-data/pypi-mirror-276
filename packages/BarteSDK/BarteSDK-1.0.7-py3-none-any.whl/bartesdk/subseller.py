from .base import BaseAPI

class subsellerAPI(BaseAPI):
    def __init__(self, api_key, env="prd", api_version="v1"):
        base_url = self._get_base_url(env, api_version)
        super().__init__(api_key, base_url)

    def _get_base_url(self, env, api_version):
        if env == "prd":
            return f'https://api.barte.com/{api_version}/seller/subseller'
        elif env == "sandbox":
            return f'https://sandbox-api.barte.com/{api_version}/seller/subseller'
        else:
            raise ValueError("Invalid environment specified")