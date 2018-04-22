from urllib.request import Request, urlopen
from urllib.parse import urlsplit, quote, urlunsplit
from urllib.error import URLError
import socket

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
TIME_OUT = 1


def get_html(url):
    url = urlsplit(url)
    url_parts = list(url)
    for i in range(0, len(url_parts)):
        if '=' in url_parts[i]:
            left = url_parts[i].split('=')[0]
            right = quote(url_parts[i].split('=')[1]) # to url encoding
            url_parts[i] = left + '=' + right
    url = urlunsplit(url_parts)
    request = Request(url)
    request.add_header('User-Agent', USER_AGENT)
    page_code = None
    try:
        response = urlopen(request, timeout=TIME_OUT)
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
    except socket.timeout as e:
        print("ERR: Timeout when fetching: %s" % url)
        raise e

    return page_code
