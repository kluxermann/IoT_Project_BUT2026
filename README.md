# 📍 BPC-IoT Project #6: GPS Tracker

> [!NOTE]
> **Brno University of Technology**  
> Faculty of Electrical Engineering and Communication  
> Department of Radio Electronics  
> Academic Year 2025/2026

---

## 👥 Team Members
- **Mykhailo Krasichkov** - 256512
- **Tomáš Běčák** - 256450
- **Andrej Balajka** - 256719
- **Martin Mikeš** - 256779

---

## 📝 Project Overview
This project focuses on the development of a **GPS Tracker** designed for monitoring vehicles and shipments across the Czech and Slovak Republics. A critical requirement is that the device must operate **completely independently** of the vehicle's internal power grid.

### 🎯 Core Objectives
- ⏱️ **Interval Reporting:** The device defaults to transmitting its location every **30 minutes**.
- 🚨 **Theft/Emergency Mode:** Operators can remotely adjust the transmission interval down to **1 minute** if theft is suspected.
- 📡 **Telemetry Dashboard:** Live location tracking and data visualization handled via **Thingsboard**.
- 🔋 **Independent Power & Efficiency:** Relies entirely on an external battery pack with implemented low-power (sleep) modes to maximize lifespan.

---

## 🔌 Hardware & Wireless Stack

- **Microcontroller:** MicroPython compatible board (e.g., Raspberry Pi Pico / ESP32).
- **Wireless Tech:** Quectel BG77 LPWA module (LTE Cat M1 / NB-IoT via Vodafone network).
- **Positioning:** Integrated GNSS on the BG77 module.
- **Power Source:** Battery (e.g., Li-Ion 18650, Li-Po) paired with a power management IC.

---

## ⚙️ Technical Implementation

### 1. Protocols & Technologies
- **Wireless Standard:** LTE-M / NB-IoT (Vodafone IoT) chosen for robust low-power wide-area coverage across CZ/SK.
- **Application Protocol:** CoAP over UDP for efficient, low-overhead communication with Thingsboard.

### 2. Logic & Communication Flow
- **Data Acquisition:** Utilizing AT commands (`AT+QGPSLOC`) to retrieve coordinates from the BG77 module. Includes a fallback mechanism generating coordinates around Brno if the GPS fix fails.
- **Transmission:** Establishing a UDP socket and sending CoAP telemetry packets containing JSON location data.
- **Remote Configuration:** Receiving downlink commands from Thingsboard to update the tracking interval dynamically.

### 3. Power Management
> [!TIP]
> A major part of the evaluation involves power consumption analysis.
- Measure active, idle, and deep-sleep currents using a laboratory probe.
- Calculate expected battery life for standard tracking (30 min) vs. theft tracking (1 min).

---

## 📊 Thingsboard Dashboard
*(Insert screenshots of the working dashboard here)*
- 🗺️ Map widget showing the current position and historical path.
- 🎛️ Dashboard widget to adjust the tracking interval remotely.
- 📈 Battery voltage/percentage telemetry charts.

---

## ✅ Project Deliverables Checklist
- [ ] **Technical Documentation** (Justification of hardware, protocols, and power source).
- [ ] **Power Consumption Analysis** (Calculations showing how the interval affects battery life).
- [ ] **Source Code** (The final firmware for the tracker).
- [ ] **Functional Demo** (Live demonstration of tracking and Thingsboard integration).