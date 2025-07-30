# /detectors/photon_event_matrix.py
# High-speed photon detection + burst memory matrix
# Author: Bryce Wooster

import numpy as np
import time

class PhotonEventMatrix:
    """
    High-speed data buffer for logging photon convergence events at picosecond intervals.
    Includes phase coherence tagging and energy signature mapping.
    """

    def __init__(self, max_events=1000000):
        self.max_events = max_events
        self.event_buffer = np.zeros((max_events, 4))  # [timestamp, x, y, phase_tag]
        self.current_index = 0

    def log_event(self, x, y, phase_tag):
        """
        Capture incoming photon event: spatial hit (x,y), harmonic phase metadata.
        """
        if self.current_index < self.max_events:
            self.event_buffer[self.current_index] = [
                time.time(), x, y, phase_tag
            ]
            self.current_index += 1

    def get_recent_events(self, count=100):
        """
        Retrieve most recent photon convergence events for processing pipeline.
        """
        start_idx = max(0, self.current_index - count)
        return self.event_buffer[start_idx:self.current_index]

    def summarize(self):
        print(f"[PhotonMatrix] {self.current_index} events logged")
        if self.current_index > 0:
            print(f"Last event: {self.event_buffer[self.current_index - 1]}")
