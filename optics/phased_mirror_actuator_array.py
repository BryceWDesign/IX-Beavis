# /optics/phased_mirror_actuator_array.py
# Dynamic phase-controlled mirror actuator system
# Author: Bryce Wooster

import numpy as np

class PhasedMirrorActuatorArray:
    """
    Controls a dense actuator mesh responsible for nanometer-level angular
    corrections across the primary and secondary micromirror layers.
    Enables real-time beam alignment stabilization across multiple focus zones.
    """

    def __init__(self, mirror_count=1500, max_deflection_deg=0.25):
        self.mirror_count = mirror_count
        self.max_deflection_deg = max_deflection_deg
        self.deflection_states = np.zeros(mirror_count)

    def apply_phase_pattern(self, phase_array):
        """
        Applies a full 1D phase modulation pattern to the micromirror array.
        Used to compensate for wavefront aberration and off-axis scattering.
        """
        if len(phase_array) != self.mirror_count:
            raise ValueError("Phase array length mismatch")
        self.deflection_states = np.clip(phase_array, -self.max_deflection_deg, self.max_deflection_deg)

    def auto_correct_wavefront(self, incoming_wavefront_map):
        """
        Applies automatic corrections based on detected wavefront errors.
        Requires high-speed telemetry input (e.g. Shack-Hartmann sensor array).
        """
        gradient = np.gradient(incoming_wavefront_map)
        correction = -0.5 * np.array(gradient[:self.mirror_count])
        self.apply_phase_pattern(correction)

    def get_deflection_profile(self):
        """
        Returns current micromirror deflection angles in degrees.
        """
        return self.deflection_states.tolist()

    def zero_all(self):
        """
        Resets all actuator positions to default neutral state.
        """
        self.deflection_states = np.zeros(self.mirror_count)
