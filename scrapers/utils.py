#!/usr/bin/env python3
from rich.prompt import Prompt, PromptBase
from pathlib import Path
import requests
import pickle
import re


domain = re.search(r'[a-z]+', Path().absolute().parent.name).group().replace('bartend', 'bartender')
base_url = f'https://{domain}.hopto.org'


def export_cookies(session='', cookie_file="cookies.pickle", py_path=Path()):
    """Export Session Cookies"""
    pickle.dump(session.cookies, py_path.joinpath(cookie_file).open('wb'))

def export_headers(session='', header_file="headers.pickle", py_path=Path()):
    """Export Session Headers"""
    pickle.dump(session.headers, py_path.joinpath(header_file).open('wb'))

def load_cookies(cookie_file="cookies.pickle", py_path=Path()):
    """Load External Cookies"""
    return pickle.load(py_path.joinpath(cookie_file).open('rb'))

def load_headers(header_file="headers.pickle", py_path=Path()):
    """Load External Headers"""
    return pickle.load(py_path.joinpath(header_file).open('rb'))

def getSession():
    s = requests.Session()
    if Path('cookies.pickle').exists() and Path('headers.pickle').exists():
        s.headers.update(load_headers())
        s.cookies.update(load_cookies())
        return s

    print('Need to log in with backend...')
    username = Prompt.ask('username')
    password = PromptBase.ask('password', password=True)
    params = {
        "username": username,
        "password": password
    }
    r = s.post(url=f"{base_url}/login", data=params)
    export_headers(session=s)
    export_cookies(session=s)
    return s
