import numpy as np
import pandas as pd

def calculate_metrics(eda_processed, smoothed_signal, sample_rate):
    amplitude_max = max(eda_processed['SCR_Amplitude'])
    amplitude_min = min(eda_processed['SCR_Amplitude'])
    duration_max = max((eda_processed['SCR_RiseTime'] + eda_processed['SCR_RecoveryTime']) / sample_rate)
    duration_min = min((eda_processed['SCR_RiseTime'] + eda_processed['SCR_RecoveryTime']) / sample_rate)
    duration_mean = np.mean((eda_processed['SCR_RiseTime'] + eda_processed['SCR_RecoveryTime']) / sample_rate)
    raw_max = max(smoothed_signal)
    raw_std = np.std(smoothed_signal)
    rise_time_max = max((eda_processed['SCR_Peaks'] - eda_processed['SCR_Onsets']) / sample_rate)
    recovery_time_max = max((eda_processed['SCR_RecoveryTime']) / sample_rate)
    peak_count = len(eda_processed['SCR_Peaks'])

    metrics = {
        'Amplitude Max': amplitude_max,
        'Amplitude Min': amplitude_min,
        'Duration Max': duration_max,
        'Duration Min': duration_min,
        'Duration Mean': duration_mean,
        'Raw Max': raw_max,
        'Raw Std': raw_std,
        'Rise Time Max': rise_time_max,
        'Recovery Time Max': recovery_time_max,
        'Peak Count': peak_count
    }

    return metrics

def save_metrics_to_csv(metrics, file_name):
    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv(file_name, index=False)
