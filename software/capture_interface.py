#!/usr/bin/env python3
"""
capture_interface.py — IX-Beavis Photon Capture Interface
Author: Bryce Wooster
Version: 1.0 
Description:
Coordinates photon capture from quantum photodiodes and micromirror states,
and routes real-time signal data into FFT and volumetric waveform analyzers.
"""

import time
import numpy as np
import spidev
import RPi.GPIO as GPIO
from datetime import datetime
from scipy.fftpack import fft
import board
import busio
import adafruit_tca9548a  # For I2C multiplexer control
import serial

# --- SENSOR CONFIGURATION ---
PHOTODIODE_CHANNELS = [0, 1, 2]  # Quantum dot detectors (UV, Visible, IR)
ADC_RESOLUTION = 12
ADC_VREF = 3.3  # V

# --- MICROMIRROR GPIO CONFIG (DLP-style control) ---
MIRROR_ENABLE_PINS = [17, 27, 22]  # GPIO for mirror field locking triggers
MIRROR_PWM_PINS = [18, 23, 24]     # PWM pin control for phase tilting

# --- SPI ADC CONFIG (MCP3208 or similar) ---
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

# --- I2C SETUP FOR MULTIPLEXING SENSORS ---
i2c = busio.I2C(board.SCL, board.SDA)
tca = adafruit_tca9548a.TCA9548A(i2c)

# --- INIT GPIO ---
GPIO.setmode(GPIO.BCM)
for pin in MIRROR_ENABLE_PINS + MIRROR_PWM_PINS:
    GPIO.setup(pin, GPIO.OUT)

def read_adc(channel):
    """Read ADC value from photodiode sensor channel"""
    cmd = 0b11 << 6 | (channel & 0x07) << 3
    adc = spi.xfer2([cmd, 0x0, 0x0])
    result = ((adc[1] & 0x0F) << 8) | adc[2]
    voltage = (result / 4096.0) * ADC_VREF
    return voltage

def sync_mirror_array(enable=True, pwm_duty=50):
    """Set micromirror tilt phase and sync cycle state"""
    for enable_pin in MIRROR_ENABLE_PINS:
        GPIO.output(enable_pin, GPIO.HIGH if enable else GPIO.LOW)
    for i, pwm_pin in enumerate(MIRROR_PWM_PINS):
        pwm = GPIO.PWM(pwm_pin, 500 + (i * 100))  # Slightly varied frequency per axis
        pwm.start(pwm_duty)
        time.sleep(0.05)
        pwm.stop()

def capture_photon_trace(duration=5.0, interval=0.01):
    """Capture multi-spectral photon sample set"""
    data = {ch: [] for ch in PHOTODIODE_CHANNELS}
    timestamps = []
    print("[*] Capturing photon trace...")

    start_time = time.time()
    while time.time() - start_time < duration:
        t_now = datetime.utcnow().timestamp()
        for ch in PHOTODIODE_CHANNELS:
            val = read_adc(ch)
            data[ch].append(val)
        timestamps.append(t_now)
        time.sleep(interval)

    return timestamps, data

def compute_fft(channel_data, sample_rate):
    """Compute FFT for a given photon signal"""
    data = np.array(channel_data)
    n = len(data)
    freq = np.fft.fftfreq(n, d=1/sample_rate)
    amp = np.abs(fft(data)) / n
    return freq[:n // 2], amp[:n // 2]

def main():
    print("[*] Initializing IX-Beavis Capture Interface (GOD MODE)")
    sync_mirror_array(enable=True, pwm_duty=60)

    timestamps, signal_data = capture_photon_trace(duration=10.0, interval=0.01)
    
    for ch in PHOTODIODE_CHANNELS:
        freq, amp = compute_fft(signal_data[ch], sample_rate=1/0.01)
        print(f"[CH{ch}] Peak freq: {freq[np.argmax(amp)]:.2f} Hz | Amplitude: {np.max(amp):.4f} V")

    sync_mirror_array(enable=False)
    print("[✓] Photon capture complete.")

if __name__ == "__main__":
    main()
