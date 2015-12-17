def log_empty_fields(item, logger):
    for key in item.update_fields_list:
        if not item.get(key):
           logger.warning('Key \'%s\' is Empty.' % key)

def get_trunk(content):
    return content.replace('\r','').replace('\n','').replace('\t','').replace(' ','').strip()

def get_content(content, skipFirst=False, skipBlank=True, exclude=()):
    if not content: return None

    idx = skipFirst and 1 or 0
    try:
        picker = content[idx]
    except IndexError:
        return None

    if skipBlank:
        picker = get_trunk(picker)
    return None if (not picker or picker in exclude) else picker
