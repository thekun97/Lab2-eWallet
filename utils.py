from web3 import Web3
from create_account import decrypt_private_key

ganache_url = 'https://goerli.infura.io/v3/523a160abf724360909cd4a401af68ae'
web3 = Web3(Web3.HTTPProvider(ganache_url))


def get_balance(address):
    balance = web3.eth.get_balance(address)
    return balance


def pay_transaction(from_address, password, to_address, value):
    private_key = decrypt_private_key(password)

    signed_txn = web3.eth.account.sign_transaction(dict(
        nonce=web3.eth.get_transaction_count(from_address),
        maxFeePerGas=web3.to_wei(250, 'gwei'),
        maxPriorityFeePerGas=web3.to_wei(2, 'gwei'),
        gas=21000,
        to=to_address,
        value=int(value),
        data=b'',
        chainId=5,
    ),
    private_key,
    )
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print('AAAAA',web3.to_hex(tx_hash))
    return web3.to_hex(tx_hash)


def get_history(address: str, num_blocks: int = 10):
    # request the latest block number
    end = web3.eth.block_number

    # latest block number minus 100 blocks
    start = end - num_blocks

    # create an empty dictionary we will add transaction data to
    tx_dictionary = {}


    print(f"Started filtering through block number {start} to {end} for transactions involving the address - {address}...")
    for x in range(start, end):
        block = web3.eth.get_block(x, True)
        for transaction in block.transactions:
            if transaction['to'] == address or transaction['from'] == address:
                hashStr = transaction['hash'].hex()
                tx_dictionary[hashStr] = transaction
    print(f"Finished searching blocks {start} through {end} and found {len(tx_dictionary)} transactions")

    return tx_dictionary
