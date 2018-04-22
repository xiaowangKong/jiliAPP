from file_parser import parse_list, parse_keyvalue_new, parse_filterwords
from request_wrapper import get_html, encode_url_app_page, encode_url_main_page
from bs4 import BeautifulSoup
import os


def getAppList(url, keyword):
    res = ""
    page_code = get_html(url)
    if page_code is None:
        return res
    try:
        soup = BeautifulSoup(page_code, 'html.parser')
        hidcomment = soup.find('ul', attrs={'class': 'app-list'})
        item_list = hidcomment.find_all('div', attrs={'class': 'info'})
        # http://shouji.baidu.com/s?data_type=app&multi=0&ajax=1&wd=%E8%B5%9A%E9%92%B1
        for item in item_list:  # href="//item.jd.com/10002531129.html"
            app_href = str(item.find('a', attrs={'class', 'app-name'}).get('href')).strip()
            app_name = str(item.find('a', attrs={'class', 'app-name'}).text).strip()
            app_id = app_href.split('/')[-1].split('.')[0]
            if app_name == keyword:
                res = app_id
                break

    except ValueError as e:
        print(url)
        print(e)
    except KeyError as e:
        print(url)
        print(e)
    except AttributeError as e:
        print(url)
        print(e)
    except Exception as e:
        print(url)
        print(e)
    return res

def getAppInfo(app_name, app_id, url1, url2):
    if (app_id == None or len(app_id) <= 0 or app_name == None or len(app_name) <= 0):
        print("app_id %s is None!" % app_id)
        return -1
    url = url1 + app_id + url2
    page_code = get_html(url)
    if page_code is None:
        print("%s is None!" % url)
        return -1
    soup = BeautifulSoup(page_code, 'html.parser')
    hidcomment = soup.find('div', attrs={'class': 'introduction'}).find('div', attrs={'class': 'brief-long'}) \
        .find('p').text.strip()

    return {'name': app_name, 'url': url, 'comments': hidcomment}


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


if __name__ == "__main__":
    keywords = parse_list("small.sort")
    search_entries = parse_keyvalue_new("domains_new.txt")
    # resfile用于保存在shouji.baidu.com中找到的app的名字 下载地址 应用信息
    resfile = "shouji.baidu_new.txt"
    if os.path.exists(resfile):
        os.remove(resfile)

    # 用于保存没在当前shouji.baidu.com中找到的app名字
    notfoundfile = "notfound.txt"
    if os.path.exists(notfoundfile):
        os.remove(notfoundfile)

    print('Supported appstores: %d' % len(search_entries))

    for appstore_name in search_entries:
        if len(search_entries[appstore_name]) < 1:
            print("%sdomain.txt configure ERROR!" % appstore_name)
            continue
        # print(appstore_name)
        for keyword in keywords:
            request_url = search_entries[appstore_name] + keyword
            request_url = encode_url_main_page(request_url)
            app_id = getAppList(request_url, keyword)
            if len(app_id) > 0:
                app_dicts = getAppInfo(keyword, app_id, "http://shouji.baidu.com/software/", ".html")
                app_name = app_dicts['name']
                app_url = app_dicts['url']
                app_comments = app_dicts['comments']

                with open(resfile, 'a') as fo:
                    fo.write('%s %s %s' % (app_name, app_url, app_comments))

            else:
                # notfoundfile
                with open(notfoundfile, 'a') as fo:
                    fo.write("%s\n" % keyword)
                print("%s NOT FOUND!" % keyword)
            # http://shouji.baidu.com/s?wd=%E8%B5%9A%E9%92%B1
            # &data_type=app&f=header_all%40input&from=web_alad_multi#page57
            # res = getAppList(app_page_url, 1, "&page=",main_url,"&data_type=app&f=header_all%40input%40btn_search&from=web_alad_multi")
            # html_search_result = get_html("http://shouji.baidu.com/s?wd=%E8%B5%9A%E9%92%B1&data_type=app&f=header_all%40input&from=web_alad_multi#page2")
            # http://shouji.baidu.com/s?data_type=app&multi=0&ajax=1&wd=%E8%B5%9A%E9%92%B1&page=1
            # print(html_search_result)
            # print(res)
            # print(len(res))
            # http://shouji.baidu.com/software/10177714.html 这是app下载页面格式
            # getAppInfo(res,"http://shouji.baidu.com/software/",".html",filter_words,resfile)
