from .charges import chargesAPI
from .buyers import buyersAPI
from .plans import plansAPI
from .subseller import subsellerAPI
from .orders import ordersAPI
from .subscriptions import subscriptionsAPI
from .paymentlinks import paymentlinksAPI

class BarteSDK:
    def __init__(self, api_key, env="prd", api_version="v2"):
        self.api_key = api_key
        self.env = env
        self.api_version = api_version
        self.charges = chargesAPI(api_key, env, api_version)
        self.buyers = buyersAPI(api_key, env, api_version)
        self.plans = plansAPI(api_key, env, api_version)
        self.subseller = subsellerAPI(api_key, env, api_version)
        self.orders = ordersAPI(api_key, env, api_version)
        self.subscriptions = subscriptionsAPI(api_key, env, api_version)
        self.paymentlinks = paymentlinksAPI(api_key, env, api_version)
