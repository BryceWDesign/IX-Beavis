# /output/harmonic_image_reconstructor.py
# Converts decoded harmonic patterns into visual outputs
# Author: Bryce Wooster

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

class HarmonicImageReconstructor:
    """
    Reconstructs visual representations of harmonic signals.
    Converts frequency-domain encoded data (from decoder) into 2D or 3D harmonic image maps.
    """

    def __init__(self, resolution=(256, 256), smoothing=1.5):
        self.resolution = resolution
        self.smoothing = smoothing
        self.last_image = None

    def generate_image(self, signature_vector):
        """
        Transforms harmonic frequency array into an interpretable visual field.
        Uses simple reshaping and filtering to reveal spatial phase formations.
        """
        if signature_vector is None or len(signature_vector) == 0:
            return None

        # Normalize and reshape the vector into a 2D grid
        vector = np.array(signature_vector)
        vector = (vector - np.min(vector)) / (np.max(vector) - np.min(vector) + 1e-9)

        padded = np.zeros(self.resolution)
        min_len = min(vector.shape[0], np.prod(self.resolution))
        padded.flat[:min_len] = vector[:min_len]

        # Smooth to simulate natural field distortion
        image = gaussian_filter(padded, sigma=self.smoothing)
        self.last_image = image
        return image

    def display_last_image(self, cmap="plasma"):
        if self.last_image is None:
            print("[HarmonicImageReconstructor] No image to display.")
            return

        plt.imshow(self.last_image, cmap=cmap)
        plt.title("Harmonic Field Representation")
        plt.colorbar()
        plt.show()
