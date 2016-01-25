def log_empty_fields(item, logger):
    for key in item.update_fields_list:
        if not item.get(key):
           logger.warning('Key \'%s\' is Empty.' % key)

def get_url_param(url, key):
    params_str, params = url.split('?')[-1].split('&'), {}
    for p in params_str:
        k, v = p.split('=')
        params[k] = v

    return params[key]

def get_trunk(content):
    return content.replace('\r','').replace('\n','').replace('\t','').replace(' ','').strip()

def get_content(content, num=1, skipFirst=False, skipBlank=True, exclude=(), delimiter=''):
    if not content: return None

    pos = 0
    while pos < len(content) and not get_trunk(content[pos]): pos += 1
    if skipFirst:
        pos += 1
        while pos < len(content) and not get_trunk(content[pos]): pos += 1
    try:
        picker = content[pos:pos+num]
    except IndexError:
        return None

    if skipBlank:
        picker = [get_trunk(x) for x in picker]
    picker = [x for x in picker if x and x not in exclude]
    return delimiter.join(picker) if picker else None

def get_thread_from_exposure_url(url):
    if url.find('-') != -1:
        return url.split('-')[1]
    if url.find('=') != -1:
        return url.split('=')[-1]
    return None

def get_thread_from_news_url(url):
    pos = url.find('.html')
    if pos != -1:
        return url[:pos].split('/')[-1]
    return None
