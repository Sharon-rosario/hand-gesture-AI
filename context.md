# 🖐️ Hand Gesture Detection System (Modular Build)

## 📁 Current Project Structure
```
hand-gesture-AI/
├── app/
│   ├── __init__.py
│   ├── config.py         # App-wide settings
│   ├── menu.py           # Main module selector UI
│   └── utils.py          # Helper functions
├── core/
│   ├── __init__.py
│   ├── gesture_detector.py # Finger/gesture logic (Pinch, Index Up, etc.)
│   └── hand_tracker.py     # MediaPipe wrapper for landmark extraction
├── modules/
│   ├── __init__.py
│   ├── base_module.py      # Abstract base class for modules
│   ├── drawing_board.py    # Drawing, Color select, Erase, Stability Buffers
│   └── shape_builder.py    # (New) Geometry modes using two-hand stretching
├── ui/
│   ├── __init__.py
│   └── canvas.py           # Prettier UI boxes, Status bar, Window management
├── main.py                 # App entry & State management
├── requirements.txt        # OpenCV, MediaPipe, NumPy
└── README.md
```

## 🚀 Key Achievements
- **Phase 1 Complete**: Reliable hand tracking + skeleton rendering on responsive black canvas.
- **Phase 2 In-Progress (Drawing Board)**: 
  - Point-to-draw (Index finger up trigger).
  - Stability buffer to solve flickering.
  - Multi-color palette and Eraser mode.
  - Smooth line rendering.

## 🧱 Module 3 (Geometry / Shapes) - Upcoming
- **Goal**: Create perfect shapes (Square, Circle, Rectangle).
- **Control**: Use two hands (Thumb + Index pinch on both) to "drag" and define shape dimensions.

## 🛠️ Tech Stack & Dependencies
- **MediaPipe**: Using Legacy Hands solutions for skeletal data.
- **OpenCV**: UI rendering, line drawing, window management.
- **NumPy**: Fast canvas manipulations.

## 🧭 Roadmap & Vision
1. **Fruit Ninja**: Real-time collision detection for slicing.
2. **Gesture Mouse**: Control Windows cursor with gestures.
3. **Module Inter-switch**: Seamless transition between active features via Pinch-selection.

---
*Updated: 2026-04-09 (Phase 2 Update)*
