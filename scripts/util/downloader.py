from urllib.request import build_opener, install_opener, urlretrieve


def download_file(url, filename, headers=[]):
    opener = build_opener()
    opener.addheaders = headers
    install_opener(opener)
    urlretrieve(url, filename)
