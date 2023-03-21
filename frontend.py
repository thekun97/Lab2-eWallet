from typing import Dict
import uuid
from fastapi import FastAPI
from fastapi import Request
from nicegui import app, ui
from fastapi.responses import RedirectResponse

from create_account import create_account
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

    @ui.page('/create-wallet')
    def create_wallet(request: Request):
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
                .on('keydown.enter', handle_create_account).classes('max-w-120')

        with ui.row().classes('w-full justify-center items-center'):
            re_password = ui.input('Confirm you password').props('type=password')\
                .on('keydown.enter', handle_create_account).classes('max-w-120')

        with ui.row().classes('w-full justify-center items-center'):
            ui.button('Create', on_click=handle_create_account)

    @ui.page('/my-wallet')
    def my_wallet():

        def show(key):
            with ui.row().classes('w-full justify-center items-center'):
                ui.label(f'Your private key: {key}')
        
        def show_history(object_transaction):
            for hashed_tx, info_tx in object_transaction.items():
                with ui.row().classes('w-full justify-center items-center'):
                    ui.label(f'Hash: {hashed_tx}')
                    ui.label(f'From: {info_tx["from"]}')
                    ui.label(f'To: {info_tx["to"]}')
                    ui.label(f'Value: {info_tx["value"]}')


        def explore_privte_key() -> None:
            private_key = decrypt_private_key(password.value)
            session_info['private_key'] = {'private_key': private_key}
            show(private_key)

        def explore_history():
            result = get_history('0xBA6DED1654b539A7b894F3de6A5EF5A4863BFAA5')
            show_history(result)

        data = session_info['user']
        balance = get_balance('0xBA6DED1654b539A7b894F3de6A5EF5A4863BFAA5')
        with ui.dialog() as dialog, ui.card().style('width: 700em'):
            with ui.row().classes('w-full justify-center items-center column'):
                password = ui.input('Enter your password').props('type=password')
            with ui.row().classes('w-full justify-center items-center row'):
                ui.button('Explore private key', on_click=explore_privte_key)
                ui.button('Close', on_click=dialog.close)

        with ui.row().classes('w-full justify-center items-center'):
            ui.label(f'Your address: {data["address"]}')
        
        with ui.row().classes('w-full justify-center items-center'):
            ui.label(f'Your address: {balance}')

        with ui.row().classes('w-full justify-center items-center'):
            ui.button('Get your private key', on_click=dialog.open)

        with ui.row().classes('w-full justify-center items-center'):
            ui.button('Get your history transaction', on_click=explore_history)

    ui.run_with(app)
