# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, NavigableString, Tag
from request_wrapper import extract_text, extract_text_list, get_html

html_test = '''
you can paste HTML code here for debugging html_parser_xxx
'''


def parse_app_list(html_code):
    assert html_code
    soup = BeautifulSoup(html_code, 'html.parser')
    tag_app_list = soup.find('ul', attrs={'id': 'j-search-list'})

    if not tag_app_list:
        raise RuntimeError("can't found <ul class:j-search-list>")

    tag_app_list = tag_app_list.find_all('li', attrs={'class': 'search-item search-searchitems'})

    if not tag_app_list:
        raise RuntimeError("can't found <li>")

    res_list = []

    for tag_app in tag_app_list:
        tag_app_link = tag_app.find('div', attrs={'class': 'app-desc'})
        assert tag_app_link
        tag_app_name = tag_app_link.find('a', attrs={'class': 'name'})
        assert tag_app_name
        app_name = tag_app_name.text.strip()
        app_brief = tag_app_link.find('div', attrs={'class': 'comment'}).text.strip()
        app_detailed_link = tag_app_name.get('href').strip()
        res = {'app_name': app_name, 'app_brief': app_brief, 'app_detailed_link': app_detailed_link}
        res_list.append(res)

    return res_list


# parse_app_list(html_test) DEBUGGING

# html_test = '''
#
# '''

def parse_app_details(html_code):
    assert html_code
    soup = BeautifulSoup(html_code, 'html.parser')

    tag = soup.find('div', attrs={'class': 'detail-wrap'})
    assert tag

    tag_brief_long = tag.find('div', attrs={'class': 'desc-info'})
    assert tag_brief_long

    tag_brief_long = tag_brief_long.find('div', attrs={'class': 'con', 'itemprop': 'description'})
    assert tag_brief_long

    if tag_brief_long.find('p'):
        tag_brief_long = tag_brief_long.find('p')

    tag_download_area = tag.find('div', attrs={'class': 'download-wp'})
    assert tag_download_area

    tag_download_area = tag_download_area.find('a')

    return {'app_brief_long': extract_text(tag_brief_long).strip(),
            'app_download_url': tag_download_area.get('href').strip()}


# html = get_html("http://www.wandoujia.com/apps/org.ie365")
# res = parse_app_details(html)
# print(res)
#
# html = get_html("http://www.wandoujia.com/apps/com.huawei.dbank.v7")
# res = parse_app_details(html)
# print(res)
