from re import compile
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


def get_filename(url, pattern):
    url = urlparse(url)
    req = Request(url.geturl(),
                  headers={
                      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0",
    })
    with urlopen(req) as site:
        html = site.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

    links = [l['href'] for l in soup.find_all(href=compile(pattern))]
    file_link = url._replace(path=links[0])
    return file_link.geturl()
