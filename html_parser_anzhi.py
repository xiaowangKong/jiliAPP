# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup,NavigableString,Tag
from request_wrapper import extract_text,get_html,get_redirect_url
html_test = '''
you can paste HTML code here for debugging html_parser_xxx
'''


def parse_app_list(html_code):
    assert html_code
    soup = BeautifulSoup(html_code, 'html.parser')
    tag_app_list = soup.find('div', attrs={'class': 'app_list border_three'})

    if not tag_app_list:
        raise RuntimeError("can't found <div class:app_list border_three>")

    tag_app_list = tag_app_list.find_all('li')

    if not tag_app_list:
        raise RuntimeError("can't found <li>")

    res_list = []

    for tag_app in tag_app_list:
        tag_app_link = tag_app.find('div',attrs={'class':'app_info'})
        assert tag_app_link
        tag_app_name = tag_app_link.find('span', attrs={'class': 'app_name'})
        assert tag_app_name
        tag_app_name = tag_app_name.find('a')
        assert tag_app_name
        app_name = extract_text(tag_app_name).strip()
        assert app_name
        app_brief = tag_app_link.find('p')
        assert app_brief
        app_brief = extract_text(app_brief)
        app_detailed_link = tag_app_name.get('href')
        assert app_detailed_link
        res = {'app_name': app_name, 'app_brief': app_brief, 'app_detailed_link': app_detailed_link.strip()}
        res_list.append(res)

    return res_list


# parse_app_list(html_test) DEBUGGING

# html_test = '''
#
# '''

def parse_app_details(html_code):
    assert html_code
    soup = BeautifulSoup(html_code, 'html.parser')

    tag = soup.find('div', attrs={'class': 'border_three'})
    assert tag

    tag_brief_long = tag.find('div', attrs={'class': 'app_detail_list'})
    assert tag_brief_long
    tag_brief_long = tag_brief_long.find('div', attrs={'class': 'app_detail_infor'})
    assert tag_brief_long
    tag_brief_long = tag_brief_long.find('p')
    assert tag_brief_long
    tag_brief_long = extract_text(tag_brief_long)
    assert tag_brief_long
    #print("hehe")
    #print(tag_brief_long)
    '''
    for tag in tag_brief_longs:
        tag_brief_long = tag
        break
    '''
    tag_download_area = soup.find('div',attrs={'class':'detail_down'})
    assert tag_download_area
    tag_download_area = tag_download_area.find('a',attrs={'title':'下载到电脑'})
    assert tag_download_area
    tag_download_area = tag_download_area.get('onclick')
    assert tag_download_area
    tag_download_area = tag_download_area.strip().split("(")[1].split(")")[0]
    assert tag_download_area  #get id in "opendown(id)"
    return {'app_brief_long': tag_brief_long.strip(),
            'app_download_url': tag_download_area.strip()}

'''debug
html_code = get_html("http://www.anzhi.com/search.php?keyword=%E6%83%A0%E9%94%81%E5%B1%8F")
res  = parse_app_list(html_code)
print(res)
html_code = get_html("http://www.anzhi.com/pkg/08d7_com.huaqian.html")
res = parse_app_details(html_code)
print(res)
debug'''
#link = "freeDownload(this,'http://103.231.68.98/McDonald/e/5736286/0/0/0/1525149030420/package_20901.1525149030420')"
#print(link.split("\'")[1])
#print(extract_text(p_tag))