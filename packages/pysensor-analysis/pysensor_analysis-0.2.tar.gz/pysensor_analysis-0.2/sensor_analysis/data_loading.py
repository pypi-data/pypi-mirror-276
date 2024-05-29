import pandas as pd
from .data_merging import resample_and_merge_csv

def load_and_merge_datasets(file_paths, date_formats):
    dataframes = [pd.read_csv(file_path, parse_dates=["DataDate"], date_format=date_format) 
                  for file_path, date_format in zip(file_paths, date_formats)]
    
    merged_df, null_counts = resample_and_merge_csv(dataframes)
    
    return merged_df, null_counts
