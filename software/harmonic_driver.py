#!/usr/bin/env python3
"""
harmonic_driver.py — IX-Beavis Tesla Harmonic Coil Controller
Author: Bryce Wooster
Version: 1.0 
Description:
Controls and synchronizes all three coil groups (3-6-9) via programmable waveform generation,
phase-lock loop logic, and live feedback from field monitoring sensors.
"""

import time
import numpy as np
import RPi.GPIO as GPIO
from scipy.signal import chirp
import spidev  # SPI comm for DACs and digital pots
import serial   # Optional: UART comm to OCXO or monitoring system

# --- SYSTEM PARAMETERS (Editable) ---
COIL_FREQS = {
    'type3': 3.0,         # Hz
    'type6': 33.0,        # Hz
    'type9': 369.0        # Hz
}

SWEEP_MODE = True         # Enable frequency sweep in initialization
SWEEP_DURATION = 30       # Seconds for full sweep
COIL_UPDATE_RATE = 0.1    # Seconds between updates
DAC_CHANNEL_MAP = {'type3': 0, 'type6': 1, 'type9': 2}
PHASE_OFFSET = {'type3': 0, 'type6': np.pi / 3, 'type9': 2*np.pi / 3}

# --- SPI/DAC Configuration ---
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000

def write_dac(channel, value):
    """Send voltage value to DAC for analog waveform output"""
    command = [channel << 4 | (value >> 8) & 0x0F, value & 0xFF]
    spi.xfer2(command)

def generate_wave(freq, phase=0, duration=1.0, rate=1000):
    """Generate a phase-locked sinusoidal waveform"""
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    return np.sin(2 * np.pi * freq * t + phase)

def initialize_sweep():
    """Optional: sweep frequencies on startup to stabilize field before lock-in"""
    print("[*] Beginning harmonic sweep calibration...")
    sweep_time = SWEEP_DURATION
    for t in np.linspace(0.1, sweep_time, num=300):
        f3 = chirp(t, f0=2.0, f1=4.5, t1=sweep_time, method='linear')
        f6 = chirp(t, f0=25.0, f1=45.0, t1=sweep_time, method='logarithmic')
        f9 = chirp(t, f0=360.0, f1=369.0, t1=sweep_time, method='quadratic')
        apply_harmonics({'type3': f3, 'type6': f6, 'type9': f9})
        time.sleep(0.05)

def apply_harmonics(freq_map):
    """Update coil output with synchronized harmonic waveforms"""
    for coil, freq in freq_map.items():
        phase = PHASE_OFFSET[coil]
        waveform = generate_wave(freq, phase, duration=0.05)
        voltage = int((np.mean(waveform) + 1.0) * 2047)  # Normalize to 12-bit DAC
        write_dac(DAC_CHANNEL_MAP[coil], voltage)

def main_loop():
    print("[*] Harmonic driver running (GOD mode)")
    try:
        while True:
            apply_harmonics(COIL_FREQS)
            time.sleep(COIL_UPDATE_RATE)
    except KeyboardInterrupt:
        print("\n[!] Shutting down harmonic driver.")

if __name__ == "__main__":
    if SWEEP_MODE:
        initialize_sweep()
    main_loop()
