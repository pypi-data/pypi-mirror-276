import neurokit2 as nk
import pandas as pd

def process_eda_signal(signal, sampling_rate):
    eda_signals, info = nk.eda_process(signal, sampling_rate=sampling_rate)
    return eda_signals, info

def smooth_signal(signal, sample_rate, window_size_sec=5):
    size = window_size_sec * sample_rate  # short term window size
    smoothed_signal = nk.signal_smooth(signal, method='moving_average', size=size)
    return smoothed_signal

def filter_signal(signal, sample_rate, highcut=5.0):
    filtered_signal = nk.signal_filter(signal, lowcut=None, highcut=highcut, sampling_rate=sample_rate, method='butterworth', order=4)
    return filtered_signal

def extract_components(signals):
    tonic_component = signals["EDA_Tonic"]
    phasic_component = signals["EDA_Phasic"]
    return tonic_component, phasic_component

def find_peaks(phasic_component):
    peak = nk.eda_findpeaks(phasic_component)
    peaks = pd.DataFrame(peak)
    return peaks
