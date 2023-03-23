from typing import Dict
from fastapi import FastAPI
from fastapi import Request
from nicegui import ui
from fastapi.responses import RedirectResponse

from create_account import create_account, import_your_wallet
from create_account import decrypt_private_key
from utils import get_balance, pay_transaction, get_history

session_info: Dict[str, Dict] = {}


def init(app: FastAPI) -> None:
    def is_authenticated(request: Request) -> bool:
        return session_info.get('user', {}).get('authenticated', False)

    @ui.page('/')
    def index(request: Request):
        if is_authenticated(request):
            return RedirectResponse('/my-wallet')

        with ui.row().classes('mt-8 w-full justify-center items-center'):
            ui.label('Welcome to Kun Chain')

        with ui.row().classes('mt-8 w-full justify-center items-center'):
            ui.button('Create a new Wallet', on_click=lambda: ui.open('/create-wallet'))
            ui.button('Import your exist wallet ', on_click=lambda: ui.open('/import-wallet'))

    @ui.page('/import-wallet')
    def import_wallet():
        def import_wallet():
            address, _ = import_your_wallet(private_key.value, password.value)
            session_info['user'] = {'address': address, 'authenticated': True}
            ui.open('/my-wallet')

        with ui.row().classes('w-full justify-center items-center'):
            private_key = ui.input('Enter your private key').props('type=text') \
                .on('keydown.enter', lambda x: x).classes('max-w-120').style('width: 300px')

        with ui.row().classes('w-full justify-center items-center'):
            password = ui.input('Enter you password').props('type=password') \
                .on('keydown.enter', lambda x: x).classes('max-w-120').style('width: 300px')

        with ui.row().classes('w-full justify-center items-center'):
            ui.button('Import', on_click=import_wallet)

    @ui.page('/create-wallet')
    def create_wallet():
        def handle_create_account() -> None:
            if password.value == '' or re_password.value == '' or password.value != re_password.value:
                ui.notify('Password not match', color='negative')
            else:
                address, _ = create_account(password.value)
                session_info['user'] = {'address': address, 'authenticated': True}
                ui.open('/my-wallet')

        with ui.row().classes('mt-8 w-full justify-center items-center'):
            ui.label('Welcome to Kun Chain')

        with ui.row().classes('w-full justify-center items-center'):
            password = ui.input('Enter your password').props('type=password')\
                .on('keydown.enter', handle_create_account).style('width: 300px')

        with ui.row().classes('w-full justify-center items-center'):
            re_password = ui.input('Confirm you password').props('type=password')\
                .on('keydown.enter', handle_create_account).style('width: 300px')

        with ui.row().classes('w-full justify-center items-center'):
            ui.button('Create', on_click=handle_create_account)

    @ui.page('/my-wallet')
    def my_wallet():

        def show(key):
            with ui.row().classes('w-full justify-center items-center'):
                ui.label(f'Your private key: {key}')

        def show_history(object_transaction):
            with ui.row().classes('w-full justify-center items-center'):
                ui.label(f'List your transactions')

            for hashed_tx, info_tx in object_transaction.items():
                with ui.row().classes('w-full justify-center items-center'):
                    ui.label(f'Hash: {hashed_tx}')
                    ui.label(f'From: {info_tx["from"]}')
                    ui.label(f'To: {info_tx["to"]}')
                    ui.label(f'Value: {info_tx["value"]}')

        def success_transaction(result):
            with ui.row().classes('w-full justify-center items-center'):
                ui.label(f'Your transaction was successful, the hashed transaction is: {result}')

        def explore_privte_key() -> None:
            private_key = decrypt_private_key(password.value)
            session_info['private_key'] = {'private_key': private_key}
            show(private_key)

        def explore_history():
            result = get_history(data['address'])
            show_history(result)

        def send_transaction():
            result = pay_transaction(data["address"], password_send.value, address.value, token.value)
            if result:
                success_transaction(result)

        data = session_info['user']
        balance = get_balance(data['address'])
        with ui.dialog() as dialog, ui.card().style('width: 700em'):
            with ui.row().classes('w-full justify-center items-center column'):
                password = ui.input('Enter your password').props('type=password').style('width: 300px')
            with ui.row().classes('w-full justify-center items-center row'):
                ui.button('Explore private key', on_click=explore_privte_key)
                ui.button('Close', on_click=dialog.close)

        with ui.dialog() as send_dialog, ui.card().style('width: 700em'):
            with ui.row().classes('w-full justify-center items-center column'):
                address = ui.input('Enter destination address').props('type=text').style('width: 300px')

            with ui.row().classes('w-full justify-center items-center column'):
                token = ui.input('Enter value (wei)').props('type=text').style('width: 300px')

            with ui.row().classes('w-full justify-center items-center column'):
                password_send = ui.input('Enter your password').props('type=text').style('width: 300px')

            with ui.row().classes('w-full justify-center items-center row'):
                ui.button('Send', on_click=send_transaction)
                ui.button('Close', on_click=send_dialog.close)

        with ui.row().classes('w-full justify-center items-center'):
            ui.label(f'Your address: {data["address"]}')

        with ui.row().classes('w-full justify-center items-center'):
            ui.label(f'Your balance: {balance} wei = {balance / 10 ** 18} ETH')

        with ui.row().classes('w-full justify-center items-center'):
            ui.button('Get your private key', on_click=dialog.open)
            ui.button('Get your history transaction', on_click=explore_history)
            ui.button('Send', on_click=send_dialog.open)
            ui.button('Logout', on_click=lambda: ui.open('/logout'))

    @ui.page('/logout')
    def logout(request: Request):
        if is_authenticated(request):
            session_info.pop('user')
        return RedirectResponse('/')

    ui.run_with(app)
