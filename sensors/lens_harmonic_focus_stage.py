# /sensors/lens_harmonic_focus_stage.py
# Harmonic convergence optics – phase-controlled field lens with 3-6-9 spiral structure
# Author: Bryce Wooster

import numpy as np

class HarmonicFocusStage:
    """
    Uses 3-6-9 harmonic spacing to project a stable convergence point for trapped light,
    allowing focused delivery to high-speed photon readout units.
    """

    def __init__(self, focal_radius=0.13, lens_segments=369, spacing_factor=0.0069):
        self.focal_radius = focal_radius
        self.lens_segments = lens_segments
        self.spacing_factor = spacing_factor
        self.focus_pattern = self._generate_focus_pattern()

    def _generate_focus_pattern(self):
        """
        Generate spiral lens segment array based on 3-6-9 phase angle rules.
        Forms an inward convergence spiral, phase-aligned to temporal trap output.
        """
        pattern = []
        for i in range(self.lens_segments):
            angle = (2 * np.pi * i) / 9  # 3-6-9 spiral
            radius = self.focal_radius - (i * self.spacing_factor)

            pattern.append({
                "x": radius * np.cos(angle),
                "y": radius * np.sin(angle),
                "z": np.tan(i * 0.001),
                "segment_id": i,
                "angle_rad": angle
            })

        return pattern

    def get_lens_geometry(self):
        """
        Output spiral lens segment layout for fabrication or simulation use.
        """
        return self.focus_pattern

    def summarize(self):
        print(f"[Lens Info] Harmonic-focus stage with {self.lens_segments} lens facets")
        print(f"[3-6-9 Spiral] Radial step: {self.spacing_factor:.4f}, Focal radius: {self.focal_radius} m")
