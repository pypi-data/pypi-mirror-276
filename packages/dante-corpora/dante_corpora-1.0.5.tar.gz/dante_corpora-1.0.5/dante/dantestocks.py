import pandas as pd
import pkg_resources

def get_dataset():
    dataset_path = pkg_resources.resource_filename(__name__, 'data/dantestocks.csv')
    df = pd.read_csv(dataset_path)
    return df
