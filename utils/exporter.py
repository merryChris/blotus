def read_cache(ftype='test', fname=None):
    if not fname: return []

    import os
    filename = os.path.join('items', ftype, fname)
    if not os.path.isfile(filename): return []

    from webpage import get_trunk
    f = open(filename, 'r')
    l = map(get_trunk, f.readlines())
    f.close()

    return l

def parse_cookies(cookies_str):
    if not cookies_str: return []

    import json
    raw_cookies, cookies = json.loads(cookies_str), []
    for rc in raw_cookies:
        cookie, flag = {}, False
        for kvs in rc.split(';'):
            if kvs.find('=') == -1: continue
            a, b = kvs.split('=')
            if a in ('domain', 'path'):
                cookie[a] = b
            elif not flag:
                cookie['name'] = a
                cookie['value'] = b
                flag = True

        cookies.append(cookie)

    return cookies

