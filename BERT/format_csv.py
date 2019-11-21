import pandas as pd
import itertools
import os


def flatten(list_of_lists):
    """ [['a', 'b'], ['c']] -> ['a', 'b', 'c'] """
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
    """ Parse all .json files in the given directory, flattened into one big list of tuples """
    repo_files = os.listdir(data_dir)
    return flatten(parse_repo_file(f'{data_dir}/{repo_file}') for repo_file in repo_files)


def data_to_ner_df(data):
    """ Convert parsed token data into a dataframe like ner_dataset.csv """
    df_data = ((f'Sentence: {i}', word, None, tag) for i, file in enumerate(data) for word, tag in zip(*file))
    df_headers = ['Sentence #', 'Word', 'POS', 'Tag']
    df = pd.DataFrame(data=df_data, columns=df_headers)
    return df

if __name__ == '__main__':
    data_dir = '../outputs-all'
    test_repo = f'{data_dir}/0xProject__0x.js.json'
    data = parse_all_repo_files(data_dir)
    df = data_to_ner_df(data)
    ffinv = lambda s: s.mask(s == s.shift())
    df['Sentence #'] = ffinv(df['Sentence #'])
    df.to_csv('types_dataset_utf8.csv', index=False)