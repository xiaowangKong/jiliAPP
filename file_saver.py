import os


def append_file(filename, content):
    with open(filename, 'a', encoding='utf-8') as fo:
        fo.write(content + '\n')
