# 🖐️ Hand Gesture Detection Project (Weekend Build)

## 📁 Project Structure

```
hand-gesture-project/
│
├── .gitignore
├── README.md
├── requirements.txt
├── project_context.md
├── setup_env.sh
├── main.py
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── utils.py
│
├── core/
│   ├── __init__.py
│   ├── hand_tracker.py
│   ├── gesture_detector.py
│
├── ui/
│   ├── __init__.py
│   ├── canvas.py
│
├── modules/
│   ├── __init__.py
│   ├── base_module.py
│   ├── fruit_ninja.py
│   ├── drawing_board.py
│
├── assets/
│   ├── images/
│   ├── sounds/
│
└── tests/
    ├── __init__.py
    ├── test_hand_tracker.py
```

---

## ⚙️ requirements.txt

```
opencv-python
mediapipe
numpy
pygame
```

---

## 🚫 .gitignore

```
__pycache__/
*.pyc
*.pyo
*.pyd
.env
venv/
.env/
.DS_Store
.vscode/
.idea/
```

---

## ⚡ setup_env.sh

```
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate   # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🚀 main.py

```python
from core.hand_tracker import HandTracker
from ui.canvas import Canvas


def main():
    tracker = HandTracker()
    canvas = Canvas()

    while True:
        frame, landmarks = tracker.get_frame()
        canvas.draw(frame, landmarks)


if __name__ == "__main__":
    main()
```

---

## 🧠 core/hand_tracker.py

```python
import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None, None

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        landmarks = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks.append(hand_landmarks)

        return frame, landmarks
```

---

## 🎨 ui/canvas.py

```python
import cv2


class Canvas:
    def draw(self, frame, landmarks):
        if frame is None:
            return

        for hand in landmarks:
            for lm in hand.landmark:
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        cv2.imshow("Hand Gesture UI", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            exit()
```

---

## 🧩 modules/base_module.py

```python
class BaseModule:
    def update(self, landmarks):
        pass

    def render(self, frame):
        pass
```

---

## 🍉 modules/fruit_ninja.py (Phase 2)

```python
from modules.base_module import BaseModule


class FruitNinja(BaseModule):
    def update(self, landmarks):
        pass

    def render(self, frame):
        pass
```

---

## 🎨 modules/drawing_board.py (Phase 2)

```python
from modules.base_module import BaseModule


class DrawingBoard(BaseModule):
    def update(self, landmarks):
        pass

    def render(self, frame):
        pass
```

---

## 📝 project_context.md

```
# Project Context

## Vision
A fun, modular hand-gesture-based interaction system using a webcam.

## Phase 1 (Foundation)
- Build reliable hand tracking
- Render skeleton on black canvas
- Clean architecture for extensibility

## Phase 2 (Interactive Modules)
1. Fruit Ninja
   - Fruits spawn
   - Slice using index finger

2. Drawing Board
   - Draw with index finger
   - Move objects with pinch
   - Erase with open palm

## Future Ideas
- Virtual mouse
- Gesture-based shortcuts
- Mini games

## Design Philosophy
- Modular (plug-and-play modules)
- Real-time performance
- Clean separation (core, UI, modules)
```

---

## 🧭 Next Steps

1. Run setup_env.sh
2. Implement finger tracking utilities
3. Detect gestures (pinch, open palm, point)
4. Add module switching system
5. Improve UI (black canvas + skeleton overlay)

---

🔥 This is a strong base to expand into multiple interactive gesture-driven apps.
