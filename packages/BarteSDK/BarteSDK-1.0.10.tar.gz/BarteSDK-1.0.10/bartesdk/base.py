import requests

class BaseAPI:
    def __init__(self, api_key, env, api_version, path):
        self.api_key = api_key
        self.base_url = self._get_base_url(env, api_version, path)


    def _get_base_url(self, env, api_version, path):
        if env == "prd":
            return f'https://api.barte.com/{api_version}/{path}'
        elif env == "sandbox":
            return f'https://sandbox-api.barte.com/{api_version}/{path}'
        else:
            raise ValueError("Invalid environment specified")


    # Generic Funcion      


    def create(self, **kwargs):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }
        payload = kwargs
        response = requests.post(self.base_url, headers=headers, json=payload)
        return response.status_code, response.json() if response.ok else response.text


    def get(self, **params):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }
        response = requests.get(self.base_url, headers=headers, params=params)
        return response.json()


    def getByUuid(self, uuid):
        headers = {
            'X-Token-Api': self.api_key
        }
        url = f"{self.base_url}/{uuid}"
        response = requests.get(url, headers=headers)
        return response.json()


    def update(self, uuid, **kwargs):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json',
            'accept': '*/*'
        }
        url = f"{self.base_url}/{uuid}"
        payload = kwargs
        response = requests.put(url, headers=headers, json=payload)
        try:
            response_data = response.json() if response.ok else response.text
        except ValueError:
            response_data = response.text
        return response.status_code, response_data


    def cancel(self, uuid):
        headers = {
            'X-Token-Api': self.api_key,
            'accept': '*/*'
        }
        url = f"{self.base_url}/{uuid}"
        response = requests.delete(url, headers=headers)
        return response.status_code, response.json() if response.ok else response.text


    # Non Generic Function
    
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


    def calculateInstallments(self, **kwargs):
        headers = {
            'X-Token-Api': self.api_key,
            'accept': '*/*'
        }
        response = requests.get(self.base_url, headers=headers, params=kwargs)
        try:
            response_data = response.json() if response.ok else response.text
        except ValueError:
            response_data = response.text
        return response.status_code, response_data


    def maxInstallments(self):
        headers = {
            'X-Token-Api': self.api_key,
            'accept': '*/*',
            'Content-Type': 'application/json'
        }
        url = f"{self.base_url}/max-installments"
        response = requests.get(url, headers=headers)
        return response.status_code, response.json() if response.ok else response.text


    def installmentsPayment(self, **kwargs):
        headers = {
            'X-Token-Api': self.api_key,
            'accept': '*/*',
            'Content-Type': 'application/json'
        }
        url = f"{self.base_url}/installments-payment"
        response = requests.get(url, headers=headers, params=kwargs)
        try:
            response_data = response.json() if response.ok else response.text
        except ValueError:
            response_data = response.text
        return response.status_code, response_data


    def updateBasicValue(self, subscription_id, **kwargs):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json',
            'accept': '*/*'
        }
        url = f"{self.base_url}/{subscription_id}/basic-value"
        response = requests.patch(url, headers=headers, json=kwargs)
        try:
            response_data = response.json() if response.ok else response.text
        except ValueError:
            response_data = response.text
        return response.status_code, response_data
