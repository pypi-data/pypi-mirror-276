import matplotlib.pyplot as plt
import pandas as pd
import neurokit2 as nk

def plot_signal(df, signal):
    plt.figure(figsize=(20, 20))
    plt.plot(df.index, signal)
    plt.show()

def plot_components(Skin_conductance, smoothed_signal, filtered_signal, tonic_component, phasic_component):
    plt.figure(figsize=(14, 8))

    plt.subplot(4, 1, 1)
    plt.plot(Skin_conductance, label='Raw EDA Data')
    plt.legend()

    plt.subplot(4, 1, 2)
    plt.plot(smoothed_signal, label='Smoothed EDA Data (Mean Moving Average)')
    plt.legend()

    plt.subplot(4, 1, 3)
    plt.plot(filtered_signal, label='Filtered EDA Data (Low Pass Filter)')
    plt.legend()

    plt.subplot(4, 1, 4)
    plt.plot(tonic_component, label='Tonic Component (SCL)')
    plt.plot(phasic_component, label='Phasic Component (SCR)')
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_peaks(phasic_component, peaks):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(phasic_component, label='Signal')

    for onset in peaks['SCR_Onsets']:
        ax.axvline(onset, color='r', linestyle='--', alpha=0.5, label='Onset')
        
    for peak_time, peak_amp in zip(peaks['SCR_Peaks'], peaks['SCR_Height']):
        ax.scatter(peak_time, peak_amp, color='y', marker='o', s=50, label='Peak')

    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.set_title('Signal with SCR Onsets and Peaks')
    ax.legend()

    plt.show()



def plot_metrics_from_csv(file_name):
    metrics_df = pd.read_csv(file_name)
    
    metrics_df.drop(['Peak Count'],axis=1).plot(kind='bar', figsize=(10, 6))
    plt.title('Metrics')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def plot_filered_neurokit_scr_signal(filtered_signal,sample_rate):
    eda_signals, info = nk.eda_process(filtered_signal, sampling_rate=sample_rate)
    plot=nk.eda_plot(eda_signals, info)
    

