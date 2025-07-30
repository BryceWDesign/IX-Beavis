# IX-Beavis – Sensors & Signal Processing BOM  
**Subsystem: Photon Detection, Signal Amplification, and Data Routing**  
**Author: Bryce Wooster**  
**Status: Buildable using verified, commercially available sensor systems**

---

## 📡 Spectral Detection & Photonics Input

| Component | Specification | Source Type |
|----------|----------------|-------------|
| **Quantum Dot Photodiode Arrays** | Wideband (UV–IR) photodetectors with low noise; high spectral sensitivity | e.g., Hamamatsu S13370 series or QD-enhanced InGaAs arrays |
| **Superconducting Nanowire Detectors (Optional – Extreme Sensitivity)** | Single-photon counters with <50 ps timing jitter | e.g., Photon Spot SNSPD or ID Quantique modules |
| **Thermal Vision Co-sensor** | LWIR bolometer array (8–14 µm) for thermal mapping overlay | FLIR Lepton 3.5 module or Seek Thermal core |
| **THz Imaging Layer (optional)** | Tunable source/detector for sub-mm wave / terahertz band capture | TeraSense or Virginia Diodes Inc. (VDI) sensors |

---

## 🔍 Signal Amplification & Conditioning

| Component | Specification | Source Type |
|----------|----------------|-------------|
| **Low-Noise Amplifiers (LNAs)** | ≤1 nV/√Hz noise floor, high CMRR, precision gain | Analog Devices ADA4522, Texas Instruments INA828 |
| **Femtosecond Timing Gates** | Electro-optic modulators for delay-based capture triggering | Keysight, Thorlabs EO-PM modulators |
| **Optical Isolators (Fiber/Free-Space)** | Minimizes back-reflection and contamination in photon path | Thorlabs IO-3-1064PM or equivalent |
| **Beam-Splitting Grid (Internal)** | Dielectric cube splitters (50:50, 70:30) for spectral bifurcation | Edmund Optics, Newport |

---

## 🧠 Signal Processing & Extraction Pipeline

| Component | Specification | Source Type |
|----------|----------------|-------------|
| **FPGA Photon Timing Engine** | Real-time photon pulse capture + gate synchronizer | Xilinx Zynq Ultrascale+ or Digilent Genesys ZU board |
| **High-Speed ADC / DAC Modules** | 14–16 bit resolution, ≥250 MSPS | Analog Devices AD9653 series or National Instruments DAQ modules |
| **Multi-Spectrum Signal Router** | Hardware-controlled channel sorting + pre-filter staging | Custom PCB with relay + analog multiplexers (ADG series) |
| **Resonance Signature Mapper** | Converts incoming field signal into harmonic layers (3-6-9 matrix mapping) | Tesla-based resonance decoder logic (to be defined in `/software/`) |
| **Volumetric Output Encoder** | Prepares signal set for holographic reconstruction or 3D waveform viewer | GPU-accelerated OpenCL/NVIDIA Jetson module + FFT/Voxel firmware |

---

## 🔄 Signal Synchronization and Grounding

| Component | Specification | Notes |
|----------|----------------|-------|
| **Time Base Oscillator** | Oven-controlled OCXO 10 MHz master clock (phase-locked) | Stanford Research Systems, Microsemi |
| **Field-Stabilized Ground Plane** | Copper lattice with active nulling (minimizes harmonic interference) | Custom etched PCB with Tesla-field harmonic alignment |
| **Photon Echo Loop** | Memory buffer for echo-pair comparison and time-offset detection | Structured in `/software/echo_decoder.py` |
| **Differential Line Drivers** | Balanced signaling (LVDS, STP) for noise suppression | SN65LVDS047 or equivalent |

---

## 📎 Integration Notes

- All sensors are selected for:
  - Wide spectral compatibility (UV to THz)
  - Real-world commercial sourcing
  - Sub-nanosecond response fidelity where applicable
- Photon paths and all delay-tuned modules must be mounted on:
  - **Optical-grade rails**
  - **Isolated cryogenic supports** where applicable
- All signal lines should run through a **shielded Faraday trench** within the frame

---

📌 Additional interface firmware will be detailed under `/software/capture_interface.py`  
📌 Alignment protocols to be documented in `/testing/photon_lock_validation.md`

