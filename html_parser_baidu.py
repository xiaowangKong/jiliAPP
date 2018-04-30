# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


def parse_app_list(html_code):
    assert html_code
    soup = BeautifulSoup(html_code, 'html.parser')
    tag_app_list = soup.find('ul', attrs={'class': 'app-list'})

    if not tag_app_list:
        raise RuntimeError("can't found <ul class:app-list>")

    tag_app_list = tag_app_list.find_all('div', attrs={'class', 'info'})

    if not tag_app_list:
        raise RuntimeError("can't found <div class:info>")

    res_list = []

    for tag_app in tag_app_list:
        tag_app_link = tag_app.find('a', attrs={'class', 'app-name'})
        tag_app_brief = tag_app.find('span', attrs={'class': 'brief'})
        assert tag_app_link
        assert tag_app_brief

        app_name = tag_app_link.text.strip()
        app_brief = tag_app_brief.text.strip()
        app_detailed_link = tag_app_link.get('href').strip()
        res = {'app_name': app_name, 'app_brief': app_brief, 'app_detailed_link': app_detailed_link}
        res_list.append(res)

    return res_list


def parse_app_details(html_code):
    assert html_code
    #print("html")
  #  print(html_code)
    soup = BeautifulSoup(html_code, 'html.parser')

    tag_brief_long = soup.find('div', attrs={'class': 'introduction'})
    assert tag_brief_long

    tag_brief_long = tag_brief_long.find('div', attrs={'class': 'brief-long'})
    assert tag_brief_long

    tag_brief_long = tag_brief_long.find('p')
    assert tag_brief_long

    tag_download_area = soup.find('div', attrs={'class': 'area-download'})
    assert tag_download_area

    tag_download_url = tag_download_area.find('a', attrs={'class': 'apk'})
    assert tag_download_url

    return {'app_brief_long': tag_brief_long.text.strip(),
            'app_download_url': tag_download_url.get('href').strip()}
