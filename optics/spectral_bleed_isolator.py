# /optics/spectral_bleed_isolator.py
# Filters spectral bleeding and isolates interference-caused anomalies
# Author: Bryce Wooster

import numpy as np

class SpectralBleedIsolator:
    """
    Isolates and subtracts spectral bleed (cross-channel contamination)
    caused by electromagnetic shearing or near-field signal overlap.
    """

    def __init__(self, channels=1024, bleed_threshold=0.015):
        """
        channels: number of spectral bins
        bleed_threshold: normalized cross-talk sensitivity (0.0–1.0)
        """
        self.channels = channels
        self.bleed_threshold = bleed_threshold
        self.last_spectrum = np.zeros(channels)

    def isolate_bleed(self, spectrum):
        """
        Detects and isolates EM bleed by comparing temporal deltas between channels.
        spectrum: np.array of current spectral readings
        Returns: corrected spectrum and bleed map
        """
        delta = spectrum - self.last_spectrum
        bleed_map = np.zeros_like(spectrum)

        for i in range(1, self.channels - 1):
            if abs(delta[i] - (delta[i - 1] + delta[i + 1]) / 2) > self.bleed_threshold:
                bleed_map[i] = delta[i]
                spectrum[i] -= bleed_map[i]

        self.last_spectrum = spectrum.copy()
        return spectrum, bleed_map

    def reset(self):
        self.last_spectrum = np.zeros(self.channels)
