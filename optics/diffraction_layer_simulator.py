# /optics/diffraction_layer_simulator.py
# Simulates beam interference across nested refractive/harmonic planes
# Author: Bryce Wooster

import numpy as np
import matplotlib.pyplot as plt

class DiffractionLayerSimulator:
    """
    Simulates the interference pattern and diffraction behavior as light
    passes through multilayer lensing systems with microphase offsets.
    """

    def __init__(self, aperture_diameter=0.5, wavelength_nm=532, resolution=2048):
        self.aperture_diameter = aperture_diameter  # in meters
        self.wavelength = wavelength_nm * 1e-9      # convert nm to meters
        self.resolution = resolution                # pixels across simulated aperture

    def simulate_pattern(self, ring_spacing_mm=0.1, offset_phase_deg=0.0):
        """
        Simulates the resulting interference pattern from radial ring diffraction
        with optional harmonic phase offset per ring layer.
        """
        x = np.linspace(-1, 1, self.resolution)
        y = np.linspace(-1, 1, self.resolution)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X**2 + Y**2)

        k = 2 * np.pi / self.wavelength
        ring_spacing = ring_spacing_mm * 1e-3

        # Phase term simulates constructive/destructive interference
        phase_shift = np.mod(R / ring_spacing + np.deg2rad(offset_phase_deg), 2 * np.pi)
        field = np.exp(1j * phase_shift)

        intensity = np.abs(np.fft.fftshift(np.fft.fft2(field)))**2
        intensity /= intensity.max()

        return intensity

    def plot_pattern(self, pattern):
        """
        Display simulated diffraction pattern.
        """
        plt.figure(figsize=(6, 6))
        plt.imshow(pattern, cmap='inferno', extent=[-1, 1, -1, 1])
        plt.title("Simulated Diffraction Pattern")
        plt.colorbar(label='Relative Intensity')
        plt.axis('off')
        plt.show()
