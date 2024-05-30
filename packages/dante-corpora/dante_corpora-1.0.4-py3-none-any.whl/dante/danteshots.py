import pandas as pd
import pkg_resources

def get_dataset():
    dataset_path = pkg_resources.resource_filename(__name__, 'data/danteshots.csv')
    with open(dataset_path, 'r') as f:
        data = f.read()
    df = pd.DataFrame(data)
    return df
