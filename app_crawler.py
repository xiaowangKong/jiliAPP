from file_parser import parse_list, parse_keyvalue_new, parse_filterwords
from request_wrapper import get_html, encode_url_app_page, encode_url_main_page, get_url_root
from html_parser import parse_app_list, parse_app_details
from difflib import SequenceMatcher
from file_saver import append_file
import os


def search_app(search_entry_url, keyword):
    request_url = search_entry_url + keyword
    request_url = encode_url_main_page(request_url)
    html_code = get_html(request_url)
    res = None

    try:
        app_list = parse_app_list(html_code)
    except RuntimeError as e:
        print("ERR: an error occurred when searching %s" % keyword)
        print(e)
        return res

    if not app_list:
        return res

    # since, we may found a few Apps relative to the keyword,
    # we just found the one which most similar to the keyword
    for app_meta_info in app_list:
        app_name = app_meta_info['app_name']
        app_brief = app_meta_info['app_brief']
        app_detailed_link = app_meta_info['app_detailed_link']

        # if url start with a slash, which means this is a relative link.
        # so, we need fix the link to a "full-url"
        if app_detailed_link.startswith('/'):
            app_detailed_link = get_url_root(search_entry_url) + app_detailed_link

        name_similarity = SequenceMatcher(a=app_name, b=keyword).ratio()

        if res is None or name_similarity > res['app_similarity']:
            res = {'app_name': app_name,
                   'app_brief': app_brief,
                   'app_detailed_link': app_detailed_link,
                   'app_similarity': name_similarity}

    return res


def get_app_details(app_details_url):
    request_url = encode_url_main_page(app_details_url)
    html_code = get_html(request_url)
    app_details = None

    try:
        app_details = parse_app_details(html_code)
    except RuntimeError as e:
        print("ERR: an error occurred when parsing %s" % app_details_url)
        print(e)
        return app_details

    app_download_url = app_details['app_download_url']

    if app_download_url.startswith('/'):
        app_download_url = get_url_root(app_details_url) + app_download_url
        app_details['app_download_url'] = app_download_url

    return app_details


def filterApp(info, filter_words):
    if filter_words == None or len(filter_words) <= 0:
        print("filter_words load failed！")
        return -1
    if info == None or len(info) <= 0:
        print("app info None！")
        return -1
    for round in filter_words:
        round_list = filter_words[round]
        flag = False
        for word in round_list:
            if word in info:
                flag = True
        if flag == False:
            return False
    return True


# TODO pause & resume features

if __name__ == "__main__":
    keywords = parse_list("input/small.sort")
    search_entries = parse_keyvalue_new("input/domains_new.txt")
    # resfile用于保存在shouji.baidu.com中找到的app的名字 下载地址 应用信息
    resfile = "output/shouji.baidu_new.txt"
    notfoundfile = "output/notfound.txt"

    if not os.path.exists('output'):
        os.mkdir('output')
    else:
        if os.path.exists(resfile):
            os.remove(resfile)

        # 用于保存没在当前shouji.baidu.com中找到的app名字
        if os.path.exists(notfoundfile):
            os.remove(notfoundfile)

    print('Supported appstores: %d' % len(search_entries))

    for appstore_name in search_entries:
        if len(search_entries[appstore_name]) < 1:
            print("%sdomain.txt configure ERROR!" % appstore_name)
            continue
        print('searching from %s' % appstore_name)

        for keyword in keywords:
            app_meta_info = search_app(search_entries[appstore_name], keyword)
            if not app_meta_info:
                print('WARN: cannot found: %s' % keyword)
                append_file(notfoundfile, keyword)
                continue

            app_info = app_meta_info.copy()

            app_detailed_info = get_app_details(app_meta_info['app_detailed_link'])
            if app_detailed_info:
                app_info.update(app_detailed_info)

            append_file(resfile, str(app_info))

            print('proceed: keyword %s found %s' % (keyword, app_info['app_name']))
