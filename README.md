# VisionKey 🎯⌨️

## ✨ Overview

**VisionKey** is a computer vision-based virtual keyboard built with Python and OpenCV that lets you **type using just your hand gestures** — no physical keyboard required!

It uses real-time hand tracking to detect finger gestures and simulate key presses by interacting with a fully functional **QWERTY keyboard** rendered directly on the webcam feed.

---

## 🎥 Features

- 🖐️ **Gesture-based keypress** using index–thumb pinch
- 🔍 **Hand tracking** via MediaPipe
- 🔡 Full **QWERTY layout** with numbers, punctuations, and symbols
- 🟩 **Transparent key overlays** with real-time visual feedback
- 🎯 **Finger tip pointers** for better accuracy
- 🔄 Works across **Windows, macOS, and Linux**

---

## 🛠 Tech Stack

- 🐍 Python 3.7+
- 📸 OpenCV
- ✋ MediaPipe
- 🧰 cvzone

---

## 📦 Installation

```bash
git clone https://github.com/ArchitJ6/VisionKey.git
cd VisionKey
pip install -r requirements.txt
python main.py
```

---

## ✅ Requirements

- Webcam
- Python 3.7+
- A steady hand ✋🙂

---

## 📂 Project Structure

```
VisionKey/
├── LICENSE
├── main.py               # Main script to launch the keyboard
├── README.md             # Project documentation
└── requirements.txt      # Python dependencies
```

---

## 🧪 How It Works

1. Launch the script and allow camera access.
2. The virtual keyboard will appear centered in the camera feed.
3. Move your index finger to hover over a key.
4. Pinch your index finger and thumb together to "press" the key.
5. Typed text is shown in a preview window below the keyboard.

---

## 🙌 Acknowledgements

- [cvzone](https://github.com/cvzone/cvzone) for high-level OpenCV utilities
- [MediaPipe](https://github.com/google-ai-edge/mediapipe) by Google for powerful hand tracking

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 💡 Future Ideas

- Add Shift / CapsLock support
- Enable multi-language layout
- Integrate with text-to-speech
- Support swiping gestures for faster input