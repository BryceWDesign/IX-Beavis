# /ai/lattice_pattern_interpreter.py
# AI model to interpret meaningful patterns from photonic lattice data
# Author: Bryce Wooster

import numpy as np
from sklearn.cluster import DBSCAN
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

class LatticePatternInterpreter:
    """
    Interprets patterns from the rendered photonic lattice data.
    Detects recurring structures, anomalies, and modulation logic in the signal.
    """

    def __init__(self, eps=0.05, min_samples=5, smoothing_sigma=1.0):
        """
        eps: DBSCAN clustering sensitivity
        min_samples: Minimum samples to form a cluster
        smoothing_sigma: Gaussian blur level to reduce noise
        """
        self.eps = eps
        self.min_samples = min_samples
        self.smoothing_sigma = smoothing_sigma

    def preprocess(self, lattice_data):
        """
        Apply Gaussian smoothing to highlight meaningful contours.
        """
        smoothed = gaussian_filter(lattice_data, sigma=self.smoothing_sigma)
        return smoothed

    def detect_clusters(self, smoothed_data):
        """
        Use DBSCAN to identify clustered regions in normalized data.
        Returns: cluster labels and coordinates
        """
        coords = np.column_stack(np.nonzero(smoothed_data > np.mean(smoothed_data)))
        clustering = DBSCAN(eps=self.eps, min_samples=self.min_samples).fit(coords)
        return clustering.labels_, coords

    def render_clusters(self, labels, coords, title='AI Interpreted Pattern Clusters'):
        """
        Plot and colorize AI-detected clusters in the photonic field.
        """
        plt.figure(figsize=(8, 6))
        scatter = plt.scatter(coords[:, 1], coords[:, 0], c=labels, cmap='tab10', s=10)
        plt.title(title)
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.colorbar(scatter, label='Cluster ID')
        plt.tight_layout()
        plt.show()

    def analyze(self, lattice_data):
        """
        Full pipeline: smooth ➝ cluster ➝ visualize
        """
        smoothed = self.preprocess(lattice_data)
        labels, coords = self.detect_clusters(smoothed)
        self.render_clusters(labels, coords)
        return labels, coords
