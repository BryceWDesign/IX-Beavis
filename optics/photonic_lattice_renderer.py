# /optics/photonic_lattice_renderer.py
# Converts unified harmonic field into 2D/3D photonic lattice map for reconstruction
# Author: Bryce Wooster

import numpy as np
import matplotlib.pyplot as plt

class PhotonicLatticeRenderer:
    """
    Renders harmonically combined photonic data into a spatial lattice map,
    visualizing real-world angular and phase-corrected positions of light packets.
    """

    def __init__(self, grid_size=(512, 512), mode='2D'):
        """
        grid_size: tuple defining render dimensions (rows, columns)
        mode: '2D' for planar output, '3D' for volumetric (placeholder for future)
        """
        self.grid_size = grid_size
        self.mode = mode

    def normalize_field(self, combined_field):
        """
        Normalize the photonic data to [0,1] for visual rendering
        """
        min_val = np.min(combined_field)
        max_val = np.max(combined_field)
        norm_field = (combined_field - min_val) / (max_val - min_val + 1e-9)
        return norm_field

    def render(self, combined_field, title='Photonic Lattice Map'):
        """
        Render the normalized photonic harmonic field to a 2D heatmap.
        """
        if self.mode != '2D':
            raise NotImplementedError("Only 2D mode is currently supported.")

        norm_field = self.normalize_field(combined_field)
        plt.figure(figsize=(8, 6))
        plt.imshow(norm_field, cmap='inferno', interpolation='bilinear')
        plt.colorbar(label='Normalized Intensity')
        plt.title(title)
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.tight_layout()
        plt.show()
