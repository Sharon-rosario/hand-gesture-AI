# 🖐️ Hand Gesture Interaction System

A modular Python project that uses computer vision to detect hand gestures and power real-time interactive applications. Built with OpenCV and MediaPipe, this system enables touchless interaction for drawing, gaming, and future gesture-controlled modules.

---

## 🚀 Features

* Real-time hand tracking using webcam
* Gesture detection (index, pinch, etc.)
* Black canvas UI with hand skeleton visualization
* Modular architecture for adding new features
* Interactive modules (Drawing Board, Fruit Ninja - upcoming)

---

## 🏗️ Project Structure

```
hand-gesture-project/
│
├── app/                # Configs and utilities
├── core/               # Hand tracking & gesture logic
├── ui/                 # Rendering and canvas
├── modules/            # Interactive modules (games/tools)
├── assets/             # Images, sounds
├── tests/              # Unit tests
│
├── main.py             # Entry point
├── requirements.txt    # Dependencies
├── project_context.md  # Vision and roadmap
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```
git clone https://github.com/Sharon-rosario/hand-gesture-AI
cd hand-gesture-project
```

### 2. Create virtual environment

```
python -m venv venv
```

### 3. Activate environment

**Windows:**

```
venv\Scripts\activate
```

**Mac/Linux:**

```
source venv/bin/activate
```

### 4. Install dependencies

```
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the application:

```
python main.py
```

### Controls (Phase 1)

* Show your hand to the webcam
* Track finger movement on screen
* Index finger used as primary pointer

---

## 🧠 Architecture

The system follows a modular pipeline:

```
Camera → HandTracker → GestureDetector → Module → UI
```

* **HandTracker**: Detects and returns hand landmarks
* **GestureDetector**: Interprets gestures (pinch, point, etc.)
* **Modules**: Feature-specific logic (drawing, games)
* **UI**: Renders output on screen

---

## 🎯 Roadmap

### Phase 1 (Foundation)

* Stable hand tracking
* Gesture detection
* Skeleton rendering on black canvas

### Phase 2 (Interactive Modules)

* 🎨 Drawing Board (draw, move, erase)
* 🍉 Fruit Ninja (slice with index finger)

### Future Ideas

* Virtual mouse
* Gesture shortcuts
* Multi-hand interactions
* AR-style UI

---

## 🧩 Modules

Each feature is designed as a plug-and-play module:

* `drawing_board.py`
* `fruit_ninja.py`

You can extend the system by adding new modules inside the `modules/` folder.

---

## 🛠️ Tech Stack

* Python
* OpenCV
* MediaPipe
* NumPy
* Pygame (for future enhancements)

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 💡 Inspiration

Built as a weekend project to explore gesture-based interaction and modular real-time systems using computer vision.

---

## ✨ Author

Created with curiosity and experimentation.
