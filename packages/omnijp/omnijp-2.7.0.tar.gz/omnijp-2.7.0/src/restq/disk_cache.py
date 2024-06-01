import os
import pickle
from datetime import timedelta, datetime


class DiskCache:
    FILE_PREFIX = "restq_"

    def __init__(self, cache_dir, expires=timedelta(days=5)):
        self.cache_dir = cache_dir
        self.expires = expires

    def save(self, result, cache_name):
        """Saves the result to a file in the cache directory.
        The file name is prefixed with 'restq_' and the cache
        name. """
        try:
            self.clear(cache_name)
            path = self.cache_path(cache_name)
            folder = os.path.dirname(path)
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open(path, 'wb') as fp:
                pickle.dump(result, fp)
        except Exception as e:
            print(f"Error saving cache: {e}")

    def load(self, cache_name):
        """ Loads the result from a file in the cache directory."""
        try:
            path = self.cache_path(cache_name)
            with open(path, 'rb') as fp:
                return pickle.load(fp)
        except Exception as e:
            print(f"Error loading cache: {e}")
            return None

    def clear(self, cache_name):
        """Clears the cache for the given cache name."""
        try:
            for file in os.listdir(self.cache_dir):
                if file.startswith(f"{self.FILE_PREFIX}{cache_name}"):
                    file_path = os.path.join(self.cache_dir, file)
                    creation_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if self.has_expired(creation_time):
                        os.remove(file_path)
        except Exception as e:
            print(f"Error clearing cache: {e}")

    def has_expired(self, timestamp):
        """Returns True if the cache has expired."""
        result_datetime = timestamp + self.expires
        return datetime.utcnow() > result_datetime

    def cache_path(self, cache_name, date=datetime.now()):
        """Returns the cache path for the given cache name."""
        formatted_date = date.strftime("%d-%m-%Y")
        filename = f"{self.FILE_PREFIX}{cache_name}_{formatted_date}.json"
        return os.path.join(self.cache_dir, filename)