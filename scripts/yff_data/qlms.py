
from os.path import basename, exists
from re import compile
from urllib.parse import urlparse
from urllib.request import (Request, build_opener, install_opener, urlopen,
                            urlretrieve)

from bs4 import BeautifulSoup

headers = [
    # ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"),
    # ("Accept-Encoding", "gzip, deflate, br"),
    # ("Accept-Language", "en-GB,en;q=0.5"),
    # ("Cache-Control", "no-cache"),
    # ("Connection", "keep-alive"),
    # ("DNT", "1"),
    # ("Host", "www.ons.gov.uk"),
    # ("Pragma", "no-cache"),
    # ("Referer", "https,//www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/summaryoflabourmarketstatistics"),
    # ("Sec-Fetch-Dest", "document"),
    # ("Sec-Fetch-Mode", "navigate"),
    # ("Sec-Fetch-Site", "same-origin"),
    # ("Sec-Fetch-User", "?1"),
    # ("Sec-GPC", "1"),
    # ("Upgrade-Insecure-Requests", "1"),
    # ("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0"),
]


def get_filename():
    url = urlparse(
        'https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/summaryoflabourmarketstatistics')
    req = Request(url.geturl(),
                  headers={
                      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0",
    })
    with urlopen(req) as site:
        html = site.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

    links = [l['href'] for l in soup.find_all(href=compile('.xls$'))]
    file_link = url._replace(path=links[0])
    return file_link.geturl()


def download_latest():
    url = get_filename()
    filename = basename(url)
    if not exists(filename):
        opener = build_opener()
        opener.addheaders = headers
        install_opener(opener)
        urlretrieve(url, filename)
    return filename
