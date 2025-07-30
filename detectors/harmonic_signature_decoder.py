# /detectors/harmonic_signature_decoder.py
# Harmonic signal extraction + translation
# Author: Bryce Wooster

import numpy as np
from scipy.fft import fft

class HarmonicSignatureDecoder:
    """
    Translates raw photon event data into harmonic signal codes using FFT and custom Tesla-derived 3-6-9 coherence models.
    """

    def __init__(self, reference_patterns=None):
        self.reference_patterns = reference_patterns or {}
        self.last_spectrum = None
        self.last_match = None

    def decode(self, photon_events):
        """
        Convert photon event hits into frequency-domain representation.
        Match with known resonance fingerprints.
        """
        if photon_events.shape[0] == 0:
            return None

        # Construct pseudo-waveform from time delta of photon arrivals
        times = photon_events[:, 0]
        deltas = np.diff(times)

        if len(deltas) < 16:
            return None  # not enough data for harmonic inference

        # Use FFT to analyze harmonic structure
        spectrum = np.abs(fft(deltas - np.mean(deltas)))
        self.last_spectrum = spectrum

        best_score = 0
        best_tag = None
        for tag, ref in self.reference_patterns.items():
            score = self._match_spectrum(spectrum, ref)
            if score > best_score:
                best_score = score
                best_tag = tag

        self.last_match = best_tag
        return best_tag

    def _match_spectrum(self, spectrum, reference):
        """
        Compare harmonic intensity alignment across known pattern.
        """
        min_len = min(len(spectrum), len(reference))
        return np.dot(spectrum[:min_len], reference[:min_len]) / (
            np.linalg.norm(spectrum[:min_len]) * np.linalg.norm(reference[:min_len]) + 1e-8
        )

    def print_last_result(self):
        print(f"[Decoder] Last harmonic match: {self.last_match}")
