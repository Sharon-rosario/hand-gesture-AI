import cv2
import numpy as np
from modules.base_module import BaseModule
from core.gesture_detector import GestureDetector
from ui.canvas import Canvas

class ShapeBuilder(BaseModule):
    def __init__(self):
        super().__init__()
        self.detector = GestureDetector()
        self.canvas_tools = Canvas()
        self.shapes = [] # List of (type, p1, p2, color)
        self.current_shape = None # (type, p1, p2)
        self.colors = [(255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0)]
        self.current_color_idx = 0
        self.mode = "Rectangle" # Square, Circle, Rectangle
        
        self.buttons = {
            "Rectangle": (100, 10, 220, 60),
            "Circle": (230, 10, 350, 60),
            "Square": (360, 10, 480, 60),
            "Clear": (500, 10, 600, 60),
            "Exit": (10, 10, 80, 60)
        }

    def update(self, landmarks, frame_shape):
        h, w, _ = frame_shape
        if not landmarks or len(landmarks) < 2:
            if self.current_shape:
                self.shapes.append(self.current_shape + (self.colors[self.current_color_idx],))
                self.current_shape = None
            
            # Selection logic for single hand if 2nd hand missing
            if landmarks:
                hand = landmarks[0]
                is_pinch = self.detector.is_pinch(landmarks, 0)
                index_tip = self.detector.get_index_finger_tip(landmarks, 0)
                if index_tip and is_pinch:
                    cx, cy = int(index_tip.x * w), int(index_tip.y * h)
                    for label, (x1, y1, x2, y2) in self.buttons.items():
                        if x1 < cx < x2 and y1 < cy < y2:
                            if label in ["Rectangle", "Circle", "Square"]: self.mode = label
                            elif label == "Clear": self.shapes = []
                            elif label == "Exit": return "HOME"
            return "SHAPES"

        # Two hands detected
        h1_is_pinch = self.detector.is_pinch(landmarks, 0)
        h2_is_pinch = self.detector.is_pinch(landmarks, 1)
        
        h1_tip = self.detector.get_index_finger_tip(landmarks, 0)
        h2_tip = self.detector.get_index_finger_tip(landmarks, 1)
        
        if h1_tip and h2_tip and h1_is_pinch and h2_is_pinch:
            p1 = (int(h1_tip.x * w), int(h1_tip.y * h))
            p2 = (int(h2_tip.x * w), int(h2_tip.y * h))
            
            if self.mode == "Square":
                # Force square by picking min delta
                dx = abs(p2[0] - p1[0])
                dy = abs(p2[1] - p1[1])
                side = min(dx, dy)
                sx = 1 if p2[0] > p1[0] else -1
                sy = 1 if p2[1] > p1[1] else -1
                p2 = (p1[0] + sx * side, p1[1] + sy * side)
            
            self.current_shape = (self.mode, p1, p2)
        else:
            # If one hand released, finish current shape
            if self.current_shape:
                self.shapes.append(self.current_shape + (self.colors[self.current_color_idx],))
                self.current_shape = None
                
        return "SHAPES"

    def render(self, canvas):
        h, w = canvas.shape[:2]
        cv2.rectangle(canvas, (0, 0), (w, 70), (25, 25, 25), -1)
        
        # UI
        for label, (x1, y1, x2, y2) in self.buttons.items():
            color = (150, 150, 150)
            active = (self.mode == label)
            if label == "Exit": color = (0, 0, 200)
            self.canvas_tools.draw_ui_box(canvas, label, x1, y1, x2, y2, color, active)

        # Draw stored shapes
        for stype, p1, p2, color in self.shapes:
            self.draw_shape(canvas, stype, p1, p2, color)
            
        # Draw current active shape
        if self.current_shape:
            stype, p1, p2 = self.current_shape
            self.draw_shape(canvas, stype, p1, p2, (255, 255, 0), 2) # Yellow preview

        return canvas

    def draw_shape(self, canvas, stype, p1, p2, color, thickness=2):
        if stype == "Rectangle" or stype == "Square":
            cv2.rectangle(canvas, p1, p2, color, thickness)
        elif stype == "Circle":
            center = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
            radius = int(np.hypot(p2[0] - p1[0], p2[1] - p1[1]) // 2)
            cv2.circle(canvas, center, radius, color, thickness)
