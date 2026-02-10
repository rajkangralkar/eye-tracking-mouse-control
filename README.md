# eye-tracking-mouse-control
# Eye Controlled Mouse using Computer Vision 👁️🖱️

A basic real-time **eye-tracking based mouse control system** built using **Python, OpenCV, MediaPipe Face Mesh, and PyAutoGUI**.  
The project allows users to control mouse movement using eye gaze direction and perform mouse clicks using blink detection.

This project is intended as a **learning and foundational implementation** of vision-based human–computer interaction.

---

## 🚀 Features
- Real-time eye tracking using MediaPipe Face Mesh
- Cursor movement based on iris position
- Vertical and horizontal gaze-based control
- Single blink → Mouse click
- Double blink → Mouse double-click
- Works with mobile IP webcam or external camera
- Visual feedback for iris and eye center

---

## 🛠️ Tech Stack
- Python 3.x
- OpenCV
- MediaPipe
- PyAutoGUI
- IP Webcam (Mobile Camera)

---

## 📷 How It Works
1. Face landmarks are detected using MediaPipe Face Mesh.
2. Iris positions from both eyes are averaged.
3. Gaze direction is calculated relative to eye center.
4. Mouse cursor moves accordingly.
5. Blink detection triggers mouse clicks.

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/rajkangralkar/eye-tracking-mouse-control.git
cd eye-controlled-mouse
