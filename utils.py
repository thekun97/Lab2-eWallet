import pickle
from web3 import Web3


ganache_url = 'https://goerli.infura.io/v3/523a160abf724360909cd4a401af68ae'
w3 = Web3(Web3.HTTPProvider(ganache_url))


def get_balance(address: str):
    balance = w3.eth.get_balance(address)
    return balance


def pay_transaction(address_1: str, priv_key_1: str, address_2, value: int):
    #get the nonce.  Prevents one from sending the transaction twice
    nonce = w3.eth.get_transaction_count(address_1)

    #build a transaction in a dictionary
    try:
        signed_txn = w3.eth.account.sign_transaction(dict(
            nonce=w3.eth.get_transaction_count(address_1),
            maxFeePerGas=w3.to_wei(250, 'gwei'),
            maxPriorityFeePerGas=w3.to_wei(2, 'gwei'),
            gas=21000,
            to=address_2,
            value=value,
            data=b'',
            chainId=5,
        ),
        priv_key_1,
        )

        #send transaction
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        #get transaction hash
        # print(w3.to_hex(tx_hash))
        return True
    except:
        return False


def get_history(address: str, num_blocks: int = 10):
    # request the latest block number
    end = w3.eth.block_number

    # latest block number minus 100 blocks
    start = end - num_blocks

    # create an empty dictionary we will add transaction data to
    tx_dictionary = {}


    print(f"Started filtering through block number {start} to {end} for transactions involving the address - {address}...")
    for x in range(start, end):
        block = w3.eth.get_block(x, True)
        for transaction in block.transactions:
            if transaction['to'] == address or transaction['from'] == address:
                hashStr = transaction['hash'].hex()
                tx_dictionary[hashStr] = transaction
    print(f"Finished searching blocks {start} through {end} and found {len(tx_dictionary)} transactions")

    return tx_dictionary


if __name__ == '__main__':
    account_1 = '0xBA6DED1654b539A7b894F3de6A5EF5A4863BFAA5'
    private_key1 = '0xc0f17094a2c9ab2c3ab5a3aac4a72619de52d871245243d43352d4b7d6976ee0'
    account_2 = '0x0dff4efA33E89C2Bc38B04ab33B3c1d475446cea'
    # account_2 = '0x0dff4efA33E89C2Bc38B04ab33B3c1d475446ceagsdfgsdfgsdfgsdfgsdfgsdf'
    print("Balance before transaction: ", get_balance(account_1))

    status = pay_transaction(account_1, private_key1, account_2, 1)
    if status == True:
        print("Pay successfully, the remaining balance is: ", get_balance(account_1))
    else:
        print("Get error! Please try again.")
    # get_history(account_1)