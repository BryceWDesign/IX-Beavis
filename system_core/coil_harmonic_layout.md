# IX-Beavis – Harmonic Coil Layout & Resonant Structuring  
**Subsystem: Tesla 3-6-9 Coil Field Architecture**  
**Author: Bryce Wooster**  
**Version: Buildable, resonance-verified, harmonically tuned**

---

## ⚡ Purpose

This document defines the physical and harmonic configuration of the IX-Beavis coil array system, designed using Tesla’s 3-6-9 field logic. The coil bank serves as the **phase-aligned harmonic driver**, enabling field stabilization, photonic containment, EM null zone generation, and cross-spectral resonance interrogation.

---

## 🧲 Coil Types & Purpose

| Coil Type | Description | Function |
|-----------|-------------|----------|
| **Type 3 Coil** | Primary low-frequency (ELF–VLF) driver | Entrainment of ambient field; baseline harmonic injection |
| **Type 6 Coil** | Mid-frequency EM resonance core | Controls internal EM field density and synchronization loop |
| **Type 9 Coil** | High-frequency phased overcoil | Injects structured harmonics and generates photon trap alignment fields |
| **Toroidal Null Ring** | Triple-wound outer ring (mu-metal + copper) | Field suppression and noise-cancellation barrier for outer shell |

---

## 🧮 Coil Dimensions & Windings

| Coil | Wire Spec | Turns | Core | Q-Factor Target | Spacing |
|------|-----------|-------|------|------------------|---------|
| Type 3 | Copper, 16 AWG | 144 | Air core | >150 | Radial gap: 1.5 cm |
| Type 6 | Copper, 14 AWG | 216 | Delrin spool | >180 | Radial gap: 2.1 cm |
| Type 9 | Copper, 22 AWG (dual twist) | 369 | Ceramic core + ferrite sleeve | >200 | Radial gap: 2.7 cm |
| Null Ring | Copper braid, 3-layer | Continuous | Mu-metal torus | Passive damping only | N/A |

Spacing between coil groups is proportional to 1.618 (Golden Ratio) from center out.

---

## 📐 Physical Layout

**Top-down view (concentric harmonic shell)**  
[ Type 9 Coil (HF driver) ]
⬇
[ Type 6 Coil (MF stabilizer) ]
⬇
[ Type 3 Coil (LF base entrainment) ]
⬇
[ Central null core / photon trap funnel ]

- Each coil set is embedded on ceramic standoff mounts  
- Coils wired in **star-grounded radial symmetry** (not daisy chain)  
- All paths return to master grounding node on baseplate (see `/system_core/structure_and_frame.md`)

---

## 🔁 Harmonic Modulation

| Harmonic Function | Signal Input | Coil Target | Output Effect |
|-------------------|--------------|-------------|----------------|
| **3 Hz – 30 Hz sweep** | Type 3 | Induces field entrainment, eliminates chaotic input | Stabilizes EM background noise |
| **33 Hz – 333 Hz** | Type 6 | Mid-band resonance phase lock | Field structuring, modulates micromirror focus dome integrity |
| **369 Hz – 9.69 kHz** | Type 9 | High-band overcoil phase layering | Injects harmonics into photon delay path for field-imprint decoding |

All signal profiles driven by function generator detailed in `/BOM/power_and_control.md`.

---

## 🔧 Tuning Procedure (Manual)

1. Connect waveform generator to Type 3 coil and sweep through ELF (0.1–10 Hz) while measuring ambient field cancellation via Hall sensor  
2. Lock Type 6 coil to 33 Hz baseline and adjust variable inductance to achieve coil-coupled Q-max  
3. Drive Type 9 with stepped frequency inputs (369 Hz, 3.69 kHz, 9.69 kHz) and fine-tune capacitance until phase reflection amplitude drops to <0.05 V peak  
4. Monitor entire system's harmonic decay profile — target is symmetric ringdown below -40 dB in <3 seconds  

---

## 🧪 Performance Targets

| Parameter | Value |
|-----------|-------|
| **Center null field leakage** | < 12 µV/m |
| **EM field stabilization rate** | < 250 ms to ±1 dB |
| **Resonant signal retention time** | ≥ 2.5 s (at 9.69 kHz) |
| **Field bleed suppression (outer shell)** | > 45 dB vs baseline (using null ring) |
| **Coil thermal drift (under load)** | ≤ 2.2°C at 60 mins continuous duty |

---

## 📌 System Notes

- Each coil has **separate EMI-shielded routing** to the harmonic driver stage  
- Winding direction for all coils follows **clockwise-right-hand rule** for consistent field polarity  
- Alignment tolerance is ±0.8 mm across coil axis due to sensitivity at Type 9 tier  
- Coil geometry is synchronized with sacred geometry chassis using **spiral alignment points** embedded in frame mounts

---

📌 Real-time harmonic control loop handled in `/software/harmonic_driver.py`  
📌 Tesla circuit waveform schematics to appear in `/diagrams/coil_wiring_diagram.png`  

