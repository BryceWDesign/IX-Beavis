#!/usr/bin/env python3
"""
echo_decoder.py — IX-Beavis Light Echo Decoder & Resonance Memory Analyzer
Author: Bryce Wooster
Version: 1.0 
Description:
Processes captured photon data to extract echo signatures, resonance-layered memory fields,
and temporal envelope anomalies. Designed for cosmic signal memory deconstruction and
multi-frame spectral-field correlation.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, hilbert, correlate
from scipy.fftpack import fft, ifft
from datetime import datetime

# --- CONFIGURABLE PARAMETERS ---
SAMPLE_RATE = 100.0      # Hz (default from capture_interface)
ECHO_THRESHOLD = 0.15     # Minimum amplitude threshold (V) for echo recognition
LAG_WINDOW = 0.3          # Seconds, echo scan limit
VOLATILITY_TOL = 0.05     # % variation from baseline to consider "resonance memory shift"

def load_trace(timestamps, data_dict):
    """Restructure time/data arrays from capture interface"""
    t = np.array(timestamps)
    traces = {k: np.array(v) for k, v in data_dict.items()}
    return t, traces

def detect_echo_peaks(trace, rate=SAMPLE_RATE):
    """Find local peaks and delayed echo intervals"""
    envelope = np.abs(hilbert(trace))
    peaks, _ = find_peaks(envelope, height=ECHO_THRESHOLD)
    echo_times = peaks / rate
    return echo_times, envelope

def extract_resonance_pattern(trace):
    """Extract frequency memory from resonance field"""
    freqs = np.fft.rfftfreq(len(trace), d=1.0/SAMPLE_RATE)
    fft_amp = np.abs(fft(trace))[:len(freqs)]
    return freqs, fft_amp

def cross_echo_correlation(tr1, tr2):
    """Compute correlation between two traces to find time displacement echo match"""
    correlation = correlate(tr1, tr2, mode='full')
    lag = np.argmax(correlation) - len(tr1)
    lag_time = lag / SAMPLE_RATE
    strength = np.max(correlation)
    return lag_time, strength

def plot_echo_output(t, envelope, echo_times, title="Echo Envelope"):
    """Visualize detected echo memory over time"""
    plt.figure(figsize=(10, 4))
    plt.plot(t, envelope, label="Envelope")
    for et in echo_times:
        plt.axvline(et, color='red', linestyle='--', label=f"Echo @ {et:.2f}s")
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (V)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def analyze_echo(timestamps, signal_data):
    """Master function: runs full echo and memory analysis on signal set"""
    t, traces = load_trace(timestamps, signal_data)
    results = {}

    for ch, trace in traces.items():
        echo_times, envelope = detect_echo_peaks(trace)
        freqs, fft_amp = extract_resonance_pattern(trace)

        result = {
            "echo_count": len(echo_times),
            "echo_times": echo_times.tolist(),
            "peak_frequency": freqs[np.argmax(fft_amp)],
            "fft_amplitude": float(np.max(fft_amp)),
        }

        # Check for multi-trace correlation
        for other_ch, other_trace in traces.items():
            if other_ch == ch:
                continue
            lag, strength = cross_echo_correlation(trace, other_trace)
            result[f"correlation_with_ch{other_ch}"] = {
                "lag_seconds": lag,
                "strength": float(strength)
            }

        results[f"channel_{ch}"] = result
        plot_echo_output(t, np.abs(hilbert(trace)), echo_times, title=f"Channel {ch} Echo Trace")

    return results

# --- Optional test/demo entry point ---
if __name__ == "__main__":
    from capture_interface import capture_photon_trace
    print("[*] Running standalone photon echo analysis...")
    timestamps, signal_data = capture_photon_trace(duration=10.0, interval=0.01)
    echo_summary = analyze_echo(timestamps, signal_data)
    print("[✓] Echo Summary:", echo_summary)
