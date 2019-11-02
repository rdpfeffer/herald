from os import path


def segregate_nonexistent_files(filepaths):
    non_existent = frozenset([f for f in filepaths if not path.exists(f)])
    existent = filepaths - non_existent
    return existent, non_existent
