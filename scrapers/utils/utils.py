#!/usr/bin/env python3
from rich.prompt import Prompt, PromptBase
from pathlib import Path
import requests
import inspect
import pickle
import re


def get_py_path(verbose=False):
    # return Path(globals()['_dh'][0]) if globals().get('_dh') else Path(__file__)
    print('starting at currentframe().f_back') if verbose else ''
    env = inspect.currentframe().f_back.f_locals
    if ((not env.get('_dh')) and (not env.get('__file__'))):
        print('going deeper: currentframe().f_back.f_back') if verbose else ''
        env = inspect.currentframe().f_back.f_back.f_locals
        if ((not env.get('_dh')) and (not env.get('__file__'))):
            print('even deeper: currentframe().f_back.f_back.f_back') if verbose else ''
            env = inspect.currentframe().f_back.f_back.f_back.f_locals
            if ((not env.get('_dh')) and (not env.get('__file__'))):
                print('extra deep: currentframe().f_back.f_back.f_back.f_back') if verbose else ''
                env = inspect.currentframe().f_back.f_back.f_back.f_back.f_locals
    if env.get('_dh'):
        print('==ipython shell==') if verbose else ''
        if env.get('__file__'):
            return Path(env["_dh"][0], env["__file__"]).resolve().parent

        if verbose:
            print('<File.py>: NOT FOUND!')
            print('Next time run with:\n  ipython -i -- <File.py>')
            print('using cwd()')
        return Path(env["_dh"][0])

    print(f'env = {env}') if verbose else ''
    return Path(env["__file__"]).resolve().parent

def export_cookies(session='', cookie_file="cookies.pickle", py_path=get_py_path()):
    """Export Session Cookies"""
    pickle.dump(session.cookies, py_path.joinpath(cookie_file).open('wb'))

def export_headers(session='', header_file="headers.pickle", py_path=get_py_path()):
    """Export Session Headers"""
    pickle.dump(session.headers, py_path.joinpath(header_file).open('wb'))

def load_cookies(cookie_file="cookies.pickle", py_path=get_py_path()):
    """Load External Cookies"""
    return pickle.load(py_path.joinpath(cookie_file).open('rb'))

def load_headers(header_file="headers.pickle", py_path=get_py_path()):
    """Load External Headers"""
    return pickle.load(py_path.joinpath(header_file).open('rb'))

def getSession(py_path=get_py_path()):
    s = requests.Session()
    if py_path.joinpath('cookies.pickle').exists() and py_path.joinpath('headers.pickle').exists():
        s.headers.update(load_headers())
        s.cookies.update(load_cookies())

        # -- check login status...
        r = s.get(url = f'{base_url}/status')
        if 'Error' not in r.json():
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

domain = re.search(r'[a-z]+', get_py_path().parent.parent.name).group().replace('bartend', 'bartender')
base_url = f'https://{domain}.hopto.org'
