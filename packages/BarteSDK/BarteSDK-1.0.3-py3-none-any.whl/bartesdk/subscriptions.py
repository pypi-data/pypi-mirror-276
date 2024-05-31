import requests

class subscriptionsAPI:
    def __init__(self, api_key, env="prd", api_version="v2"):
        self.api_key = api_key
        self.base_url = self._get_base_url(env, api_version)

    def _get_base_url(self, env, api_version):
        if env == "prd":
            return f'https://api.barte.com/{api_version}/subscriptions'
        elif env == "sandbox":
            return f'https://sandbox-api.barte.com/{api_version}/subscriptions'
        else:
            raise ValueError("Invalid environment specified")

    def getByUuid(self, uuid):
        headers = {
            'X-Token-Api': self.api_key
        }
        url = f"{self.base_url}/{uuid}"
        response = requests.get(url, headers=headers)
        return response.json()

    def create(self, uuid_plan, basic_value, additional_value, payment, uuid_buyer, start_date):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }
        payload = {
            "uuidPlan": uuid_plan,
            "basicValue": basic_value,
            "additionalValue": additional_value,
            "payment": payment,
            "uuidBuyer": uuid_buyer,
            "startDate": start_date
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        return response.status_code, response.json() if response.ok else response.text

    def updateBasicValue(self, subscription_id, uuid_plan, basic_value_type, value_per_month, bank_slip_description):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json',
            'accept': '*/*'
        }
        payload = {
            "uuidPlan": uuid_plan,
            "basicValueRequest": {
                "type": basic_value_type,
                "valuePerMonth": value_per_month
            },
            "bankSlipDescription": bank_slip_description
        }
        url = f"{self.base_url}/{subscription_id}/basic-value"
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

    def get(self, **params):
        headers = {
            'X-Token-Api': self.api_key
        }
        response = requests.get(self.base_url, headers=headers, params=params)
        return response.json()