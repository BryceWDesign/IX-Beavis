# IX-Beavis – Power & Harmonic Control BOM  
**Subsystem: Power Regulation, Tesla Harmonic Synchronization, Field Nullification**  
**Author: Bryce Wooster**  
**Status: All components are real-world, commercially available, and integration-ready**

---

## 🔋 Primary Power Input & Regulation

| Component | Specification | Source Type |
|----------|----------------|-------------|
| **AC-DC Modular Power Supply** | 12V, 24V, ±15V, and ±5V rail modules (≥150W total load) | MeanWell RT-125 series or TDK-Lambda multi-output PSUs |
| **Isolated DC-DC Converters** | Galvanically isolated modules for sensitive analog/digital lines | Recom, Vicor, or Traco Power (rated >85% efficiency) |
| **Battery Buffer (optional)** | LiFePO4 bank (12V/20Ah min) with pure sine wave inverter backup | Battle Born, Bioenno, or Dakota Lithium kits |
| **Power Conditioning Unit** | Active EMI/RFI filters + surge protection | Schaffner FN series / Tripp Lite industrial filter units |

---

## ⚙️ Harmonic Field Control (Tesla Logic Core)

| Component | Specification | Source Type |
|----------|----------------|-------------|
| **Tesla Harmonic Coil Bank** | Triple-wound LCR-tuned coils in 3-6-9 configuration (variable inductance) | Hand-wound copper, 12–18 AWG, shielded toroidal core or air-core, ceramic standoffs |
| **Waveform Generator (Primary Driver)** | Arbitrary function generator (0.01 Hz – 5 MHz) with sync out | Siglent SDG2042X, Rigol DG1022Z, or Keysight EDU33212A |
| **Class D Harmonic Amplifier** | 0–20 kHz resonant amplification, >100W RMS, matched to coil impedance | Crown XLS series, DIY amp with IRF540N MOSFETs |
| **Phase-Locking Loop (PLL)** | Synchronizes field oscillations with crystal oscillator master clock | Analog Devices PLL IC (e.g., ADF4351) or custom PCB clock sync system |
| **Frequency-Responsive Feedback Sensors** | Hall effect sensors + piezoelectric pickups to detect harmonic field coherence | Honeywell SS49E, Murata PKM17EPP-4001 |

---

## ⚡ Control Interface & Actuation

| Component | Specification | Notes |
|----------|----------------|-------|
| **Raspberry Pi 5 or Jetson Nano** | Primary control board for GPIO/mirror sync/harmonic tuning | Runs real-time control stack (to be defined in `/software/`) |
| **Digital Potentiometers** | Used for voltage-controlled resonance modulation | MCP41010 or Analog Devices AD5292 series |
| **Solid-State Relays (SSR)** | Optical-isolated 2–20 A for safe subsystem switching | Crydom, Omron G3NA, or Panasonic AQ-H series |
| **I²C/SPI Bus Expansion Chips** | Multiplexes multiple sensors/mirrors/field monitors | PCA9548A (I²C), MCP23S17 (SPI) |
| **Thermal Control Loops** | PWM fan driver + thermistor logic + heat pipe feedback | Microchip TC654, Vishay NTC thermistors, Noctua fans (whisper-class) |

---

## 🧩 Synchronization Backbone

| Component | Specification | Purpose |
|----------|----------------|---------|
| **OCXO Time Base (Shared with Signal Path)** | 10 MHz oven-controlled master oscillator | Shared with `/BOM/sensors_and_signal.md` for temporal lock-in |
| **Master Ground Reference Node** | Copper star-ground plate with differential symmetry lines | Prevents harmonic phase drift and ground loop distortions |
| **Multi-Zone Shield Isolation Ring** | Ferrite bead-lined compartments separating analog/digital/coil domains | Essential for Tesla coil EM isolation at high harmonics |

---

## 📝 Integration Notes

- Tesla harmonic control and mirror actuation must be:
  - **Phase-locked to main OCXO time base**
  - **EM-isolated through shielded partitions**
  - Fed through **filtered, regulated DC rails only**
- Every power subsystem must survive a full **field collapse and self-recover**
- Use **solid ground planes**, **line ferrites**, and **multi-layer shielding** between signal and harmonic sections

---

📌 Actuation logic and waveform generation firmware will be covered in `/software/harmonic_driver.py`  
📌 Tesla coil wiring diagrams and LCR tuning profiles will be defined in `/system_core/coil_harmonic_layout.md`

