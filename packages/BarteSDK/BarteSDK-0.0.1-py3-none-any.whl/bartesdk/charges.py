import requests

class chargesAPI:
    def __init__(self, api_key, env="prd", api_version="v2"):
        self.api_key = api_key
        self.base_url = self._get_base_url(env, api_version)

    def _get_base_url(self, env, api_version):
        if env == "prd":
            return f'https://api.barte.com/{api_version}/charges'
        elif env == "sandbox":
            return f'https://sandbox-api.barte.com/{api_version}/charges'
        else:
            raise ValueError("Invalid environment specified")

    def getByUuid(self, uuid):
        headers = {
            'X-Token-Api': self.api_key
        }
        url = f"{self.base_url}/{uuid}"
        response = requests.get(url, headers=headers)
        return response.json()

    def get(self, **params):
        headers = {
            'X-Token-Api': self.api_key
        }
        response = requests.get(self.base_url, headers=headers, params=params)
        return response.json()

    def refund(self, uuid, as_fraud=True):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json',
            'accept': '*/*'
        }
        url = f"{self.base_url}/{uuid}/refund"
        payload = {
            'asFraud': as_fraud
        }
        response = requests.patch(url, headers=headers, json=payload)
        return response.status_code, response.ok

    def cancel(self, uuid):
        headers = {
            'X-Token-Api': self.api_key,
            'accept': '*/*'
        }
        url = f"{self.base_url}/{uuid}"
        response = requests.delete(url, headers=headers)
        return response.status_code, response.ok