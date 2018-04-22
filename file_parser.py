import os


def parse_list(filename):
    res = set()
    if not os.path.exists(filename):
        raise IOError("file %s doesn't exists" % filename)

    with open(filename, 'r', encoding='utf-8') as fi:
        for line in fi:
            line = line.strip()
            if line.startswith("#"):
                continue
            res.add(line)
    return res


def parse_keyvalue(filename):
    res = {}
    if not os.path.exists(filename):
        raise IOError("file %s doesn't exists" % filename)

    with open(filename, 'r', encoding='utf-8') as fi:
        for line in fi:
            line = line.strip()
            if line.startswith("#"):
                continue
            tmp = line.split(' ')
            if len(tmp) != 2:
                raise ValueError("bad line %s" % line)
            res[tmp[0]] = tmp[1]
    return res
