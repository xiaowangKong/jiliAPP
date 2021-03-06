# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from request_wrapper import get_redirect_url, get_html

html_test = '''
you can paste HTML code here for debugging html_parser_xxx
'''


def parse_app_list(html_code):
    assert html_code
    soup = BeautifulSoup(html_code, 'html.parser')
    tag_app_list = soup.find('ul', attrs={'class': 'applist'})

    if not tag_app_list:
        raise RuntimeError("can't found <ul class:applist>")

    tag_app_list = tag_app_list.find_all('li', attrs={'class': 'iapp'})

    if not tag_app_list:
        raise RuntimeError("can't found <li>")

    res_list = []

    for tag_app in tag_app_list:
        tag_app_link = tag_app.find('a', attrs={'class': 'agray'})
        assert tag_app_link
        app_name = tag_app_link.get('title').strip()
        app_brief = tag_app_link.find('p').text.strip()
        app_detailed_link = tag_app_link.get('href').strip()
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

    tag = soup.find('div', attrs={'class': 'w670 fl'})
    assert tag

    tag_brief_long = tag.find('div', attrs={'class': 'ibor w668 mart10 hidden'})
    assert tag_brief_long
    tag_brief_long = tag_brief_long.find('div', attrs={'class': 'ibox'})

    tag_brief_long = tag_brief_long.find_all('p')
    assert tag_brief_long

    brief_long = "".join([tag_p.text.strip() for tag_p in tag_brief_long])

    tag_download_area = soup.find('a', attrs={'class': 'dl-icon'})
    assert tag_download_area
    tag_download_area = tag_download_area.get('href')
    assert tag_download_area
    tag_download_area = get_redirect_url(tag_download_area)
    assert tag_download_area
    # hehe = tag_brief_long.text
    # hehehe = hehe.replace("\r","")
    return {'app_brief_long': brief_long,
            'app_download_url': tag_download_area.strip()}


# html_test = get_html('http://www.mumayi.com/android-1085176.html')
# print(parse_app_details(html_test))
