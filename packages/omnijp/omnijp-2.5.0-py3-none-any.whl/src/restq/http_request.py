from urllib.parse import urljoin
import requests
import configparser
from retry import retry


class HttpRequest:
    def __init__(self):
        self.base_url = ""
        self.headers = {'User-Agent': 'MyApp/1.0'}

    def __str__(self):
        return f'{self.method} {self.base_url}'

    @property
    def tries(self):
        return self.tries

    # Decorate your function with the @retry decorator
    @retry(delay=1, backoff=2, max_delay=4, tries=3)
    def request_get(self, url):
        full_url = urljoin(self.base_url, url)
        return requests.get(full_url, headers=self.headers or None)

    def set_base_url(self, url):
        self.base_url = url
        return self

    def set_headers(self, headers):
        self.headers = headers
        return self

    def build(self):
        return self