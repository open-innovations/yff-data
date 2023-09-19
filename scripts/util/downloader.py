import requests


def download_file(url, filename, headers=[]):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
