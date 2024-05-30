import requests

class paymentlinksAPI:
    def __init__(self, api_key, env="prd", api_version="v2"):
        self.api_key = api_key
        self.base_url = self._get_base_url(env, api_version)

    def _get_base_url(self, env, api_version):
        if env == "prd":
            return f'https://api.barte.com/{api_version}/payment-links'
        elif env == "sandbox":
            return f'https://sandbox-api.barte.com/{api_version}/payment-links'
        else:
            raise ValueError("Invalid environment specified")

    def getByUuid(self, uuid):
        headers = {
            'X-Token-Api': self.api_key,
            'accept': 'application/json'
        }
        url = f"{self.base_url}/{uuid}"
        response = requests.get(url, headers=headers)
        return response.status_code, response.json() if response.ok else response.text

    def update(self, uuid, payload):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json',
            'accept': '*/*'
        }
        url = f"{self.base_url}/{uuid}"
        response = requests.put(url, headers=headers, json=payload)
        return response.status_code, response.ok

    def cancel(self, uuid):
        headers = {
            'X-Token-Api': self.api_key,
            'accept': '*/*'
        }
        url = f"{self.base_url}/{uuid}"
        response = requests.delete(url, headers=headers)
        return response.status_code, response.ok

    def get(self, **params):
        headers = {
            'X-Token-Api': self.api_key,
            'accept': '*/*'
        }
        response = requests.get(self.base_url, headers=headers, params=params)
        return response.status_code, response.json() if response.ok else response.text

    def create(self, payload):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json',
            'accept': '*/*'
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        return response.status_code, response.json() if response.ok else response.text

    def maxInstallments(self):
        headers = {
            'X-Token-Api': self.api_key,
            'accept': '*/*',
            'Content-Type': 'application/json'
        }
        url = f"{self.base_url}/max-installments"
        response = requests.get(url, headers=headers)
        return response.status_code, response.json() if response.ok else response.text

    def installmentsPayment(self, amount, max_installments):
        headers = {
            'X-Token-Api': self.api_key,
            'accept': '*/*',
            'Content-Type': 'application/json'
        }
        params = {
            'amount': amount,
            'maxInstallments': max_installments
        }
        url = f"{self.base_url}/installments-payment"
        response = requests.get(url, headers=headers, params=params)
        return response.status_code, response.json() if response.ok else response.text