from pathlib import Path
import inspect


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
