import requests

class ordersAPI:
    def __init__(self, api_key, env="prd", api_version="v2"):
        self.api_key = api_key
        self.base_url = self._get_base_url(env, api_version)

    def _get_base_url(self, env, api_version):
        if env == "prd":
            return f'https://api.barte.com/{api_version}/orders'
        elif env == "sandbox":
            return f'https://sandbox-api.barte.com/{api_version}/orders'
        else:
            raise ValueError("Invalid environment specified")

    def create(self, start_date, value, installments, title, description, payment, uuid_buyer, idempotency_key):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json',
            'x-idempotency-key': idempotency_key,
            'accept': '*/*'
        }
        payload = {
            "startDate": start_date,
            "value": value,
            "installments": installments,
            "title": title,
            "description": description,
            "payment": payment,
            "uuidBuyer": uuid_buyer
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        return response.status_code, response.json() if response.ok else response.text

    def get(self, **params):
        headers = {
            'X-Token-Api': self.api_key
        }
        response = requests.get(self.base_url, headers=headers, params=params)
        return response.json()

    def update(self, uuid, metadata, description):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json',
            'accept': '*/*'
        }
        payload = {
            "metadata": metadata,
            "description": description
        }
        url = f"{self.base_url}/{uuid}/basic-value"
        response = requests.patch(url, headers=headers, json=payload)
        return response.status_code, response.json() if response.ok else response.text

    def getByUuid(self, uuid):
        headers = {
            'X-Token-Api': self.api_key,
            'accept': 'application/json'
        }
        url = f"{self.base_url}/{uuid}"
        response = requests.get(url, headers=headers)
        return response.status_code, response.json() if response.ok else response.text

    def cancel(self, uuid):
        headers = {
            'X-Token-Api': self.api_key,
            'accept': '*/*'
        }
        url = f"{self.base_url}/{uuid}"
        response = requests.delete(url, headers=headers)
        return response.status_code, response.json() if response.ok else response.text

    def calculateInstallments(self, amount, max_installments):
        headers = {
            'X-Token-Api': self.api_key,
            'accept': '*/*'
        }
        params = {
            'amount': amount,
            'maxInstallments': max_installments
        }
        response = requests.get(self.base_url, headers=headers, params=params)
        return response.status_code, response.json() if response.ok else response.text