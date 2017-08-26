
pretty_name = "Twitter"
service_name = "twitter"
url = "https://www.twitter.com/"

def search(keyword):
    result = {}

    result['title'] = pretty_name
    result['url'] = url + keyword
    result['source'] = service_name
    result['keyword'] = keyword

    return result