# -*- coding: utf-8 -*-

"""
Copyright (c) 2016 Randal S. Olson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import pandas as pd
import os
from .dataset_lists import classification_dataset_names, regression_dataset_names

dataset_names = classification_dataset_names + regression_dataset_names
GITHUB_URL = 'https://github.com/EpistasisLab/penn-ml-benchmarks/raw/master/datasets'

def fetch_data(dataset_name, return_X_y=False, local_cache_dir=None):
    """Download a data set from the PMLB, (optionally) store it locally, and return the data set.

    You must be connected to the internet if you are fetching a data set that is not cached locally.

    Parameters
    ----------
    dataset_name: str
        The name of the data set to load from PMLB.
    return_X_y: bool (default: False)
        Whether to return the data in scikit-learn format, with the features and labels stored in separate NumPy arrays.
    local_cache_dir: str (default: None)
        The directory on your local machine to store the data files.
        If None, then the local data cache will not be used.

    Returns
    ----------
    dataset: pd.DataFrame or (array-like, array-like)
        if return_X_y == False: A pandas DataFrame containing the fetched data set.
        if return_X_y == True: A tuple of NumPy arrays containing (features, labels)

    """
    suffix = '.tsv.gz'
    if dataset_name in classification_dataset_names:
        data_type = 'classification'
    elif dataset_name in regression_dataset_names:
        data_type = 'regression'
    else:
        raise ValueError('Data set not found in PMLB.')

    dataset_url = '{GITHUB_URL}/{DATA_TYPE}/{DATASET_NAME}/{DATASET_NAME}{SUFFIX}'.format(GITHUB_URL=GITHUB_URL, DATA_TYPE=data_type, DATASET_NAME=dataset_name, SUFFIX=suffix)

    if local_cache_dir is None:
        dataset = pd.read_csv(dataset_url, sep='\t', compression='gzip')
    else:
        dataset_path = os.path.join(local_cache_dir, dataset_name) + suffix

        # Use the local cache if the file already exists there
        if os.path.exists(dataset_path):
            dataset = pd.read_csv(dataset_path, sep='\t', compression='gzip')
        # Download the data to the local cache if it is not already there
        else:
            dataset = pd.read_csv(dataset_url, sep='\t', compression='gzip')
            dataset.to_csv(dataset_path, sep='\t', compression='gzip', index=False)
    if return_X_y:
        X = dataset.drop('target', axis=1).values
        y = dataset['target'].values
        return (X, y)
    else:
        return dataset
