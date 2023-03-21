from web3 import Web3
ganache_url = 'https://goerli.infura.io/v3/523a160abf724360909cd4a401af68ae'
web3 = Web3(Web3.HTTPProvider(ganache_url))


def get_balance(address: str):
    balance = web3.eth.get_balance(address)
    return balance


def pay_transaction(address_1: str, priv_key_1: str, address_2, value: int):
    #get the nonce.  Prevents one from sending the transaction twice
    nonce = web3.eth.get_transaction_count(address_1)

    #build a transaction in a dictionary
    try:
        signed_txn = web3.eth.account.sign_transaction(dict(
            nonce=web3.eth.get_transaction_count(address_1),
            maxFeePerGas=web3.to_wei(250, 'gwei'),
            maxPriorityFeePerGas=web3.to_wei(2, 'gwei'),
            gas=21000,
            to=address_2,
            value=value,
            data=b'',
            chainId=5,
        ),
        priv_key_1,
        )

        #send transaction
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        #get transaction hash
        # print(web3.to_hex(tx_hash))
        return True
    except:
        return False


if __name__ == '__main__':
    account_1 = '0xBA6DED1654b539A7b894F3de6A5EF5A4863BFAA5'
    private_key1 = '0xc0f17094a2c9ab2c3ab5a3aac4a72619de52d871245243d43352d4b7d6976ee0'
    # account_2 = '0x0dff4efA33E89C2Bc38B04ab33B3c1d475446cea'
    account_2 = '0x0dff4efA33E89C2Bc38B04ab33B3c1d475446ceagsdfgsdfgsdfgsdfgsdfgsdf'
    print("Balance before transaction: ", get_balance(account_1))

    status = pay_transaction(account_1, private_key1, account_2, 1)
    if status == True:
        print("Pay successfully, the remaining balance is: ", get_balance(account_1))
    else:
        print("Get error! Please try again.")