# /optics/harmonic_field_combiner.py
# Merges multiple lens-array outputs into a single unified harmonic channel
# Author: Bryce Wooster

import numpy as np

class HarmonicFieldCombiner:
    """
    Combines photonic input from multiple lens outputs into a coherent
    unified signal, preserving phase integrity and frequency fidelity.
    """

    def __init__(self, lens_count=3, harmonic_alignment=3.14159):
        """
        lens_count: number of photonic input sources (lenses)
        harmonic_alignment: target harmonic convergence phase (radians)
        """
        self.lens_count = lens_count
        self.harmonic_alignment = harmonic_alignment

    def combine_fields(self, *fields):
        """
        Accepts photonic field arrays and merges them into one coherent stream.
        Input:
            fields: multiple np.arrays of equal size
        Output:
            combined field with harmonic normalization
        """
        if len(fields) != self.lens_count:
            raise ValueError(f"Expected {self.lens_count} fields, got {len(fields)}")

        stack = np.stack(fields)
        mean_field = np.mean(stack, axis=0)
        phase_adjustment = np.sin(self.harmonic_alignment)  # Tesla harmonic logic
        combined = mean_field * phase_adjustment

        return combined
