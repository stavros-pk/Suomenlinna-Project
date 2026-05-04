# Development of an autonomous navigation system in the Finnish ROPAX vessel "Suomenlina"

> A functional prototype of an autonomous navigation and remote teleoperation system, implemented on a scale model of the Finnish ROPAX ferry **MS Suomenlinna II**.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Design Process](#design-process)
  - [Hull](#hull)
  - [Electronics Housing](#electronics-housing)
  - [Propulsion & Azipod Design](#propulsion--azipod-design)
  - [Integrated Components](#integrated-components)
- [System Architecture](#system-architecture)
- [Hardware](#hardware)
- [Software](#software)
  - [Entry Point](#entry-point)
  - [Fuzzy Logic Heading Controller](#fuzzy-logic-heading-controller)
  - [Sensor Drivers](#sensor-drivers)
  - [Actuation](#actuation)
  - [Utilities](#utilities)
  - [Dependencies](#dependencies)
- [Data Logging](#data-logging)
- [Getting Started](#getting-started)
- [Remote Teleoperation Dashboard](#remote-teleoperation-dashboard)
- [Project Status](#project-status)
- [Future Work](#future-work)
- [License](#license)

---

## Overview

This project explores the development of an autonomous navigation system for a small-scale physical model of the **MS Suomenlinna II**, a real-world ROPAX (Roll-On/Roll-Off Passenger) ferry operating in Helsinki, Finland.

The goal is to simulate key navigation behaviours found in modern maritime autonomous surface ships (MASS), including heading control and remote monitoring — all running on embedded hardware using **MicroPython**.

> Colision avoidance will be implemented on a future project.

This is a personal side project driven by an interest in autonomous systems, embedded engineering, and maritime robotics.

---

## Features

- **Heading Control** — Closed-loop heading stabilisation using IMU sensor feedback and a control algorithm to maintain or follow a target bearing
- **Remote Teleoperation** — Full remote control and live monitoring via an [Adafruit IO](https://io.adafruit.com/) cloud dashboard accessible from any browser or mobile device
- **Sensor Integration** — Ultrasonic distance sensors and an IMU (Inertial Measurement Unit) for situational awareness and orientation tracking
- **MicroPython Stack** — Entirely written in MicroPython, running on a Raspberry Pi microcontroller platform

---

## Design Process

The physical model went through a structured multi-stage design process covering the hull, electronics enclosure, propulsion system, and sensor/actuator integration — all modelled in **[Onshape](https://www.onshape.com/)**, a cloud-based parametric CAD platform.

---

### Hull

The hull design was directly inspired by the **MS Suomenlinna II**, the real passenger ferry serving the Helsinki archipelago.

<div align="center">
<table>
  <tr>
    <td align="center"><img width="275" height="183" alt="image" src="https://github.com/user-attachments/assets/18cea3b3-703b-467f-952e-0f400f40100e" /></td>
    <td align="center"><img width="275" height="183" alt="image" src="https://github.com/user-attachments/assets/e1c81543-1377-4b11-8a97-3321345f9a8b" /></td>
  </tr>
  <tr>
    <td colspan="2" align="center"><b>MS Suomenlinna II ROPAX Ferry</b></td>
  </tr>
</table>
</div>

The 3D model was carefully dimensioned to accommodate all desired internal components while maintaining a realistic hull form and waterline. Buoyancy, weight distribution, and internal volume for electronics were key constraints driving the design decisions.

<div align="center">
<table>
  <tr>
    <td align="center"><img width="1920" height="908" alt="Screenshot (65)" src="https://github.com/user-attachments/assets/3b61d4fd-9dd6-4665-af12-dec3e1948ac6" /></td>
    <td align="center"><img width="525" height="394" alt="image" src="https://github.com/user-attachments/assets/90862220-67b6-4daa-a700-b22d1d99fd35" />
</td>
  </tr>
  <tr>
    <td colspan="2" align="center"><b>3D CAD Model</b></td>
  </tr>
</table>
</div>

---

### Electronics Housing

A dedicated electronics enclosure was designed and integrated into the hull to keep all wiring and components organised, accessible, and protected from water ingress.

Key design goals for the housing were:
- Clean and manageable routing of connections between components
- Easy physical access for maintenance and iteration
- Secure mounting to prevent movement during operation

<div align="center">
<table>
  <tr>
    <td align="center"><img width="764" height="306" alt="image" src="https://github.com/user-attachments/assets/c9f0f137-e5f5-4f8e-97a2-c88e25574305" />
</td>
  </tr>
  <tr>
    <td colspan="2" align="center"><b>General Arrangment of the Model</b></td>
  </tr>
</table>
</div>

---

### Propulsion & Azipod Design

The propulsion system was one of the most technically challenging aspects of the build, owing to the complexity of the azipod configuration, the limited availability of off-the-shelf components at this scale, and the tight geometric constraints of the model.

The vessel uses a **dual azipod configuration** — one pod mounted at the stern and one at the bow — mirroring the arrangement found on modern azipod-driven vessels. The design process involved three key engineering challenges:

**1. Watertight Installation**
The first priority was ensuring each pod's drive shaft penetrated the hull without allowing water ingress. A sealing solution was designed to maintain a watertight barrier at the hull interface while still permitting free rotation of the shaft.

**2. Independent Pod Orientation**
Each azipod needed to rotate independently to allow omnidirectional thrust vectoring. This required designing a pivot mechanism that could be actuated by a servo motor while remaining compact enough to fit within the model's geometry.

**3. Motor-to-Propeller Coupling**
Connecting the drive motor to the propeller at this small scale — while maintaining alignment and minimising friction — required careful tolerancing in the CAD model and iteration on the physical assembly.

<div align="center">
<table>
  <tr>
    <td align="center"><img width="1146" height="802" alt="Screenshot (66)" src="https://github.com/user-attachments/assets/ccf5a1de-aff8-49fc-a095-a8bf18e1f4bd" /></td>
  </tr>
  <tr>
    <td colspan="2" align="center"><b>General Arrangment of the Model</b></td>
  </tr>
</table>
</div>

---

### Integrated Components

To enable full actuation and situational awareness during a mission, the following sensors and actuators were integrated into the model:

| Type | Component | Purpose |
|---|---|---|
| **Sensor** | Accelerometer | Measure linear acceleration and detect motion |
| **Sensor** | Magnetometer | Provide heading reference for navigation |
| **Sensor** | GPS Module | Determine absolute position during a mission |
| **Actuator** | Servo Motors | Azipod orientation (thrust vectoring) |
| **Actuator** | DC Motors | Propeller drive for each azipod |

The integration of these components required careful placement within the hull to maintain balance, minimise electromagnetic interference between sensors, and keep cable runs manageable.

---

## System Architecture

```
<div align="center">
<table>
  <tr>
    <td align="center"><img width="811" height="412" alt="Diagrams-Hardware Schematic drawio" src="https://github.com/user-attachments/assets/d02c00e3-8ca2-40f2-a8e3-23542165f015" />
</td>
  </tr>
  <tr>
    <td colspan="2" align="center"><b>Hardware Schematic</b></td>
  </tr>
</table>
</div>
```

---

## Hardware

| Component | Details |
|---|---|
| **Microcontroller** | Raspberry Pi Pico (CircuitPython / MicroPython) |
| **Magnetometer** | LSM303DLH — compass heading via I²C (GP2/GP3) |
| **IMU / Gyroscope** | MPU6050 — angular velocity via I²C (GP0/GP1) |
| **GPS Module** | UART GPS — position fix via UART (GP8/GP9) |
| **Motor Driver** | L293D — DC motor H-bridge driver |
| **Azipod Servos** | 2× servo motors — PWM via GP16 & GP17 |
| **DC Motors** | 2× DC motors — PWM via GP12/GP13 through L293D |


---

## Software

The entire software stack is written in **MicroPython** (CircuitPython-compatible), running on the Raspberry Pi Pico. The codebase is modular, with each file handling a distinct subsystem.

### Entry Point

#### `code.py`
The main control loop. Initialises all subsystems, connects to Wi-Fi and the Adafruit IO MQTT broker, then enters the main loop which handles two operating modes received from the dashboard:

**AUTO mode** — Autonomous heading control:
1. Reads current heading from the magnetometer and subtracts the target angle to compute heading error
2. Reads angular velocity from the MPU6050 gyroscope
3. Selects the active controller — either the **Fuzzy Logic** controller (`FUZ`) or the **PD controller** (`PD`) — based on a dashboard feed
4. Clamps the rudder command to ±60° and drives both azipod servos
5. Controls motor thrust based on the dashboard `THRUST` feed value
6. Provides visual LED feedback — green when within ±5° of target, red otherwise
7. Logs all data (time, heading error, rudder angle, yaw rate, controller type) to an SD card CSV file

**MAN mode** — Remote manual control:
1. Reads rudder angle and thrust commands directly from the dashboard feeds
2. Passes commands to servos and motors without any autonomous processing

Additional features in the main loop:
- **Wi-Fi auto-reconnect** on startup with retry loop
- **MQTT remote power-off** — a dedicated `POWEROFF` feed can cleanly shut down the system, centering servos and stopping motors before termination
- **Selectable controller** — switch between Fuzzy and PD control mid-mission from the dashboard

---

### Fuzzy Logic Heading Controller

The heading controller is the core of the autonomous navigation system. Rather than a conventional PID controller, a **Mamdani-type fuzzy logic controller** was designed and implemented from scratch.

#### `fuzzy_rossi_ang.py` — Full Fuzzy Controller (Heading + Angular Velocity)
The primary controller. Takes two inputs — **heading error** (degrees) and **angular velocity** (°/s) — and outputs a **rudder angle** command (degrees).

**Fuzzification** — inputs are mapped onto overlapping fuzzy sets using membership functions:

| Heading Error Sets | Angular Velocity Sets |
|---|---|
| HHL (Hard Hard Left) | HL (Hard Left) |
| HL (Hard Left) | ML (Medium Left) |
| ML (Medium Left) | SL (Soft Left) |
| SL (Soft Left) | ZE (Zero) |
| ZE (Zero) | SR (Soft Right) |
| SR (Soft Right) | MR (Medium Right) |
| MR (Medium Right) | HR (Hard Right) |
| HR (Hard Right) | |
| HHR (Hard Hard Right) | |

Membership function types used: triangular, trapezoidal, open-left, and open-right — implemented as static methods on the `fuzzy_controller` class.

**Rule Base** — a 9×7 rule matrix maps every combination of heading error and angular velocity fuzzy set to a rudder output fuzzy set. Rules are evaluated using the `min` operator (AND).

**Defuzzification** — the crisp rudder angle output is computed via the **centre of area (centroid)** method, calculating the weighted area under each output membership function.

#### `fuzzy_rossi.py` — Single-Input Fuzzy Controller (Heading Only)
An earlier version of the fuzzy controller using only heading error as input. Kept for reference and comparison.

---

### Sensor Drivers

#### `mag_heading.py` — Magnetometer Heading
Wraps the **LSM303DLH** magnetometer (via I²C on GP2/GP3). Uses `math.atan2` on the X/Y magnetic field components to compute a compass heading in degrees (±180°).

```python
# I²C pins: SDA → GP2, SCL → GP3
i2c = busio.I2C(board.GP3, board.GP2)
```

#### `mpu6050.py` — Gyroscope (Angular Velocity)
Wraps the **MPU6050** IMU (via I²C on GP0/GP1). Reads the Z-axis gyroscope and converts from rad/s to °/s. Averages 4 consecutive readings per call to reduce noise.

```python
# I²C pins: SDA → GP0, SCL → GP1
i2c = busio.I2C(board.GP1, board.GP0)
```

#### `gps.py` — GPS Module
Reads NMEA sentences from a GPS module over UART (TX → GP8, RX → GP9) at 9600 baud. Parses position data for absolute localisation during a mission.

```python
# UART pins: TX → GP8, RX → GP9
gps_module = busio.UART(board.GP8, board.GP9, baudrate=9600, timeout=10)
```

---

### Actuation

#### `servo.py` — Azipod Servo Control
Controls **two servo motors** (one per azipod) via PWM on GP16 and GP17 at 50 Hz. Accepts a rudder angle from the fuzzy controller and translates it into a servo position (offset by +90° to centre the range).

```python
# PWM pins: Azipod 1 → GP16, Azipod 2 → GP17
self.pwm1 = pwmio.PWMOut(board.GP16, frequency=50)
self.pwm2 = pwmio.PWMOut(board.GP17, frequency=50)
```

#### `motor_test.py` / `pwm_motor_test.py` — DC Motor Tests
Test scripts for the **L293D** motor driver. `motor_test.py` uses simple digital on/off control; `pwm_motor_test.py` uses PWM (GP12/GP13) for variable speed control with duty cycle ramping.

---

### Utilities

#### `angular_vel.py` — Angular Velocity (Heading Differencing)
An alternative angular velocity estimator that computes heading rate of change by differencing two consecutive magnetometer readings over elapsed time. Used in earlier iterations before the MPU6050 gyroscope was integrated.

---

### Dependencies

| Library | Source | Used In |
|---|---|---|
| `adafruit_lsm303dlh_mag` | Adafruit CircuitPython | `mag_heading.py` |
| `adafruit_mpu6050` | Adafruit CircuitPython | `mpu6050.py` |
| `adafruit_gps` | Adafruit CircuitPython | `gps.py` |
| `adafruit_motor` | Adafruit CircuitPython | `servo.py` |
| `ulab.numpy` | MicroPython ulab | `fuzzy_rossi*.py` |

Install Adafruit CircuitPython libraries via the [Adafruit CircuitPython Bundle](https://circuitpython.org/libraries).

---

## Data Logging

Mission data is logged in real time to a **MicroSD card** connected to the Raspberry Pi Pico via SPI. This allows post-mission analysis of the vessel's behaviour, controller performance comparison, and tuning of control parameters without relying on a live connection.

### Hardware Interface

The SD card module communicates over SPI using the following pin assignment:

| SPI Signal | Pico GPIO |
|---|---|
| CS (Chip Select) | GP5 |
| SCK (Clock) | GP6 |
| MOSI (TX) | GP7 |
| MISO (RX) | GP4 |

The SD card is mounted at `/sd` using CircuitPython's `storage` and `adafruit_sdcard` libraries:

```python
storage.mount(
    storage.VfsFat(adafruit_sdcard.SDCard(io.SPI(SCK, MOSI, MISO),
    digitalio.DigitalInOut(CS))), "/sd"
)
```

### Log File Format

Each time the system enters **AUTO mode**, a new numbered CSV file is created on the SD card (`data1.csv`, `data2.csv`, etc.), ensuring no previous run's data is overwritten.

Each row records a single control loop iteration with the following fields:

| Column | Description |
|---|---|
| `Time` | Elapsed time since AUTO mode was activated (seconds) |
| `Heading` | Heading error relative to target (degrees) |
| `Rudder` | Commanded rudder/azipod angle (degrees) |
| `Yaw_Rate` | Angular velocity from MPU6050 gyroscope (°/s) |
| `Controller` | Active controller at the time of the entry (`FUZ` or `PD`) |

Example log output:
```
Time Heading Rudder Yaw_Rate Controller
0.21 -34.5 18.7 -2.3 FUZ
0.32 -31.2 16.4 -1.8 FUZ
0.43 -27.8 14.1 -1.4 FUZ
...
```

### Use Cases

The logged data enables direct **comparison between the Fuzzy Logic and PD controllers** across identical test runs — heading error convergence rate, overshoot, steady-state accuracy, and response to disturbances can all be analysed and plotted from the CSV files offline.

---

## Getting Started

### Prerequisites

- Raspberry Pi with MicroPython firmware flashed
- [Adafruit IO](https://io.adafruit.com/) account (free tier is sufficient)
- Wi-Fi network

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/stavros-pk/Autonomous-ROPAX.git
   cd Autonomous-ROPAX
   ```

2. **Configure credentials**

   Create a `settings.toml` file in the root of the Pico with your network and Adafruit IO credentials (CircuitPython reads this automatically via `os.getenv()`):
   ```toml
   WIFI_SSID = "your_wifi_ssid"
   WIFI_PASSWORD = "your_wifi_password"
   AIO_USERNAME = "your_adafruit_io_username"
   AIO_KEY = "your_adafruit_io_key"
   BROKER = "io.adafruit.com"
   PORT = "8883"
   ```

3. **Upload files to the board**

   Use a tool like [Thonny IDE](https://thonny.org/) to upload all `.py` files to the microcontroller.

4. **Run**
   ```bash
   # Via Thonny: open code.py and press Run
   ```

---

## Remote Teleoperation Dashboard

The vessel is controlled and monitored through an **Adafruit IO** dashboard. The dashboard provides:

- **Control feeds** — Set heading target, throttle, and operating mode (manual / autonomous)
- **Telemetry feeds** — Live display of current heading, sensor readings, and system status

To set up your own dashboard, create the following feeds on Adafruit IO and add them to your `settings.toml` configuration file:

| Feed Name | Direction | Description |
|---|---|---|
| `Mode` | → Vessel | Operating mode: `AUTO` (autonomous) or `MAN` (manual) |
| `THRUST` | → Vessel | Motor thrust level (integer) |
| `STEER` | → Vessel | Manual rudder angle override (degrees, MAN mode only) |
| `TARGET` | → Vessel | Desired heading target (degrees, AUTO mode only) |
| `CONTROLLER` | → Vessel | Active controller: `FUZ` (fuzzy) or `PD` (PD controller) |
| `POWEROFF` | → Vessel | Send `1` to safely shut down the system |
| `RUDDERANGLE` | ← Vessel | Live rudder angle telemetry (degrees) |
| `STREAMDATA` | ← Vessel | Live heading error telemetry (degrees) |

---

## Project Status

**✅ Functional Prototype**

The core systems — heading control, sensor integration, and remote teleoperation — are operational on the physical model. The vessel can be commanded remotely and autonomously maintains a set heading.

---

## Future Work

- [ ] **GPS-based waypoint navigation** — Follow a pre-programmed route using GPS coordinates
- [ ] **Collision avoidance** — Integrate ultrasonic readings into an autonomous stop/reroute behaviour
- [ ] **Path planning** — Basic A* or potential field navigation in constrained waterways
- [ ] **Improved UI** — Custom web dashboard to replace Adafruit IO

---

## License

This project is for educational and personal development purposes.  
© Stavros — feel free to reach out with questions or collaboration ideas.
