from pathlib import Path
import inspect
import re


def get_py_path(verbose=False):
    # return Path(globals()['_dh'][0]) if globals().get('_dh') else Path(__file__)
    env = inspect.currentframe().f_back.f_locals
    if ((not env.get('_dh')) and (not env.get('__file__'))):
        env = inspect.currentframe().f_back.f_back.f_locals
    if env.get('_dh'):
        if verbose:
            print('==ipython shell==')
        if env.get('__file__'):
            return Path(env["_dh"][0], env["__file__"]).resolve().parent

        if verbose:
            print('<File.py>: NOT FOUND!')
            print('Next time run with:\n  ipython -i -- <File.py>')
            print('using cwd()')
        return Path(env["_dh"][0])
    if verbose:
        print(f'env = {env}')
    return Path(env["__file__"]).resolve().parent


def parseURI(url_paths):
    r = re.compile(r"/", re.VERBOSE)
    url_split = r.split(url_paths)
    # print(f'url_paths = {url_paths}')
    # print(f'url_split = {url_split}')

    if (len(url_split) % 2) == 0:
        p = map(str, url_split)
        url_params = dict(zip(p, p))
    elif url_paths:
        keys, values = ([] for i in range(2))
        for i in range(0, len(url_split), 2):
            if re.match(r"([a-z_]+)", url_split[i]):
                keys.append(url_split[i])
                values.append(url_split[i + 1])
            else:
                values[-1] = "/".join([values[-1], url_split[i]])
        url_params = dict(zip(keys, values))
    else:
        url_params = {}

    return url_params


def parseUrlPaths(url_paths, req_items, columns):
    # -- parse "params" and "filters" from url paths
    url_params = parseURI(url_paths)

    # -- process filters (pop from url_params if necessary)
    url_filters = url_params.pop("filter") if url_params.get("filter") else ""
    req_filters = req_items["filter"] if req_items.get("filter") else ""
    filters = " AND ".join([f for f in [url_filters, req_filters] if f])

    # -- process params
    req_params = {k:v for (k,v) in req_items.items() if k in columns}
    params = {**url_params, **req_params}

    return params, filters
