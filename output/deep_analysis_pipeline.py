# /output/deep_analysis_pipeline.py
# Advanced real-time inference pipeline for harmonic signal interpretation
# Author: Bryce Wooster

import numpy as np
from output.harmonic_image_reconstructor import HarmonicImageReconstructor
from output.signature_decoder import HarmonicSignatureDecoder
from sklearn.cluster import KMeans
import logging

class DeepAnalysisPipeline:
    """
    Central analyzer that receives raw harmonic signal vectors, reconstructs visualizations,
    and performs pattern clustering for unknown signal classification or anomaly detection.
    """

    def __init__(self, resolution=(256, 256), cluster_count=4):
        self.decoder = HarmonicSignatureDecoder()
        self.reconstructor = HarmonicImageReconstructor(resolution=resolution)
        self.cluster_model = KMeans(n_clusters=cluster_count)
        self.history = []
        logging.basicConfig(level=logging.INFO)

    def analyze(self, encoded_signal):
        """
        Full signal-to-image-to-cluster pipeline.
        Decodes signal, generates image, and classifies based on internal feature space.
        """
        decoded = self.decoder.decode(encoded_signal)
        image = self.reconstructor.generate_image(decoded)

        if image is None:
            logging.warning("Failed to generate harmonic image.")
            return None

        # Flatten image to feature vector for clustering
        flat_img = image.flatten().reshape(1, -1)
        try:
            label = self.cluster_model.predict(flat_img)[0]
        except Exception:
            # Initial fit if model hasn't been trained
            self.cluster_model.fit(flat_img)
            label = self.cluster_model.predict(flat_img)[0]

        self.history.append((label, flat_img))
        logging.info(f"[DeepAnalysis] Signal clustered into group: {label}")
        return label

    def visualize_last(self):
        self.reconstructor.display_last_image()

    def get_history(self):
        return self.history
