# /software/echo_decoder_matrix.py
# Converts harmonic field data into visual and exportable profiles
# Author: Bryce Wooster

import csv
import numpy as np
import matplotlib.pyplot as plt

class EchoDecoderMatrix:
    """
    Decodes 3-6-9 harmonic field data into usable waveform outputs,
    enabling real-time visualization and export for physical diagnostics.
    """

    def __init__(self, enable_plot=True):
        self.harmonic_log = []
        self.enable_plot = enable_plot

    def ingest(self, harmonic_payload: dict):
        """
        Accepts output from HarmonicReaderCoil.
        Stores harmonic amplitude + phase values into log.
        """
        if harmonic_payload:
            entry = {
                "harmonic_3_amp": harmonic_payload["harmonic_3"]["amplitude"],
                "harmonic_3_phase": harmonic_payload["harmonic_3"]["phase"],
                "harmonic_6_amp": harmonic_payload["harmonic_6"]["amplitude"],
                "harmonic_6_phase": harmonic_payload["harmonic_6"]["phase"],
                "harmonic_9_amp": harmonic_payload["harmonic_9"]["amplitude"],
                "harmonic_9_phase": harmonic_payload["harmonic_9"]["phase"]
            }
            self.harmonic_log.append(entry)

    def visualize_latest(self):
        """
        Plots the phase relationship of 3-6-9 harmonics in polar view
        """
        if not self.harmonic_log:
            print("[Warning] No data to visualize.")
            return

        latest = self.harmonic_log[-1]
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111, polar=True)

        for h in [3, 6, 9]:
            phase = latest[f"harmonic_{h}_phase"]
            amp = latest[f"harmonic_{h}_amp"]
            ax.plot([0, phase], [0, amp], label=f'H{h}', linewidth=2)

        ax.set_title("Harmonic Phase Relationship (3-6-9)")
        ax.legend()
        plt.show()

    def export_csv(self, filepath='harmonic_log.csv'):
        """
        Exports all logged harmonic data to a .csv file
        """
        if not self.harmonic_log:
            print("[Info] No data to export.")
            return

        keys = self.harmonic_log[0].keys()
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.harmonic_log)

        print(f"[Success] Data exported to {filepath}")
