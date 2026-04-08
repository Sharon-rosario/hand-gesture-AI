import cv2
import numpy as np
from modules.base_module import BaseModule
from core.gesture_detector import GestureDetector

class DrawingBoard(BaseModule):
    def __init__(self):
        super().__init__()
        self.detector = GestureDetector()
        self.points = [] # List of list of points (each list is a stroke)
        self.current_stroke = []
        self.colors = [(255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0)] # White, Red, Green, Blue
        self.current_color_idx = 0
        self.brush_size = 5
        self.eraser_size = 50
        
        # UI Button areas (x1, y1, x2, y2)
        self.buttons = {
            "Color 1": (50, 10, 150, 60),
            "Color 2": (170, 10, 270, 60),
            "Color 3": (290, 10, 390, 60),
            "Color 4": (410, 10, 510, 60),
            "Eraser": (530, 10, 630, 60),
            "Back": (10, 400, 100, 450)
        }
        
    def update(self, landmarks, frame_shape):
        h, w, _ = frame_shape
        if not landmarks:
            if self.current_stroke:
                self.points.append((self.current_stroke, self.colors[self.current_color_idx]))
                self.current_stroke = []
            return None

        # Check for pinch (click/draw)
        is_drawing = self.detector.is_pinch(landmarks)
        index_tip = self.detector.get_index_finger_tip(landmarks)
        
        if index_tip:
            cx, cy = int(index_tip.x * w), int(index_tip.y * h)
            
            # Check for button clicks
            if is_drawing:
                # Color selection
                if 10 < cy < 60:
                    if 50 < cx < 150: self.current_color_idx = 0
                    elif 170 < cx < 270: self.current_color_idx = 1
                    elif 290 < cx < 390: self.current_color_idx = 2
                    elif 410 < cx < 510: self.current_color_idx = 3
                    elif 530 < cx < 630: self.current_color_idx = -1 # Eraser mode
                
                # Back button
                if 400 < cy < 450 and 10 < cx < 100:
                    return "HOME"

                # Drawing logic
                if cy > 70: # Area below buttons
                    if self.current_color_idx == -1:
                        # Erase nearby points
                        self.erase_points(cx, cy)
                    else:
                        self.current_stroke.append((cx, cy))
            else:
                # Not pinching, end stroke
                if self.current_stroke:
                    self.points.append((self.current_stroke, self.colors[self.current_color_idx]))
                    self.current_stroke = []
        
        return "DRAWING"

    def erase_points(self, cx, cy):
        # Very basic eraser: clear all points for now or remove strokes nearby
        # For simplicity, let's filter out points within eraser_size
        new_points = []
        for stroke, color in self.points:
            new_stroke = [p for p in stroke if np.hypot(p[0]-cx, p[1]-cy) > self.eraser_size]
            if new_stroke:
                new_points.append((new_stroke, color))
        self.points = new_points

    def render(self, canvas):
        # Draw UI
        for label, (x1, y1, x2, y2) in self.buttons.items():
            color = (100, 100, 100)
            if label.startswith("Color"):
                idx = int(label.split()[1]) - 1
                color = self.colors[idx]
                if self.current_color_idx == idx:
                    cv2.rectangle(canvas, (x1-5, y1-5), (x2+5, y2+5), (255, 255, 255), 2)
            elif label == "Eraser" and self.current_color_idx == -1:
                cv2.rectangle(canvas, (x1-5, y1-5), (x2+5, y2+5), (255, 255, 255), 2)
                
            cv2.rectangle(canvas, (x1, y1), (x2, y2), color, -1)
            cv2.putText(canvas, label, (x1+5, y1+35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Draw all previous strokes
        for stroke, color in self.points:
            for i in range(1, len(stroke)):
                cv2.line(canvas, stroke[i - 1], stroke[i], color, self.brush_size)
        
        # Draw current stroke
        if self.current_stroke:
            color = (255, 255, 255) if self.current_color_idx == -1 else self.colors[self.current_color_idx]
            for i in range(1, len(self.current_stroke)):
                cv2.line(canvas, self.current_stroke[i - 1], self.current_stroke[i], color, self.brush_size)
        
        return canvas
