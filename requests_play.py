import requests

def get_url(url):
    r = requests.get(url)
    print(r.headers)
    print(r.content)
    pass