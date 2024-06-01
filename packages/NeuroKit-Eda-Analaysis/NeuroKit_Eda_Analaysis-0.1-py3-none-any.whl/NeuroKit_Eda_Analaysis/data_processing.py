import pandas as pd
import math

def load_data(file_name):
    df = pd.read_csv(file_name)
    return df

def preprocess_data(df):
    df['time'] = pd.to_datetime(df['time'])
    return df

def calculate_sample_rate(df):
    start_time = df['time'].min()
    end_time = df['time'].max()
    timespan = end_time - start_time
    num_samples = len(df['time'])
    sample_rate = num_samples / timespan.total_seconds()
    sample_rate = int(math.ceil(sample_rate))
    return sample_rate

def fill_missing_values(eda_processed):
    eda_processed['SCR_RecoveryTime'].fillna(eda_processed['SCR_RecoveryTime'].mean(), inplace=True)
    eda_processed['SCR_Recovery'].fillna(eda_processed['SCR_RecoveryTime'].mean(), inplace=True)
    return eda_processed
