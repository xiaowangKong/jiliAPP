from bs4 import BeautifulSoup
html_test = '''
you can paste HTML code here for debugging html_parser_xxx
'''


def parse_app_list(html_code):
    assert html_code
    soup = BeautifulSoup(html_code, 'html.parser')
    tag_app_list = soup.find('ul', attrs={'class': 'applist'})

    if not tag_app_list:
        raise RuntimeError("can't found <ul class:applist>")

    tag_app_list = tag_app_list.find_all('li')

    if not tag_app_list:
        raise RuntimeError("can't found <li>")

    res_list = []

    for tag_app in tag_app_list:
        tag_app_link = tag_app.find('h5').find('a')
        tag_app_brief = tag_app.find('p', {'class': 'app-desc'}).find('a')
        assert tag_app_link
        assert tag_app_brief

        app_name = tag_app_link.text.strip()
        app_brief = tag_app_brief.text.strip()
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

    tag_brief_long = soup.find('div', attrs={'class': 'app-text'})
    assert tag_brief_long


    tag_brief_long = tag_brief_long.find('p', attrs={'class': 'pslide'})
    assert tag_brief_long
    '''
    for tag in tag_brief_longs:
        tag_brief_long = tag
        break
    '''
    #print(tag_brief_long)
    #tag_brief_long = re.match(r"<h3>应用介绍</h3><p class=\"pslide\">(.+?)<br/></p>", str(tag_brief_long))
    print(tag_brief_long)
    assert tag_brief_long
    tag_download_area = soup.find('div', attrs={'class': 'app-info-down'})
    assert tag_download_area

    tag_download_url = tag_download_area.find('a', attrs={'class': 'download'})
    assert tag_download_url
    #hehe = tag_brief_long.text
   # hehehe = hehe.replace("\r","")
    return {'app_brief_long': tag_brief_long.text.replace("\r","").strip(),
            'app_download_url': tag_download_url.get('href').strip()}

# print(parse_app_details(html_test))
