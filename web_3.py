from web3 import Web3, eth
from eth_account import Account
from create_account import get_my_key


priv_key, pub_key_point = get_my_key()
# print(priv_key)
# MAIN_NET_HTTP_ENDPOINT = "https://goerli.infura.io/v3/523a160abf724360909cd4a401af68ae"
# w3 = Web3(Web3.HTTPProvider(MAIN_NET_HTTP_ENDPOINT))
# account = w3.eth.account.from_key(priv_key)
# private_key = account.key
# public_key = account.address
# print(private_key, public_key)


class Web3Mixin:
    def __init__(self, provider):
        self.provider = provider
        self.w3 = Web3(Web3.HTTPProvider(provider))
        self.account = None

    def create_account_web3(self, private_key):
        account = self.w3.eth.account.create(private_key)
        self.account = account
        return account

    def check_connected(self):
        return self.w3.is_connected()

    def get_balance(self):
        balance = self.w3.eth.get_balance(self.account.address)
        print("Balance", balance)


if __name__ == "__main__":
    w3 = Web3Mixin('https://goerli.infura.io/v3/523a160abf724360909cd4a401af68ae')
    w3.create_account_web3(priv_key)
    import pdb; pdb.set_trace()
    w3.get_balance()
