# BPC-IoT Projekt #6: GPS Tracker

---

**Vysoké učení technické v Brně, Fakulta elektrotechniky a komunikačních technologií, Ústav radioelektroniky, 2025/2026**

---

## 👥 Členové týmu
 - Mykhailo Krasichkov - Odpovědný za ... (doplnit)
 - [Jméno 2] - Odpovědný za ...
 - [Jméno 3] - Odpovědný za ...
 - [Jméno 4] - Odpovědný za ...

## 📝 Popis projektu (Zadání)
Tento projekt realizuje **GPS Tracker** pro sledování a monitorování vozidel a zásilek v rámci České a Slovenské republiky. Zařízení funguje zcela nezávisle na napájecí soustavě vozidla.

**Hlavní požadavky:**
- **Pravidelné hlášení polohy:** Výchozí interval vysílání polohy je minimálně **30 minut**.
- **Režim krádeže:** Možnost vzdáleně změnit interval odesílání operátorem až na **1 minutu** v případě odcizení.
- **Zobrazení dat:** Vizualizace polohy na platformě **Thingsboard**.
- **Nezávislé napájení:** Zařízení nesmí být připojeno k napájení vozidla (nutnost vlastní baterie).
- **Úspora energie:** Implementace vhodných režimů úspory energie (Low-power modes).

## 🔌 Hardware a Technologie
*(Bude doplněno na základě zvoleného řešení)*
- **Vývojová deska:** např. ESP32, STM32, Pico W, případně jiná (obsahující zvolenou technologii).
- **Bezdrátová technologie:** např. LoRaWAN, NB-IoT, Sigfox, GSM, Bluetooth, Zigbee ... *(Zvoleno na základě požadavku celostátního pokrytí)*.
- **GPS Modul:** např. NEO-6M, ...
- **Napájení:** Zvolená baterie (např. Li-Ion 18650, Li-Pol) + obvod pro řízení spotřeby.

## ⚙️ Funkce systému a technické řešení
**1. Zvolená technologie a protokoly**
 - **Technologie:** [Doplnit zdůvodnění volby technologie s ohledem na pokrytí v ČR a SR].
 - **Transportní a aplikační protokol:** [Doplnit zdůvodnění volby protokolu, např. MQTT, CoAP, HTTP].

**2. Měření polohy a komunikace**
 - Získávání souřadnic z GPS modulu.
 - Odesílání dat na server v definovaných intervalech.
 - Příjem příkazů z platformy pro změnu intervalu (vzdálená správa intervalu).

**3. Napájení a spotřeba energie**
 - Měření proudové spotřeby zařízení na proudové sondě v laboratoři.
 - Diskuse nad životností zařízení při standardním intervalu (30 min) a při režimu krádeže (1 min).
 - Implementované úsporné režimy (Deep sleep).

## 📊 Vizualizace (Thingsboard)
*(Zde budou vloženy screenshoty z dashboardu Thingsboard)*
- Zobrazení mapy s polohou vozidla/zboží.
- Ovládací prvek pro operátora pro změnu intervalu odesílání dat.

## 🔍 Požadované výstupy projektu (Checklist)
📂 **Hlavní soubory a dokumentace**
 - [ ] **Popis technického řešení** (Zdůvodnění technologie, protokolů, napájení).
 - [ ] **Analýza spotřeby** (Jak se promítne změna intervalu do celkové spotřeby a životnosti baterie).
 - [ ] **Zdrojové kódy** k realizaci GPS Trackeru.
 - [ ] **Ukázka funkčnosti** na platformě Thingsboard.

---
---

**Brno University of Technology, Faculty of Electrical Engineering and Communication, Department of Radio Electronics, 2025/2026**

---

## 👥 Team Members
 - Mykhailo Krasichkov - Responsible for ... (to be filled)
 - [Name 2] - Responsible for ...
 - [Name 3] - Responsible for ...
 - [Name 4] - Responsible for ...

## 📝 Project Description (Task)
This project implements a **GPS Tracker** for tracking and monitoring vehicles and shipments within the Czech and Slovak Republics. The device operates entirely independently of the vehicle's power system.

**Main requirements:**
- **Regular position reporting:** Default transmission interval is at least **30 minutes**.
- **Theft mode:** Option to remotely change the transmission interval by the operator down to **1 minute** in case of theft.
- **Data visualization:** Position displayed on the **Thingsboard** platform.
- **Independent power supply:** The device must not be connected to the vehicle's power system (requires its own battery).
- **Power saving:** Implementation of appropriate power saving modes.

## 🔌 Hardware and Technology
*(To be filled based on the chosen solution)*
- **Development board:** e.g., ESP32, STM32, Pico W, or other (must include the chosen technology).
- **Wireless technology:** e.g., LoRaWAN, NB-IoT, Sigfox, GSM, Bluetooth, Zigbee ... *(Chosen based on the nationwide coverage requirement)*.
- **GPS Module:** e.g., NEO-6M, ...
- **Power supply:** Chosen battery (e.g., Li-Ion 18650, Li-Pol) + power management circuit.

## ⚙️ System Functionality and Technical Solution
**1. Chosen Technology and Protocols**
 - **Technology:** [Add reasoning for the technology choice considering CZ/SK coverage].
 - **Transport and application protocol:** [Add reasoning for the protocol choice, e.g., MQTT, CoAP, HTTP].

**2. Position Measurement and Communication**
 - Acquiring coordinates from the GPS module.
 - Sending data to the server at defined intervals.
 - Receiving commands from the platform to change the interval (remote interval management).

**3. Power Supply and Energy Consumption**
 - Measurement of device current consumption using a current probe in the lab.
 - Discussion on device battery life under the standard interval (30 min) and theft mode (1 min).
 - Implemented power saving modes (Deep sleep).

## 📊 Visualization (Thingsboard)
*(Screenshots from the Thingsboard dashboard will be placed here)*
- Map display showing the vehicle/goods position.
- Control element for the operator to change the data transmission interval.

## 🔍 Required Project Outputs (Checklist)
📂 **Main Files and Documentation**
 - [ ] **Technical solution description** (Reasoning for technology, protocols, power supply).
 - [ ] **Power consumption analysis** (How interval changes affect overall consumption and battery life).
 - [ ] **Source codes** for the implementation of the GPS Tracker.
 - [ ] **Demonstration of functionality** on the Thingsboard platform.