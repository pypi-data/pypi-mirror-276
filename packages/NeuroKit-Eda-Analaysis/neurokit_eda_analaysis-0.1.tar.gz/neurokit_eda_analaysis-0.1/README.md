# NeuroKit_Eda_Analysis
# EDA Analysis Library
# This library provides tools for processing, analyzing, and visualizing Electrodermal Activity (EDA) data. It includes functions for loading and preprocessing data, smoothing and filtering signals, extracting features, and plotting results.

# Table of Contents
# - [Installation](#installation)
# - [Usage](#usage)
#   - [Loading and Preprocessing Data](#loading-and-preprocessing-data)
#   - [Signal Processing](#signal-processing)
#   - [Metrics Calculation](#metrics-calculation)
#   - [Plotting](#plotting)
# - [Modules](#modules)
#   - [data_processing](#data_processing)
#   - [signal_processing](#signal_processing)
#   - [plotting](#plotting)
#   - [metrics](#metrics)
# - [Contributing](#contributing)
# - [License](#license)

# Installation
 To install the required dependencies, use:
 pip install -r requirements.txt


# Modules

## data_processing
### Functions for loading and preprocessing data:
  - `load_data(file_name)`
  - `preprocess_data(df)` 
  - `calculate_sample_rate(df)`
  - `fill_missing_values(df)`

## signal_processing
### Functions for signal processing:
  - `process_eda_signal(filtered_signal, sample_rate)`
  - `smooth_signal(signal, sample_rate)`
  - `filter_signal(signal, sample_rate)`
  - `extract_components(signals)`
  - `find_peaks(phasic_component)`

## plotting
### Functions for plotting:
  - `plot_signal(df, signal)`
  - `plot_components(Skin_conductance, smoothed_signal, filtered_signal, tonic_component, phasic_component)`
  - `plot_peaks(phasic_component, peaks)`
  - `plot_metrics_from_csv(file_name)`
  - `plot_filtered_neurokit_scr_signal(filtered_signal, sample_rate)`

## metrics
### Functions for metrics calculation:
  - `calculate_metrics(eda_processed, smoothed_signal, sample_rate)`
  - `save_metrics_to_csv(metrics, file_name)`

# Contributing
# Contributions are welcome! Please feel free to submit a Pull Request.
