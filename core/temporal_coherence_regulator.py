# /core/temporal_coherence_regulator.py
# Manages phase-locked light packet control to freeze target photons for extended analysis
# Author: Bryce Wooster

import numpy as np

class TemporalCoherenceRegulator:
    """
    Regulates coherence windows and phase alignment of incoming light pulses,
    enabling time-slowing and momentary capture for deep harmonic analysis.
    """

    def __init__(self, coherence_threshold_fs=5.0, sampling_interval_fs=0.5):
        """
        coherence_threshold_fs: max time difference in femtoseconds for phase lock
        sampling_interval_fs: time resolution per sample (in femtoseconds)
        """
        self.coherence_threshold = coherence_threshold_fs
        self.interval = sampling_interval_fs

    def phase_lock(self, pulse_train):
        """
        Attempts to lock phases of input pulse train within coherence threshold.
        pulse_train: list of (time_fs, phase_radians)
        Returns locked_phases: list of booleans indicating phase lock status.
        """
        locked = []
        for i in range(1, len(pulse_train)):
            t1, p1 = pulse_train[i - 1]
            t2, p2 = pulse_train[i]
            dt = abs(t2 - t1)
            dp = abs((p2 - p1 + np.pi) % (2 * np.pi) - np.pi)
            locked.append((dt <= self.coherence_threshold) and (dp <= 0.2))  # radians threshold
        return locked

    def coherence_window(self, pulse_train):
        """
        Calculates average phase-stable window (in fs) from pulse train.
        """
        locked = self.phase_lock(pulse_train)
        count = sum(locked)
        return count * self.interval

    def regulate(self, pulse_train):
        """
        Filters pulse train for only those within phase-stable region.
        Returns new train with stable pulses only.
        """
        locked = self.phase_lock(pulse_train)
        return [pulse_train[i] for i in range(1, len(pulse_train)) if locked[i - 1]]
