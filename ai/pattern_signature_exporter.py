# /ai/pattern_signature_exporter.py
# Module to catalog and export unique photonic field pattern signatures
# Author: Bryce Wooster

import hashlib
import numpy as np
import json
from datetime import datetime

class PatternSignatureExporter:
    """
    Extracts a reproducible signature from clustered photonic lattice data.
    Stores time-stamped signature IDs for historical tracking and comparison.
    """

    def __init__(self, export_path='signatures_db.json'):
        self.export_path = export_path
        self.signature_log = []

    def generate_hash(self, coords, labels):
        """
        Create a unique hash from cluster label distribution and geometry.
        """
        hash_input = f"{labels.tolist()}::{coords.mean(axis=0).tolist()}"
        return hashlib.sha256(hash_input.encode()).hexdigest()

    def export_signature(self, coords, labels, metadata=None):
        """
        Saves signature with timestamp and optional user metadata.
        """
        signature_hash = self.generate_hash(coords, labels)
        timestamp = datetime.utcnow().isoformat()

        entry = {
            'timestamp_utc': timestamp,
            'signature_hash': signature_hash,
            'centroid': coords.mean(axis=0).tolist(),
            'cluster_count': len(set(labels)) - (1 if -1 in labels else 0),
            'metadata': metadata or {}
        }

        self.signature_log.append(entry)
        self._save_to_file()
        return signature_hash

    def _save_to_file(self):
        """
        Append the new signature to the JSON database.
        """
        try:
            with open(self.export_path, 'w') as f:
                json.dump(self.signature_log, f, indent=2)
        except Exception as e:
            print(f"[ERROR] Failed to save signature file: {e}")

    def load_existing(self):
        """
        Load existing signature log from disk.
        """
        try:
            with open(self.export_path, 'r') as f:
                self.signature_log = json.load(f)
        except FileNotFoundError:
            self.signature_log = []
