import cv2
import numpy as np
from modules.base_module import BaseModule
from core.gesture_detector import GestureDetector
from ui.canvas import Canvas

class DrawingBoard(BaseModule):
    def __init__(self):
        super().__init__()
        self.detector = GestureDetector()
        self.canvas_tools = Canvas()
        self.points = []
        self.current_stroke = []
        self.colors = [(255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0)]
        self.color_names = ["White", "Red", "Green", "Blue"]
        self.current_color_idx = 0 # White by default
        self.brush_size = 5
        self.eraser_size = 50
        self.last_w, self.last_h = 0, 0
        self.buttons = {}
        
        # Stability & Smoothing
        self.lost_frame_count = 0
        self.max_lost_frames = 3
        self.smooth_x, self.smooth_y = 0, 0
        self.alpha = 0.5 # Smoothing factor (0 to 1, lower is smoother but more lag)


        
    def _update_layout(self, w, h):
        """Update button positions based on current frame resolution."""
        if w == self.last_w and h == self.last_h:
            return
            
        self.last_w, self.last_h = w, h
        btn_w = min(100, w // 10)
        btn_h = 50
        gap = 10
        start_x = (w - (btn_w * 6 + gap * 5)) // 2 # Center buttons
        
        # Define buttons
        self.buttons = {
            "White": (start_x, 10, start_x + btn_w, 10 + btn_h),
            "Red": (start_x + (btn_w + gap), 10, start_x + (btn_w + gap) + btn_w, 10 + btn_h),
            "Green": (start_x + (btn_w + gap)*2, 10, start_x + (btn_w + gap)*2 + btn_w, 10 + btn_h),
            "Blue": (start_x + (btn_w + gap)*3, 10, start_x + (btn_w + gap)*3 + btn_w, 10 + btn_h),
            "Eraser": (start_x + (btn_w + gap)*4, 10, start_x + (btn_w + gap)*4 + btn_w, 10 + btn_h),
            "Clear": (start_x + (btn_w + gap)*5, 10, start_x + (btn_w + gap)*5 + btn_w, 10 + btn_h),
            "Exit": (10, 10, 10 + btn_w, 10 + btn_h)
        }

    def update(self, landmarks, frame_shape):
        h, w, _ = frame_shape
        self._update_layout(w, h)
        
        if not landmarks:
            self.lost_frame_count += 1
            if self.lost_frame_count >= self.max_lost_frames:
                if self.current_stroke:
                    self.points.append((self.current_stroke, self.colors[self.current_color_idx if self.current_color_idx != -1 else 0]))
                    self.current_stroke = []
            return "DRAWING"

        # Hand found, reset lost frame count
        self.lost_frame_count = 0
        
        is_drawing = self.detector.is_drawing_mode(landmarks)
        is_selecting = self.detector.is_pinch(landmarks)
        index_tip = self.detector.get_index_finger_tip(landmarks)
        
        if index_tip:
            # Apply smoothing to coordinates
            new_x, new_y = int(index_tip.x * w), int(index_tip.y * h)
            if self.smooth_x == 0: # Initialize
                self.smooth_x, self.smooth_y = new_x, new_y
            else:
                self.smooth_x = int(self.alpha * new_x + (1 - self.alpha) * self.smooth_x)
                self.smooth_y = int(self.alpha * new_y + (1 - self.alpha) * self.smooth_y)
            
            cx, cy = self.smooth_x, self.smooth_y
            
            if is_selecting:

                for label, (x1, y1, x2, y2) in self.buttons.items():
                    if x1 < cx < x2 and y1 < cy < y2:
                        if label in self.color_names: self.current_color_idx = self.color_names.index(label)
                        elif label == "Eraser": self.current_color_idx = -1
                        elif label == "Clear": self.points = []
                        elif label == "Exit": return "HOME"

            if is_drawing and cy > 80:
                if self.current_color_idx == -1:
                    self.erase_points(cx, cy)
                else:
                    self.current_stroke.append((cx, cy))
            else:
                # Still count as "drawing" if we just briefly lost the pose
                if self.current_stroke:
                    self.lost_frame_count += 1
                    if self.lost_frame_count >= self.max_lost_frames:
                        color = self.colors[self.current_color_idx] if self.current_color_idx != -1 else (0,0,0)
                        self.points.append((self.current_stroke, color))
                        self.current_stroke = []
                        self.lost_frame_count = 0

        
        return "DRAWING"

    def erase_points(self, cx, cy):
        new_points = []
        for stroke, color in self.points:
            new_stroke = [p for p in stroke if np.hypot(p[0]-cx, p[1]-cy) > self.eraser_size]
            if new_stroke:
                new_points.append((new_stroke, color))
        self.points = new_points

    def render(self, canvas):
        h, w = canvas.shape[:2]
        cv2.rectangle(canvas, (0, 0), (w, 70), (25, 25, 25), -1)
        
        for label, (x1, y1, x2, y2) in self.buttons.items():
            color = (100, 100, 100)
            active = False
            if label in self.color_names:
                idx = self.color_names.index(label)
                color = self.colors[idx]
                active = (self.current_color_idx == idx)
            elif label == "Eraser":
                color = (200, 200, 200)
                active = (self.current_color_idx == -1)
            elif label == "Exit": color = (0, 0, 200)
            
            self.canvas_tools.draw_ui_box(canvas, label, x1, y1, x2, y2, color, active)

        for stroke, color in self.points:
            for i in range(1, len(stroke)):
                cv2.line(canvas, stroke[i - 1], stroke[i], color, self.brush_size, cv2.LINE_AA)
        if self.current_stroke:
            color = self.colors[self.current_color_idx] if self.current_color_idx != -1 else (255,255,255)
            for i in range(1, len(self.current_stroke)):
                cv2.line(canvas, self.current_stroke[i - 1], self.current_stroke[i], color, self.brush_size, cv2.LINE_AA)
        return canvas
