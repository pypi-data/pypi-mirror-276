import requests

class buyersAPI:
    def __init__(self, api_key, env="prd", api_version="v2"):
        self.api_key = api_key
        self.base_url = self._get_base_url(env, api_version)

    def _get_base_url(self, env, api_version):
        if env == "prd":
            return f'https://api.barte.com/{api_version}/buyers'
        elif env == "sandbox":
            return f'https://sandbox-api.barte.com/{api_version}/buyers'
        else:
            raise ValueError("Invalid environment specified")

    def create(self, document, name, email, phone, country_code=None, alternative_email=None, address=None):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }
        payload = {
            'document': document,
            'name': name,
            'email': email,
            'phone': phone,
        }
        if country_code:
            payload['countryCode'] = country_code
        if alternative_email:
            payload['alternativeEmail'] = alternative_email
        if address:
            payload['address'] = address

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

    def update(self, uuid, name, email, countryCode, phone, alternativeEmail):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json',
            'accept': '*/*'
        }
        url = f"{self.base_url}/{uuid}"
        payload = {
            'name': name,
            'email': email,
            'countryCode': countryCode,
            'phone': phone,
            'alternativeEmail': alternativeEmail
        }
        response = requests.put(url, headers=headers, json=payload)
        return response.status_code, response.ok
