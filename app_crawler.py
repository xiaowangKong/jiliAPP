from file_parser import parse_list, parse_keyvalue, parse_filterwords
from request_wrapper import get_html, encode_url_app_page,encode_url_main_page
from bs4 import BeautifulSoup


def getAppList(app_page_baseurl,p,app_page_lasturl,main_baseurl,main_lasturl):
    #第一页没有page那一项。
    id = 1
    res = {}
    #url = baseurl + lasturl + str(id)
    url = main_baseurl+main_lasturl
    print (url)
    page_code = get_html(url)
    if page_code is None:
        return []
        # print(page_code)
    print("读取main page **********************************")
    soup = BeautifulSoup(page_code, 'html.parser')  # id="plist"
    hidcomment = soup.find('ul', attrs={'class': 'app-list'})
    item_list = hidcomment.find_all('div', attrs={'class': 'info'})
    # print(item_list)
    # http://shouji.baidu.com/s?data_type=app&multi=0&ajax=1&wd=%E8%B5%9A%E9%92%B1
    for item in item_list:  # href="//item.jd.com/10002531129.html"
        #  print item
        app_href = str(item.find('a', attrs={'class', 'app-name'}).get('href')).strip()
        app_name = str(item.find('a', attrs={'class', 'app-name'}).text).strip()
        # print  content
        app_id = app_href.split('/')[-1].split('.')[0]
        # print(app_name)
        # print(app_href)
        # print(app_id)
        if app_name in res:
            continue
        else:
            res[app_name] = app_id
    print('item_num：')
    print(res)
    # 下面从第一页上解析出总页面个数，然后循环读取
    #从主页获取页面个数########################
    page_num = int(soup.find('input',attrs={'class':'total-page'}).get('value'))
    #page_num = 2
    print(page_num)
    try:
        for i in range(1,page_num):
           print("i=")
           print (i)
           url = app_page_baseurl + app_page_lasturl + str(i)
           print("url=")
           print(url)
           page_code = get_html(url)
           #print(page_code)
           if page_code is None:
               return []
           print("第%d次读取**********************************" % (i+1))
           soup = BeautifulSoup(page_code, 'html.parser')  # id="plist"
           hidcomment = soup.find('ul', attrs={'class': 'app-list'})
           item_list = hidcomment.find_all('div', attrs={'class': 'info'})
           #print(item_list)
           for item in item_list:
               #  print item
               app_href = str(item.find('a', attrs={'class', 'app-name'}).get('href')).strip()
               app_name = str(item.find('a', attrs={'class', 'app-name'}).text).strip()
               # print  content
               app_id = app_href.split('/')[-1].split('.')[0]
               #print(app_name)
               #print(app_href)
               #print(app_id)
               if app_name in res:
                   continue
               else:
                   res[app_name] = app_id
           print('item_num：')
           print(res)
        return res
    except ValueError as e:
      print (url)
      print (e)
      return res
    except KeyError as e:
      print (url)
      print (e)
      return res
    except AttributeError as e:
      print (url)
      print (e)
      return res
    except Exception as e:
      print (url)
      print (e)
      return res


def getAppInfo(list,url1,url2,filter_words,file):
    if(list == None or len(list)<=0):
        print("applist is None!")
        return -1
    for key in list:
        url  = url1+list[key]+url2
        page_code = get_html(url)
        if page_code is None:
            continue
        soup = BeautifulSoup(page_code, 'html.parser')
        hidcomment = soup.find('div', attrs={'class': 'introduction'}).find('div',attrs={'class': 'brief-long'})\
            .find('p').text.strip()
        print (hidcomment)
        if filterApp(hidcomment,filter_words):
            print ("点赚类")
            f = open(file, 'a')
            f.write(str(key))
            f.write('\t')
            f.write(str(url))
            f.write('\t')
            f.write(str(hidcomment))
            f.write("\n")
            f.close()
        else:
            print ('非点赚')

def filterApp(info,filter_words):
    if filter_words == None or len(filter_words) <=0:
        print ("filter_words load failed！")
        return -1
    if info == None or len(info) <=0:
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
    keywords = parse_list("keywords.txt")
    search_entries = parse_keyvalue("domains.txt") #变成
    filter_words = parse_filterwords("filterwords.txt")
    resfile = "shouji.baidu.txt"
    print('Supported appstores: %d' % len(search_entries))

    for appstore_name in search_entries:
        print(appstore_name)
        for keyword in keywords:
            if len(search_entries[appstore_name]) < 2:
                print("%sdomain.txt configure ERROR!" % appstore_name)
                continue

            app_page_url = search_entries[appstore_name][1] + keyword
            print(app_page_url)
            app_page_url = encode_url_app_page(app_page_url)
            print("requesting app page %s" % app_page_url)
            main_url = search_entries[appstore_name][0]+ keyword
            main_url = encode_url_main_page(main_url)
            print("requesting main page %s" % main_url)
            #http://shouji.baidu.com/s?wd=%E8%B5%9A%E9%92%B1
            # &data_type=app&f=header_all%40input&from=web_alad_multi#page57
            res = getAppList(app_page_url, 1, "&page=",main_url,"&data_type=app&f=header_all%40input%40btn_search&from=web_alad_multi")
            #html_search_result = get_html("http://shouji.baidu.com/s?wd=%E8%B5%9A%E9%92%B1&data_type=app&f=header_all%40input&from=web_alad_multi#page2")
            #http://shouji.baidu.com/s?data_type=app&multi=0&ajax=1&wd=%E8%B5%9A%E9%92%B1&page=1
            #print(html_search_result)
            print(res)
            print(len(res))
            #http://shouji.baidu.com/software/10177714.html 这是app下载页面格式
            getAppInfo(res,"http://shouji.baidu.com/software/",".html",filter_words,resfile)
