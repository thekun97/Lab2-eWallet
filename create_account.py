import hashlib
import json
import os
import secrets
from web3 import Web3

import base58
import qrcode
from Crypto.Hash import RIPEMD160
from Crypto.Cipher import AES
from tinyec import registry
from read_file import read_file

curve = registry.get_curve('secp256r1')
ganache_url = 'https://goerli.infura.io/v3/523a160abf724360909cd4a401af68ae'


def compress_point(point):
    return hex(point.x) + hex(point.y % 2)[2:]


def get_my_key():
    priv_key = secrets.randbelow(curve.field.n)  # k
    g = curve.g
    pub_key = priv_key * g
    my_priv_key = priv_key
    my_pub_key = pub_key
    return my_priv_key, my_pub_key


def make_address(pub_key_point):
    x = pub_key_point.x
    y = pub_key_point.y
    x_byte = x.to_bytes(32, 'little')
    y_byte = y.to_bytes(32, 'little')
    _1_byte_prefix = b"\x02"
    _65_byte_format = b"".join([_1_byte_prefix, x_byte, y_byte])
    m = hashlib.sha256()
    m.update(_65_byte_format)
    hashed_32 = m.digest()

    ripemd_160 = RIPEMD160.new()
    ripemd_160.update(hashed_32)
    hashed_20 = ripemd_160.digest()

    _1_byte_type_address = b"\111"
    _21_byte_format = b"".join([_1_byte_type_address, hashed_20])

    m.update(_21_byte_format)
    hashed_32_2nd = m.digest()

    _4_head_byte = hashed_32_2nd[:4]

    _25_byte_address = b"".join([_21_byte_format, _4_head_byte])
    base_58_str = base58.b58encode(_25_byte_address).decode('ascii')

    char_to_remove = ['+', '/', '0', 'O', '1']
    sc = set(char_to_remove)
    address = ''.join([c for c in base_58_str if c not in sc])
    return address


def make_qrcode_priv_pub_key(priv, address, dirname):
    qr_priv = qrcode.make(priv)
    qr_address = qrcode.make(address)
    qr_code_priv_name = 'QR_PRIVATE.png'
    qr_code_address = 'QR_ADDRESS.png'
    qr_priv.save(f'{dirname}/{qr_code_priv_name}')
    qr_address.save(f'{dirname}/{qr_code_address}')
    return qr_code_priv_name, qr_code_address


def encrypt_private_key(priv_key, password):
    _16_byte_password = password.zfill(16)
    key = _16_byte_password.encode('ascii')
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    cipherpass, tag = cipher.encrypt_and_digest(priv_key.encode('ascii'))
    return cipherpass, nonce, tag


def decrypt_private_key(password):
    ciphertext, nonce = read_file()
    _16_byte_password = password.zfill(16)
    key = _16_byte_password.encode('ascii')
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode('ascii')


def create_account(password):
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    acc = web3.eth.account.create()
    address = acc.address
    priv_key = web3.to_hex(acc._private_key)

    cipherpass, nonce, tag = encrypt_private_key(priv_key, password)

    dirname = f'data'
    if os.path.isdir(dirname) == False:
        os.mkdir(dirname)
        print("The directory is created.")
    else:
        print("The directory already exists.")

    f = open(f"{dirname}/encryted_password.txt", "wb")
    f.write(cipherpass)
    f.close()

    f = open(f"{dirname}/nonce.txt", "wb")
    f.write(nonce)
    f.close()

    qr_code_priv_name, qr_code_address = make_qrcode_priv_pub_key(priv_key, address, dirname)

    json_data_user = {
        'qr_priv_key': qr_code_priv_name,
        'pub_key': qr_code_address,
    }

    with open(f"{dirname}/data.json", 'w', encoding='utf-8') as f:
        json.dump(json_data_user, f, ensure_ascii=False, indent=4)

    return address, priv_key
