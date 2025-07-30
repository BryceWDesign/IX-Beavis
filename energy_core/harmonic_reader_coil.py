# /energy_core/harmonic_reader_coil.py
# Real-world Tesla-based harmonic reader coil for IX-Beavis
# Author: Bryce Wooster

import numpy as np

class HarmonicReaderCoil:
    """
    Reads photonic phase shifts and energy flux from the photon trap,
    translating them into measurable signal voltages with harmonic tagging.
    """

    def __init__(self, turns=369, coil_diameter_mm=42, wire_diameter_mm=0.4):
        self.turns = turns
        self.coil_diameter_mm = coil_diameter_mm
        self.wire_diameter_mm = wire_diameter_mm
        self.inductance_nH = self._calculate_inductance()
        self.phase_resolution = 0.003  # radians
        self.data_buffer = []

    def _calculate_inductance(self):
        """
        Wheeler formula approximation for circular coil
        """
        r = self.coil_diameter_mm / 2
        l = self.turns
        d = self.wire_diameter_mm
        inductance = (r ** 2 * l ** 2) / (9 * r + 10 * d)
        return inductance * 1e3  # convert to nH

    def feed_photon_flux(self, incoming_waveform: np.ndarray):
        """
        Accepts waveform from photon trap throat, assumes input is in
        time-domain energy pulses. Performs Fourier harmonic deconstruction.
        """
        harmonic_spectrum = np.fft.fft(incoming_waveform)
        amplitudes = np.abs(harmonic_spectrum)
        phases = np.angle(harmonic_spectrum)

        # Extract dominant harmonic regions for 3-6-9 Tesla structuring
        harmonic_payload = self._extract_harmonics(amplitudes, phases)
        self.data_buffer.append(harmonic_payload)

        return harmonic_payload

    def _extract_harmonics(self, amplitudes, phases):
        """
        Pull harmonic keys from 3rd, 6th, and 9th Fourier bins
        """
        result = {
            "harmonic_3": {
                "amplitude": amplitudes[3],
                "phase": phases[3]
            },
            "harmonic_6": {
                "amplitude": amplitudes[6],
                "phase": phases[6]
            },
            "harmonic_9": {
                "amplitude": amplitudes[9],
                "phase": phases[9]
            }
        }
        return result

    def clear_buffer(self):
        self.data_buffer.clear()

    def get_latest_readout(self):
        if not self.data_buffer:
            return None
        return self.data_buffer[-1]
