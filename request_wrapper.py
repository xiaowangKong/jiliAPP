from urllib.request import Request, urlopen
from urllib.parse import urlsplit, quote, urlunsplit
from urllib.error import URLError
from socket import timeout

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/47.0.2526.73 Chrome/47.0.2526.73 Safari/537.36'
TIME_OUT = 10


# http://shouji.baidu.com/s?data_type=app&multi=0&ajax=1&wd=赚钱
def encode_url_app_page(url):
    right = url.strip().split('wd=')[1]
    left = url.strip().split('wd=')[0]
    right = quote(right)  # to url encoding
    url = left + 'wd=' + right
    return url


def encode_url_main_page(url):
    url = urlsplit(url)
    url_parts = list(url)
    for i in range(0, len(url_parts)):
        url_part = url_parts[i]
        if '=' in url_part:
            left = url_part.split('=')[0]
            right = quote(url_part.split('=')[1])  # to url encoding
            url_parts[i] = left + '=' + right
    url = urlunsplit(url_parts)
    return url


def get_url_root(url):
    part_list = urlsplit(url)
    # e.g http://shouji.baidu.com/software/6989076.html -> part_list[0] = http, part_list[1] = shouji.baidu.com
    return '%s://%s' % (part_list[0], part_list[1])


def get_html(url):  ##URL must be encoded!
    request = Request(url)
    request.add_header('User-Agent', USER_AGENT)
    page_code = None
    try:
        with urlopen(request, timeout=TIME_OUT) as response:
            page_code = response.read()
            page_code = page_code.decode('utf-8')
    except UnicodeDecodeError as e:
        try:
            print("WARN: Trying to decode as 'gbk'")
            page_code = page_code.decode('gbk')
        except UnicodeDecodeError as e:
            print("ERR: error occurred when decoding: %s", url)
            raise e
    except URLError as e:
        print("ERR: error occurred when fetching: %s" % url)
        raise e
    except ConnectionResetError as e:
        print("ERR: ConnectionResetError %s" % url)
        raise e
    except timeout as e:
        print("ERR: Timeout when fetching: %s" % url)
        raise e

    return page_code
