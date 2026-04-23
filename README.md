# Finger_Cursor
AI-powered gesture control for Windows/Mac/Linux. Uses computer vision to enable single-pinch clicking, double-pinch right-clicking, and long-pinch dragging with built-in jitter smoothing.

### Project Description
# 🖐️ Artificial Mouse: AI-Powered Gesture Control

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-00C7B7?logo=google&logoColor=white)](https://mediapipe.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Artificial Mouse** is a sophisticated computer vision tool that enables touchless human-computer interaction. By leveraging MediaPipe's high-fidelity hand tracking and PyAutoGUI's automation capabilities, this project transforms a standard webcam into a spatial input device.

## ✨ Key Capabilities

### 🖱️ Seamless Navigation
* **Precision Tracking:** Uses a "Magic Box" sensitivity area to map finger movements to screen coordinates with linear interpolation.
* **Smoothened Motion:** Implements a weighted-average algorithm to eliminate cursor jitter, providing a fluid user experience.

### 🖖 Intuitive Gestures
* **Single Pinch:** Briefly join the thumb and index finger for a standard **Left Click**.
* **Long Pinch (Drag & Drop):** Holding a pinch for more than `0.3s` triggers a `mouseDown` event, allowing for window dragging and file movement.
* **Double Pinch (Right Click):** Rapidly pinching twice within a `0.4s` window executes a **Right Click**.

---

## 🚀 Getting Started

### Prerequisites
Ensure you have Python 3.8+ installed. You will need a functioning webcam and a desktop environment that supports automation.

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/Arjunren/Finger_Cursor.git](https://github.com/yourusername/artificial-mouse.git)
   cd artificial-mouse
   ```

2. Install the required dependencies:
   ```bash
   pip install opencv-python mediapipe pyautogui numpy
   ```

3. Run the application:
   ```bash
   python finger.py
   ```
---

## ⚙️ Configuration

The system is designed to be highly configurable via the constants at the top of `finger.py`. These parameters allow you to tune the sensitivity and timing to match your hardware and lighting conditions.

| Constant | Description | Default Value |
| :--- | :--- | :--- |
| `frame_R` | The "Magic Box" size. Higher values increase cursor sensitivity by reducing the active tracking area. | `150` |
| `smoothening` | Reduces cursor jitter. Higher values make the movement "heavier" and smoother. | `5` |
| `PINCH_THRESH` | The pixel distance threshold between fingers to trigger a pinch event. | `30` |
| `HOLD_DELAY` | Time (in seconds) required to hold a pinch to activate the "Hold Click/Drag" state. | `0.3s` |
| `DOUBLE_CLICK_DELAY` | Time window (in seconds) to detect a double pinch for a Right Click. | `0.4s` |

---

## 🧪 Technical Implementation

The core engine utilizes **MediaPipe Hands** to identify 21 3D hand landmarks in real-time. The system specifically monitors:
* **Landmark 8 (Index Tip):** Used for primary cursor positioning and movement.
* **Landmark 4 (Thumb Tip):** Used in conjunction with the index tip to calculate Euclidean distance for gesture triggers.

The software employs a state machine to track the duration and frequency of "pinch" events, enabling the distinction between simple clicks, sustained drags, and secondary clicks.
