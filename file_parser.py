# -*- coding: utf-8 -*-
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
    return sorted(res)


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
            if len(tmp) != 3:
                raise ValueError("bad line %s" % line)
            values =[]
            values.append(tmp[1])#用来加载首页，然后解析出第一页的app以及page—num
            values.append(tmp[2])#后面根据page-num的循环进行翻页，因为发现带page-num的页面
            # 跟翻页页面不一样。
            res[tmp[0]] = values
    return res

def parse_keyvalue_new(filename):
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

def parse_filterwords(filename):
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
            value_list = tmp[1].strip().split(",")
            print (value_list)
            res[tmp[0]] = value_list
    return res
