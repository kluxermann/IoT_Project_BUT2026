# BPC-IoT Project #6: GPS Tracker

> **Brno University of Technology**  
> Faculty of Electrical Engineering and Communication  
> Department of Radio Electronics  
> Academic Year 2025/2026

---

## Team Members
- **Mykhailo Krasichkov** - 256512
- **Tomáš Běčák** - 256450
- **Andrej Balajka** - 256719
- **Martin Mikeš** - 256779

---

## Project Overview
This project focuses on the development of a GPS Tracker device designed for monitoring vehicles and shipments across both Czech and Slovak republic. The GPS Tracker device will operate in two modes: 
1. Normal mode 
2. Emergency mode

In normal mode, the device reports its location every 30 minutes. In case of theft, the operator will be able to remotely change the sending interval of reports at his own discretion down to a minimum of 1 minute. The location of the device will be visable on the ThingsBoard platform. A critical requirement is that the car's power grid cannot be used as power source.

### Core Objectives
-  **Interval Reporting:** The device defaults to transmitting its location every **30 minutes**.
-  **Theft/Emergency Mode:** Operators can remotely adjust the transmission interval down to **1 minute** if theft is suspected.
-  **Telemetry Dashboard:** Live location tracking and data visualization handled via **Thingsboard**.
-  **Independent Power & Efficiency:** Relies entirely on an external battery pack with implemented low-power modes to maximize lifespan.

---

##  Hardware & Wireless Stack

- **Microcontroller:** RP 2040.
- **Wireless Tech:** Quectel BG77 LPWA module (LTE Cat M1 / NB-IoT via Vodafone network).
- **Positioning:** Integrated GNSS on the BG77 module.
- **Power Source:** Battery 

---

##  Technical Implementation

### 1. Protocols & Technologies
As is in the nature of the project we will need to send data frequently, every 30 minutes and in case of theft every minute, so choosing technology that is not constrained by duty cycle and daily message caps is paramount. This leaves two options: LTE Cat M and NB-IoT. Since the device will be in motion, NB-IoT is not viable as it does not have defined handover. Therefore, LTE Cat M is the best choice. As for application protocol, we need to ensure confirmation of data reception while keeping minimal overhead, as LTE Cat M uses licensed spectrum keeping it financially viable is paramount. For these reasons CoAP with implemented acknowledgment is the most suitable option for this application as it uses UDP (which have only 8B header) so overhead rudction is achieved. 

**Used Technolgy:**
- **Wireless Standard:** LTE-M / NB-IoT (Vodafone IoT) chosen for robust low-power wide-area coverage across CZ/SK.
- **Application Protocol:** CoAP over UDP for efficient, low-overhead communication with Thingsboard.

### 2. Logic & Communication Flow
- **Data Acquisition:** Utilizing AT commands (`AT+QGPSLOC`) to retrieve coordinates from the BG77 module. Includes a fallback mechanism generating coordinates around Brno if the GPS fix fails.
- **Transmission:** Establishing a UDP socket and sending CoAP telemetry packets containing JSON location data.
- **Remote Configuration:** Receiving downlink commands from Thingsboard to update the tracking interval dynamically.

### 3. Power Management
- Measured active, idle, and deep-sleep currents using a laboratory probe.
I_active = 32 mA
I_sleep = 0,005 mA
t_active = 30 s
t_sleep = 1800 s
t_overall = 1830 s

- Expected battery life for standard tracking (30 min) vs. theft tracking (1 min).
-Battery: 4x SAFT LSH 20(LI-SOCl2) in parallel

-**Power consumtion 30 minutes**
I_avg_30_min = \frac{(I_{\text{active}} \cdot t_{\text{active}}) + (I_{\text{sleep}} \cdot t_{\text{sleep}})}{t_{\text{overall}}}
I_avg_30_min = \frac{969}{1830} = 0,53 mA
Battery_life_expectancy_hours = \frac{44200}{0,53} = 83396 hours
Battery_life_expectancy_days = \frac{83396}{24} = 3474,8 days
Battery_life_expectancy_years = \frac{3474,8}{365} = 9,52 years
-**Power consumption 1 minute**
I_avg_1_min = \frac{(I_{\text{active}} \cdot t_{\text{active}}) + (I_{\text{sleep}} \cdot t_{\text{sleep}})}{t_{\text{overall}}}
I_avg_1_min = \frac{(960 + 15)}{60} = 16,00 mA
Battery_life_expectancy_hours = \frac{44200}{16} = 2762,5 hours
Battery_life_expectancy_days = \frac{83396}{24} = 115,1 days

As we can see the change in trasmition interval will have huge impact on battery life expectancy. In case of 30 minutes interval the expected battery life is 3474,8 days or almost 10 years. In contrast if the transmition inerval is set to 1 minute the expected battery life is only 115,1 days which is 30 times less.   
---

##  Thingsboard Dashboard
*(Insert screenshots of the working dashboard here)*
-  Map widget showing the current position and historical path.
-  Dashboard widget to adjust the tracking interval remotely.
-  Battery voltage/percentage telemetry charts.
