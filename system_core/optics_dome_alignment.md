# IX-Beavis – Optics Dome Alignment Protocol  
**Subsystem: Inward-Facing Micromirror Array & Sacred Geometry Grid Mounting**  
**Author: Bryce Wooster**  
**Version: Physically buildable, Tesla-synchronized, and lab-alignable**

---

## 🔍 Purpose

This document provides the **real-world assembly and alignment process** for the optical capture dome — the layered, sacred geometry–based inward-facing micromirror array that forms the photon compression chamber of the IX-Beavis system.

---

## 📐 Geometry Foundation

- Dome layout is built using a **triple-nested flower-of-life radial array**:
  - **Inner ring**: 18 micromirrors  
  - **Middle ring**: 54 micromirrors  
  - **Outer ring**: 144 micromirrors  
  - Total = **216 precision-tuned mirror modules**, each tilt-capable via MEMS control

- Geometry is embedded in a **non-planar spiraled trinity array** (Gankyil format)  
  - Mirror mounts follow the **3-6-9 positional symmetry**, based on Tesla’s harmonic field rotation sequence  
  - Mount angles spiral inward at **15.3°, 27.6°, and 39.6°** tiers depending on array level

---

## 🧱 Materials Required

| Component | Function |
|----------|----------|
| **Ceramic Mirror Mounts** | Non-conductive, thermal-stable base for micromirrors |
| **Optical-Grade Alignment Pins** | Set angular spacing and ensure rotational harmonic symmetry |
| **Titanium Tension Grid Frame** | Suspends ring lattice across three vertical Z-height bands |
| **IR Reflectivity Markers** | Mounted at key harmonic nodes for calibration laser crosscheck |
| **Multi-Axis Micro Positioner** | (e.g. Newport XYZ stage) – used for center beam cone alignment |

---

## 🧭 Alignment Procedure (Critical Path)

### 🧱 Step 1: Base Layer Mounting  
- Position inner ring (18 mirrors) using CNC-spaced ceramic fixtures  
- Align each mirror inward-facing at **precisely 39.6° tilt**  
- Confirm radial symmetry using circular reticle projected from top-down laser

### 🔄 Step 2: Mid Ring Mount (54 mirrors)  
- Install on titanium spiral bracket arms  
- Set to **27.6° inward tilt**, ensure overlap trajectory intersects center funnel with ≤0.5 mm variance  
- Apply phase marker dots for laser triangulation

### 🔺 Step 3: Outer Ring (144 mirrors)  
- Position using Gankyil radial mount guides  
- Each mirror tilted to **15.3°**, spacing nodes equidistant from internal central axis  
- Set mirror centerlines to intersect **photon trap throat at focal depth of 88 mm**

### 🔬 Step 4: Verification  
- Use fiber-coupled 650 nm collimated laser to confirm mirror angle convergence  
- Project laser from outer ring node and ensure reflection terminates at central photon trap  
- Repeat test on at least 9 cross-symmetric mirror triplets (3-6-9 rule)

---

## 🎯 Calibration Tolerances

| Parameter | Target Value |
|----------|---------------|
| **Mirror concentricity** | ±0.25 mm radial from node |
| **Angular error margin** | ≤ 0.12° per mount |
| **Field convergence error** | ≤ 1.5 mm total across all rings |
| **Z-height ring variance** | < 0.8 mm between mirror ring layers |

---

## 💡 Integration Notes

- All mirrors must be synchronized using `capture_interface.py` and tested under live phase-tuning conditions
- Frame mount tolerances must be thermally decoupled using ceramic or Teflon interface shims
- Titanium ring arms must be grounded back to harmonic center node (per `/system_core/structure_and_frame.md`)
- Laser check protocol must be repeated **after system reaches thermal stability**

---

📌 Resonant tuning adjustments controlled in `/software/harmonic_driver.py`  
📌 Visual alignment diagnostics tool will be in `/software/dome_calibration_gui.py`  

