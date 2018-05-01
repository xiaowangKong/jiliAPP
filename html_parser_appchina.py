# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup,NavigableString,Tag
from request_wrapper import extract_text,get_html
html_test = '''
you can paste HTML code here for debugging html_parser_xxx
'''


def parse_app_list(html_code):
    assert html_code
    soup = BeautifulSoup(html_code, 'html.parser')
    tag_app_list = soup.find('div', attrs={'class': 'main'})

    if not tag_app_list:
        raise RuntimeError("can't found <div class:main>")

    tag_app_list = tag_app_list.find_all('li',attrs={'class':'has-border app'})

    if not tag_app_list:
        raise RuntimeError("can't found <li>")

    res_list = []

    for tag_app in tag_app_list:
        tag_app_link = tag_app.find('div',attrs={'class':'app-info'})
        assert tag_app_link
        tag_app_name = tag_app_link.find('h1', attrs={'class': 'app-name'})
        assert tag_app_name
        tag_app_name = tag_app_name.find('a')
        assert tag_app_name
        app_name = tag_app_name.text.strip()
        tag_app_link = tag_app.find('div', attrs={'class': 'app-intro'})
        assert tag_app_link
        app_brief = tag_app_link.find('span').text.strip()
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

    tag = soup.find('div', attrs={'class': 'detail-app-intro'})
    assert tag

    tag_brief_long = tag.find('p', attrs={'class': 'art-content'})
    assert tag_brief_long
    tag_brief_long = extract_text(tag_brief_long)
    assert tag_brief_long
    print("hehe")
    print(tag_brief_long)
    '''
    for tag in tag_brief_longs:
        tag_brief_long = tag
        break
    '''
    # print(tag_brief_long)
    # tag_brief_long = re.match(r"<h3>应用介绍</h3><p class=\"pslide\">(.+?)<br/></p>", str(tag_brief_long))
    # print(tag_brief_long)
    tag_download_area = soup.find('div',attrs={'class':'detail-classify'})
    tag_download_area = tag_download_area.find('div',attrs={'class':'download-button direct_download'})
    assert tag_download_area
    tag_download_area = tag_download_area.find('a',attrs={'class':'download_app'})
    assert tag_download_area
    tag_download_area = tag_download_area.get('onclick')
    assert tag_download_area
    tag_download_area = tag_download_area.strip().split("\'")[1]
    assert tag_download_area
    #tmp = tag_download_area.text
    #print(tmp)
    # hehe = tag_brief_long.text
    # hehehe = hehe.replace("\r","")
    return {'app_brief_long': tag_brief_long.strip(),
            'app_download_url': tag_download_area.strip()}

# print(parse_app_details(html_test))
#html_code = get_html("http://www.appchina.com/sou/?keyword=%E8%B6%A3%E5%A4%B4%E6%9D%A1")
#res  = parse_app_list(html_code)
#print(res)
#html_code = get_html("http://www.appchina.com/app/com.jifen.qukan")
#res = parse_app_details(html_code)
#link = "freeDownload(this,'http://103.231.68.98/McDonald/e/5736286/0/0/0/1525149030420/package_20901.1525149030420')"
#print(link.split("\'")[1])
#print(res)
#print(extract_text(p_tag))
#html_code = get_html("http://www.appchina.com/app/netbox.wifihome")
#res = parse_app_details(html_code)
#print(res)