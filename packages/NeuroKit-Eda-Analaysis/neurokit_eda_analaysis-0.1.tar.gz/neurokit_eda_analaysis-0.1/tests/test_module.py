import unittest
import pandas as pd
from NeuroKit_Eda_Analaysis import data_processing, signal_processing, plotting, metrics

class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            'time': [1, 2, 3, 4, 5],
            'signal': [10, 20, 30, 40, 50]
        }
        self.df = pd.DataFrame(self.sample_data)

    def test_load_data(self):
        # Assume that the load_data function returns the provided DataFrame
        data = data_processing.load_data(self.df)
        self.assertTrue(data.equals(self.df))

    def test_preprocess_data(self):
        processed_df = data_processing.preprocess_data(self.df)
        self.assertIsInstance(processed_df, pd.DataFrame)
        # Add more assertions to check the preprocessing logic

    def test_calculate_sample_rate(self):
        sample_rate = data_processing.calculate_sample_rate(self.df)
        self.assertEqual(sample_rate, 1)

    def test_fill_missing_values(self):
        df_with_missing = self.df.copy()
        df_with_missing.loc[2, 'signal'] = None
        filled_df = data_processing.fill_missing_values(df_with_missing)
        self.assertFalse(filled_df.isnull().values.any())

class TestSignalProcessing(unittest.TestCase):
    def setUp(self):
        self.signal = [10, 20, 30, 40, 50]
        self.sample_rate = 1

    def test_smooth_signal(self):
        smoothed_signal = signal_processing.smooth_signal(self.signal, self.sample_rate)
        self.assertIsInstance(smoothed_signal, list)
        # Add more assertions to check the smoothing logic

    def test_filter_signal(self):
        filtered_signal = signal_processing.filter_signal(self.signal, self.sample_rate)
        self.assertIsInstance(filtered_signal, list)
        # Add more assertions to check the filtering logic

    def test_extract_components(self):
        tonic, phasic, _ = signal_processing.extract_components(self.signal)
        self.assertIsInstance(tonic, list)
        self.assertIsInstance(phasic, list)
        # Add more assertions to check the component extraction logic

    def test_find_peaks(self):
        phasic_component = [10, 20, 30, 40, 50]
        peaks = signal_processing.find_peaks(phasic_component)
        self.assertIsInstance(peaks, list)
        # Add more assertions to check the peak detection logic

class TestPlotting(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({'signal': [10, 20, 30, 40, 50]})

    def test_plot_signal(self):
        # Assume that the plot_signal function doesn't return anything
        plotting.plot_signal(self.df, 'signal')
        # No assertions needed, as long as the function runs without errors

    # Add more test cases for other plotting functions

class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.eda_processed = [10, 20, 30, 40, 50]
        self.smoothed_signal = [15, 25, 35, 45, 55]
        self.sample_rate = 1

    def test_calculate_metrics(self):
        metrics = metrics.calculate_metrics(self.eda_processed, self.smoothed_signal, self.sample_rate)
        self.assertIsInstance(metrics, dict)
        # Add more assertions to check the calculated metrics

    def test_save_metrics_to_csv(self):
        metrics = {'metric1': 10, 'metric2': 20}
        file_name = 'metrics.csv'
        metrics.save_metrics_to_csv(metrics, file_name)
        # Add assertions to check if the file was created and has the expected content

if __name__ == '__main__':
    unittest.main()