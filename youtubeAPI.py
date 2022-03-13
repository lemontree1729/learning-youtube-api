import requests
from urllib import parse


def set_url(url, **kwargs):  # query should be dict
    if kwargs.get("query"):
        kwargs["query"] = parse.urlencode(kwargs["query"], doseq=True)
    return parse.urlunparse(parse.urlparse(url)._replace(**kwargs))


def get_youtube_api_json(path, query: dict, show=False):
    base_url = f"https://www.googleapis.com/youtube/v3/{path}"
    api_url = set_url(base_url, query=query)
    html = requests.get(api_url)
    try:
        api_json = html.json()
    except:
        api_json = {"result": "error occurs on youtube api"}
    if show:
        print("api_url:", api_url)
    return api_json
