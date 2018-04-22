from file_parser import parse_list, parse_keyvalue
from request_wrapper import get_html

if __name__ == "__main__":
    keywords = parse_list("keywords.txt")
    search_entries = parse_keyvalue("domains.txt")
    print('Supported appstores: %d' % len(search_entries))

    for appstore_name in search_entries:
        for keyword in keywords:
            request_url = search_entries[appstore_name] + keyword
            print("requesting %s" % request_url)
            html_search_result = get_html(request_url)
            print(html_search_result)
            break
