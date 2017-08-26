
pretty_name = "Reddit"
service_name = "reddit"
url = "https://www.reddit.com/"

def search(keyword):
    result = {}

    result['title'] = pretty_name
    result['url'] = url + keyword
    result['source'] = service_name
    result['keyword'] = keyword

    return result