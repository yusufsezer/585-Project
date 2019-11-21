import pandas as pd
import itertools
import os


def flatten(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def parse_repo_file(json_path):
    """ Parse the .json which represents all the files for a repository
    Returns:
    [
        # file 1
        ([token1, token2, ... ], [tag1, tag2, ...])

        # file 2
        ([token1, token2, ... ], [tag1, tag2, ...])

        ...
    ]
    """
    with open(json_path) as file:
        return [tuple(chunk.split() for chunk in line.split('\t')) for line in file]


def parse_all_repo_files(data_dir):
    repo_files = os.listdir(data_dir)
    return flatten(parse_repo_file(f'{data_dir}/{repo_file}') for repo_file in repo_files)


if __name__ == '__main__':
    data_dir = '../outputs-all'
    test_repo = f'{data_dir}/0xProject__0x.js.json'