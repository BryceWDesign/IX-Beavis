# /optics/photon_trap_array.py
# Photon confinement and angular reflection chamber using micro-mirror rings
# Author: Bryce Wooster

import numpy as np

class PhotonTrapArray:
    """
    Optical module that traps incoming photons using a micro-mirror ring system arranged
    in a recursive sacred geometry pattern. Used to slow light momentarily and increase
    photonic density for enhanced frame resolution during signal capture.
    """

    def __init__(self, ring_count=7, mirrors_per_ring=1536):
        self.ring_count = ring_count
        self.mirrors_per_ring = mirrors_per_ring
        self.mirror_matrix = self._initialize_mirror_geometry()

    def _initialize_mirror_geometry(self):
        """
        Constructs a nested array of micro-mirror angles and positions,
        forming a light vortex-like pattern to maximize containment.
        """
        mirror_matrix = []
        for r in range(self.ring_count):
            radius = 1.0 + 0.25 * r
            angle_step = 2 * np.pi / self.mirrors_per_ring
            ring = []

            for m in range(self.mirrors_per_ring):
                angle = m * angle_step
                # Initial orientation and location
                position = (radius * np.cos(angle), radius * np.sin(angle))
                normal_vector = (-np.cos(angle), -np.sin(angle))  # inward facing
                ring.append({"pos": position, "normal": normal_vector})

            mirror_matrix.append(ring)
        return mirror_matrix

    def simulate_reflections(self, photon_origin, direction, bounce_limit=50):
        """
        Simulate photon path through the mirror ring trap array.
        Used for verification of photon entrapment and measurement modeling.
        """
        path = [photon_origin]
        current_pos = np.array(photon_origin, dtype=float)
        current_dir = np.array(direction, dtype=float) / np.linalg.norm(direction)

        for _ in range(bounce_limit):
            # Simple estimate — reflect off innermost mirror layer
            ring = self.mirror_matrix[0]
            closest = min(ring, key=lambda m: np.linalg.norm(np.array(m["pos"]) - current_pos))
            mirror_pos = np.array(closest["pos"])
            mirror_norm = np.array(closest["normal"])

            to_mirror = mirror_pos - current_pos
            dot = np.dot(current_dir, mirror_norm)

            if dot >= 0:
                break  # Photon escaped

            # Reflect photon
            reflect_dir = current_dir - 2 * dot * mirror_norm
            current_pos += reflect_dir * 0.05  # propagate a step
            current_dir = reflect_dir / np.linalg.norm(reflect_dir)
            path.append(current_pos.copy())

        return np.array(path)

    def get_trap_parameters(self):
        """
        Return key parameters of trap for alignment and diagnostics.
        """
        return {
            "ring_count": self.ring_count,
            "mirrors_per_ring": self.mirrors_per_ring,
            "total_mirrors": self.ring_count * self.mirrors_per_ring,
        }
