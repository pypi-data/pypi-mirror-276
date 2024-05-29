import pandas as pd

def resample_and_merge_csv(dataframes, resample_freq='min'):
    def prepare_df(df):
        df['DataDate'] = pd.to_datetime(df['DataDate'])
        df.set_index('DataDate', inplace=True)
        if isinstance(df.index, pd.DatetimeIndex):
            return df.resample(resample_freq).mean().dropna()
        else:
            raise TypeError("Index is not a DatetimeIndex. Resampling requires a DatetimeIndex.")

    try:
        prepared_dfs = [prepare_df(df) for df in dataframes]
        
        merged_df = prepared_dfs[0]
        for df in prepared_dfs[1:]:
            merged_df = pd.merge(merged_df, df, left_index=True, right_index=True, how='inner')
        
        merged_df.reset_index(inplace=True)
        return merged_df, merged_df.isnull().sum()

    except ValueError as e:
        print(f"Error: {e}")
        return None, None
    except TypeError as e:
        print(f"Error: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None
