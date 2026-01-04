# 🏎️ Active Suspension HIL Simulation (Python + CODESYS)

![System Architecture](https://img.shields.io/badge/Architecture-HIL-blue) ![Protocol](https://img.shields.io/badge/Protocol-Modbus%20TCP-green) ![Status](https://img.shields.io/badge/Status-Functional-brightgreen)

## 📖 Overview
This project is a **Hardware-in-the-Loop (HIL)** simulation designed to develop and test active suspension control algorithms. 

Instead of relying purely on software models, this system bridges the gap between **IT (Python Physics Engine)** and **OT (Industrial PLC)**. It simulates a "Quarter-Car Model" interacting with a bumpy road in real-time, while an industrial controller (CODESYS) actively regulates the suspension damping to maximize ride comfort.

## ⚙️ System Architecture

| Component | Technology | Responsibility |
|-----------|------------|----------------|
| **The Plant** | Python (Matplotlib) | Simulates vehicle physics, road disturbances (Sine/Random), and visualizes telemetry. |
| **The Controller** | CODESYS (IEC 61131-3) | Runs the P-Control loop to calculate counter-force based on sensor feedback. |
| **The Bridge** | Modbus TCP/IP | High-speed, low-latency (<20ms) data exchange between Plant and Controller. |

## 🚀 How It Works
1.  **Disturbance Generation:** The Python script generates a "Road Profile" consisting of sine waves and random noise (simulating potholes).
2.  **Sensor Feedback:** The car's vertical position is sent to the PLC via Modbus Holding Registers.
3.  **Control Logic:** The PLC compares the current position to the Setpoint (50% travel). It uses a Proportional (P) algorithm to calculate the necessary counter-force.
4.  **Actuation:** The force command is sent back to Python, which applies it to the physics model to counteract the bump.

## 📊 Results
The system demonstrates successful **Disturbance Rejection**.
* **Green Line:** Road Profile (High variance/Rough terrain).
* **Blue Line:** Chassis Position (Stabilized).

![Simulation Graph](result_graph.png)
*(Note: As seen above, the controller maintains chassis stability even during extreme road events.)*

## 🛠️ Prerequisites
* **Python 3.x**
    * `pymodbus`
    * `matplotlib`
* **CODESYS Development System V3.5** (or newer)
* **CODESYS Control Win V3** (SoftPLC Runtime)

## 💻 Installation & Usage

### 1. PLC Setup
1.  Open `PLC/ActiveSuspension.project` in CODESYS.
2.  Start the **CODESYS Control Win V3** runtime from the Windows SysTray.
3.  Login (`Alt+F8`) and Start (`F5`) the PLC.

### 2. Python Simulation
1.  Install dependencies:
    ```bash
    pip install pymodbus matplotlib
    ```
2.  Run the simulation:
    ```bash
    python Python/suspension_sim.py
    ```

## 📝 Key Learnings
* Implementation of **Closed-Loop Feedback Control** in an industrial environment.
* Interfacing **High-Level Languages (Python)** with **Real-Time Industrial Hardware**.
* Handling Modbus TCP/IP data serialization and latency management.
