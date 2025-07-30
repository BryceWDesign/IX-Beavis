# /processing/time_series_decoder.py
# Converts temporal lens matrix outputs into coherent spectral snapshots
# Author: Bryce Wooster

import numpy as np
from scipy.fft import fft, fftfreq

class TimeSeriesDecoder:
    """
    Decodes phase-encoded wavefront data from the temporal lens matrix into
    usable frequency and time-domain data for imaging and analysis.
    """

    def __init__(self, sample_rate_thz=1.0):
        self.sample_rate_thz = sample_rate_thz  # Sampling in terahertz (light-relevant)

    def decode(self, complex_wavefront_matrix):
        """
        Processes a 2D array of complex-valued phase data and performs
        temporal reconstruction via FFT for each spatial axis.
        """
        rows, cols = complex_wavefront_matrix.shape
        freq_data = np.zeros((rows, cols), dtype=np.complex128)
        time_domain_data = np.zeros((rows, cols))

        for r in range(rows):
            row_signal = complex_wavefront_matrix[r, :]
            fft_result = fft(row_signal)
            freqs = fftfreq(len(row_signal), d=1 / self.sample_rate_thz)
            dominant_freq_index = np.argmax(np.abs(fft_result))
            freq_data[r, :] = fft_result
            time_domain_data[r, :] = np.real(np.fft.ifft(fft_result))

        return freq_data, time_domain_data

    def extract_spectral_signature(self, freq_data):
        """
        Derives average spectral signature across all rows.
        """
        magnitude_spectrum = np.abs(freq_data)
        return np.mean(magnitude_spectrum, axis=0)

    def detect_anomalies(self, time_domain_data, threshold=0.5):
        """
        Detects any signal deviation indicative of photon curvature shifts,
        source pulse distortion, or lens artifacts.
        """
        anomalies = np.where(np.abs(time_domain_data) > threshold)
        return list(zip(anomalies[0], anomalies[1]))
