from web3 import Web3
from create_account import decrypt_private_key

ganache_url = 'https://goerli.infura.io/v3/523a160abf724360909cd4a401af68ae'
web3 = Web3(Web3.HTTPProvider(ganache_url))


def get_balance(address):
    balance = web3.eth.get_balance(address)
    return balance


def pay_transaction(from_address, password, to_address, value: int):
    private_key = decrypt_private_key(password)

    nonce = web3.eth.get_transaction_count(from_address)

    try:
        signed_txn = web3.eth.account.sign_transaction(dict(
            nonce=web3.eth.get_transaction_count(from_address),
            maxFeePerGas=web3.to_wei(250, 'gwei'),
            maxPriorityFeePerGas=web3.to_wei(2, 'gwei'),
            gas=21000,
            to=to_address,
            value=value,
            data=b'',
            chainId=5,
        ),
        private_key,
        )
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(web3.to_hex(tx_hash))
        return True
    except:
        return False
