import os

from shutil import copyfile
from multiprocessing.pool import ThreadPool
from multiprocessing.context import TimeoutError
# Above are our functions
from file_parser import parse_list, parse_keyvalue_new
from request_wrapper import get_html, encode_url_main_page, get_url_root
from html_parser_baidu import parse_app_list as parse_app_list_baidu, parse_app_details as parse_app_details_baidu
from html_parser_xiaomi import parse_app_list as parse_app_list_xiaomi, parse_app_details as parse_app_details_xiaomi
from file_saver import append_file, write_file


def search_app(parse_app_list, search_entry_url, keyword):
    request_url = search_entry_url + keyword
    request_url = encode_url_main_page(request_url)
    matched_app_meta_info = None

    try:
        html_code = get_html(request_url)
    except RuntimeError as e:
        print(e)
        return None

    try:
        app_list = parse_app_list(html_code)
    except RuntimeError as e:
        print("ERR: an error occurred when searching %s" % keyword)
        print(e)
        return None

    if not app_list:
        return None

    for app_meta_info in app_list:
        app_name = app_meta_info['app_name']
        app_brief = app_meta_info['app_brief']
        app_detailed_link = app_meta_info['app_detailed_link']

        # if url start with a slash, which means this is a relative link.
        # so, we need fix the link to a "full-url"
        if app_detailed_link.startswith('/'):
            app_detailed_link = get_url_root(search_entry_url) + app_detailed_link

        if app_name == keyword:
            matched_app_meta_info = {'app_name': app_name,
                                     'app_brief': app_brief,
                                     'app_detailed_link': app_detailed_link}
            break

    return matched_app_meta_info


def get_app_details(parse_app_details, app_details_url):
    # request_url = encode_url_main_page(app_details_url)
    request_url = app_details_url

    try:
        html_code = get_html(request_url)
    except RuntimeError as e:
        print(e)
        return None

    try:
        app_details = parse_app_details(html_code)
    except RuntimeError as e:
        print("ERR: an error occurred when parsing %s" % app_details_url)
        print(e)
        return None

    app_download_url = app_details['app_download_url']

    if app_download_url.startswith('/'):
        app_download_url = get_url_root(app_details_url) + app_download_url
        app_details['app_download_url'] = app_download_url

    return app_details


def crawler(func_parse_app_list, func_parse_app_details, url_search_entry, keyword):
    app_meta_info = search_app(func_parse_app_list, url_search_entry, keyword)
    if not app_meta_info:
        return None

    app_info = app_meta_info.copy()

    app_detailed_info = get_app_details(func_parse_app_details, app_meta_info['app_detailed_link'])

    # we merge meta_info(app_name, app_brief,etc.) & details(app_brief_long, app_download_url)
    if app_detailed_info:
        app_info.update(app_detailed_info)

    return app_info


def crawler_multi(function_mapper, search_entries, keyword):
    app_info = None

    for appstore_name in function_mapper:
        func_parsers = function_mapper[appstore_name]
        func_parse_app_list = func_parsers['func_parse_app_list']
        func_parse_app_details = func_parsers['func_parse_app_details']
        url_search_entry = search_entries[appstore_name]
        app_info = crawler(func_parse_app_list, func_parse_app_details, url_search_entry, keyword)

        if app_info:
            app_info['app_source'] = appstore_name
            break

    return app_info


def main(keywords_file, domains_file, res_file, notfound_file, remained_file, PARALLELISM=8, TASK_TIMEOUT=20):
    search_entries = parse_keyvalue_new(domains_file)
    total_keywords = parse_list(keywords_file)
    keywords = total_keywords

    if len(search_entries) == 0:
        print("ERR: search_entries configure err!")
        return

        # for the first time running
    if not os.path.exists(remained_file):
        copyfile(keywords_file, remained_file)
        print('INFO: not found remained keywords, starting from scratch')
    else:
        keywords = parse_list(remained_file)
        print('Total keywords %d remained %d' % (len(total_keywords), len(keywords)))

    print('Supported appstores: %d' % len(search_entries))

    function_mapper = {'百度手机助手': {'func_parse_app_list': parse_app_list_baidu,
                                  'func_parse_app_details': parse_app_details_baidu},
                       '小米应用商店': {'func_parse_app_list': parse_app_list_xiaomi,
                                  'func_parse_app_details': parse_app_details_xiaomi}}

    pool = ThreadPool(processes=PARALLELISM)

    finished_keywords = keywords.copy()

    not_found = []
    # we take PARALLELISM keywords once
    for idx_start in range(0, len(keywords), PARALLELISM):
        idx_end = min(len(keywords), idx_start + PARALLELISM)
        future_tasks = []

        # launch a bunch of async tasks
        for idx_keyword in range(idx_start, idx_end):
            keyword = keywords[idx_keyword]
            future_tasks.append({'keyword': keyword, 'task': pool.apply_async(crawler_multi,
                                                                              (function_mapper,
                                                                               search_entries,
                                                                               keyword))})

        for task_dict in future_tasks:
            keyword = task_dict['keyword']
            task = task_dict['task']

            try:
                app_info = task.get(timeout=TASK_TIMEOUT)  # Waiting for task done

                if app_info:
                    # once we save 'keyword' to res_file, we remove the keyword from list
                    finished_keywords.remove(keyword)
                    write_file(remained_file, '\n'.join(finished_keywords))

                    # save result
                    append_file(res_file, '%s\t%s\t%s\t%s\t%s' % (
                        "".join(app_info['app_source'].splitlines()),
                        "".join(app_info['app_name'].splitlines()),
                        "".join(app_info['app_brief_long'].splitlines()),
                        "".join(app_info['app_detailed_link'].splitlines()),
                        "".join(app_info['app_download_url'].splitlines())))

                    print('processed: keyword %s found %s from %s' %
                          (keyword, app_info['app_name'], app_info['app_source']))
                else:
                    not_found.append(keyword)
                    print("WARN: can not found %s" % keyword)

            except TimeoutError as e:
                print("WARN: Timeout when fetching %s" % keyword)

    # we searched keywords from all App stores, bet still have keywords not found, save them!
    write_file(notfound_file, "\n".join(not_found))


if __name__ == "__main__":
    if not os.path.exists('output'):
        os.mkdir('output')

    # resfile用于保存在shouji.baidu.com中找到的app的名字 下载地址 应用信息
    main(keywords_file="input/small.sort",
         domains_file="input/domains.txt",
         res_file="output/shouji.baidu_new.txt",
         remained_file="output/remained.txt",
         notfound_file="output/notfound.txt")
    print('All done!')
