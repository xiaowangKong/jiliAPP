from file_parser import parse_list, parse_keyvalue_new, parse_filterwords
from request_wrapper import get_html, encode_url_main_page, get_url_root
from html_parser_baidu import parse_app_list as parse_app_list_baidu, parse_app_details as parse_app_details_baidu
from html_parser_xiaomi import parse_app_list as parse_app_list_xiaomi, parse_app_details as parse_app_details_xiaomi
from file_saver import append_file
import os


def search_app(parse_app_list, search_entry_url, keyword):
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

    for app_meta_info in app_list:
        app_name = app_meta_info['app_name']
        app_brief = app_meta_info['app_brief']
        app_detailed_link = app_meta_info['app_detailed_link']

        # if url start with a slash, which means this is a relative link.
        # so, we need fix the link to a "full-url"
        if app_detailed_link.startswith('/'):
            app_detailed_link = get_url_root(search_entry_url) + app_detailed_link

        if app_name == keyword:
            res = {'app_name': app_name,
                   'app_brief': app_brief,
                   'app_detailed_link': app_detailed_link}

    return res


def get_app_details(parse_app_details, app_details_url):
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

    function_mapper = {'百度手机助手': {'func_parse_app_list': parse_app_list_baidu,
                                  'func_parse_app_details': parse_app_details_baidu},
                       '小米应用商店': {'func_parse_app_list': parse_app_list_xiaomi,
                                  'func_parse_app_details': parse_app_details_xiaomi}}

    for appstore_name in search_entries:
        if len(search_entries[appstore_name]) < 1:
            print("%sdomain.txt configure ERROR!" % appstore_name)
            continue
        print('searching from %s' % appstore_name)
        func_parsers = function_mapper[appstore_name]
        func_parse_app_list = func_parsers['func_parse_app_list']
        func_app_details = func_parsers['func_parse_app_details']

        not_found = []
        for keyword in keywords:
            app_meta_info = search_app(func_parse_app_list, search_entries[appstore_name], keyword)
            if not app_meta_info:
                print('WARN: cannot found: %s' % keyword)
                append_file(notfoundfile, keyword)
                not_found.append(keyword)
                continue

            app_info = app_meta_info.copy()

            app_detailed_info = get_app_details(func_app_details, app_meta_info['app_detailed_link'])
            if app_detailed_info:
                app_info.update(app_detailed_info)

            append_file(resfile, '%s\t%s\t%s\t%s' % (
                app_info['app_name'],
                app_info['app_brief_long'],
                app_info['app_detailed_link'],
                app_info['app_download_url']))

            print('proceed: keyword %s found %s' % (keyword, app_info['app_name']))

        keywords = not_found  # we use up this app sotre, we need search keywords from new store
