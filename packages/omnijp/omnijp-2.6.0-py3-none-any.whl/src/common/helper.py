import shutil
from itertools import islice


def split_into_subsets(data, n):
    """
    Split the data into n subsets.
    """
    subsets = []
    iterable = iter(data)
    subset = list(islice(iterable, n))
    while subset:
        subsets.append(subset)
        subset = list(islice(iterable, n))
    return subsets

def zip_directory(directory, zip_name, delete_after_zip=True):
    """
    Zip the directory.
    """
    shutil.make_archive(zip_name, 'zip', directory)
    if delete_after_zip:
        shutil.rmtree(directory)