from src.restq.http_request import HttpRequest
from src.restq.disk_cache import DiskCache


class HttpCachedRequest(HttpRequest):
    def __init__(self):
        self.cache = None
        super().__init__()

    def set_cache(self, cache_dir):
        self.cache = DiskCache(cache_dir)
        return self

    def build(self):
        return self

    def request_get(self, url, cache_name):
        result = super().request_get(url)
        if result.status_code == 200:
            self.cache.save(result.content, cache_name)
            return result.content
        return self.cache.load(cache_name)
