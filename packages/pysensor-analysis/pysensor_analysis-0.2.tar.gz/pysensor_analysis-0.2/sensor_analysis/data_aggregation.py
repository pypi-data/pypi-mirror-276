import pandas as pd

def resample_and_aggregate(data, resample_freq, aggregation_func):
    resampled_df = None
    if data is not None:
        data['DataDate'] = pd.to_datetime(data['DataDate'])
        data = data.set_index('DataDate') 

        if aggregation_func == 'mean':
            resampled_df = data.resample(resample_freq).mean().dropna()
        elif aggregation_func == 'max':
            resampled_df = data.resample(resample_freq).max().dropna()
        elif aggregation_func == 'min':
            resampled_df = data.resample(resample_freq).min().dropna()
        else:
            raise ValueError("Invalid aggregation function. Choose 'mean', 'max', or 'min'.")
    resampled_df.reset_index(inplace=True)
    return resampled_df, resampled_df.isnull().sum()
