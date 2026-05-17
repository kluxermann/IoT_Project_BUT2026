# 📍 BPC-IoT Project #6: GPS Tracker

> [!NOTE]
> **Brno University of Technology**  
> Faculty of Electrical Engineering and Communication  
> Department of Radio Electronics  
> Academic Year 2025/2026

---

## 👥 Team Members
- **Mykhailo Krasichkov** - Responsible for ... (to be filled)
- **[Name 2]** - Responsible for ...
- **[Name 3]** - Responsible for ...
- **[Name 4]** - Responsible for ...

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
*(To be completed based on final implementation choices)*

- **Microcontroller:** e.g., ESP32, STM32, Pico W, etc.
- **Wireless Tech:** e.g., LoRaWAN, NB-IoT, Sigfox, GSM, LTE-M *(chosen for broad CZ/SK coverage)*
- **Positioning:** GPS Module (e.g., NEO-6M)
- **Power Source:** Battery (e.g., Li-Ion 18650, Li-Po) paired with a power management IC.

---

## ⚙️ Technical Implementation

### 1. Protocols & Technologies
- **Wireless Standard:** [Add reasoning for the technology choice considering CZ/SK coverage].
- **Application Protocol:** [Add reasoning for protocol choice, e.g., MQTT for Thingsboard, CoAP, HTTP].

### 2. Logic & Communication Flow
- **Data Acquisition:** Parsing NMEA sentences from the GPS module.
- **Transmission:** Waking up from deep sleep, connecting to the network, and sending telemetry payloads.
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