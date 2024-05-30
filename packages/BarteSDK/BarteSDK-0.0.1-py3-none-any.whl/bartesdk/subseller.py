import requests

class subsellerAPI:
    def __init__(self, api_key, env="prd", api_version="v2"):
        self.api_key = api_key
        self.base_url = self._get_base_url(env, api_version)

    def _get_base_url(self, env, api_version):
        if env == "prd":
            return f'https://api.barte.com/{api_version}/seller/subseller'
        elif env == "sandbox":
            return f'https://sandbox-api.barte.com/{api_version}/seller/subseller'
        else:
            raise ValueError("Invalid environment specified")

    def getByID(self, id):
        headers = {
            'X-Token-Api': self.api_key,
            'accept': '*/*'
        }
        url = f"{self.base_url}/{id}"
        response = requests.get(url, headers=headers)
        return response.status_code, response.json() if response.ok else response.text

    def update(self, subseller_id, name, document_type, document, alternative_email, owner_name, owner_document, birthdate, opening_date, payment_type, payment_value, description):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json',
            'accept': '*/*'
        }
        payload = {
            "name": name,
            "documentType": document_type,
            "document": document,
            "alternativeEmail": alternative_email,
            "ownerName": owner_name,
            "ownerDocument": owner_document,
            "birthdate": birthdate,
            "openingDate": opening_date,
            "paymentType": payment_type,
            "paymentValue": payment_value,
            "description": description
        }
        url = f"{self.base_url}/{subseller_id}"
        response = requests.patch(url, headers=headers, json=payload)
        return response.status_code, response.json() if response.ok else response.text

    def create(self, name, document_type, document, phone, alternative_email, address, account, contact, payment_type, payment_value, description):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json',
            'accept': '*/*'
        }
        payload = {
            "name": name,
            "documentType": document_type,
            "document": document,
            "phone": phone,
            "alternativeEmail": alternative_email,
            "address": address,
            "account": account,
            "contact": contact,
            "paymentType": payment_type,
            "paymentValue": payment_value,
            "description": description
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        return response.status_code, response.json() if response.ok else response.text


