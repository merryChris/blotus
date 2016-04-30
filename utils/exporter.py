def read_cache(ftype='test', fname=None):
    if not fname: return []

    import os
    filename = os.path.join('item', ftype, fname)
    if not os.path.isfile(filename): return []

    from webpage import get_trunk
    f = open(filePath, 'r')
    l = map(get_trunk, f.readlines())
    f.close()

    return l
