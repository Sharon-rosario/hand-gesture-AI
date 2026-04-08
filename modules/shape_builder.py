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
        self.current_shape = None
        self.colors = [(255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0)]
        self.current_color_idx = 0
        self.mode = "Rectangle"
        self.buttons = {}
        self.last_w, self.last_h = 0, 0
        
    def _update_layout(self, w, h):
        if w == self.last_w and h == self.last_h:
            return
        self.last_w, self.last_h = w, h
        
        btn_count = 7
        btn_w = min(90, (w - 20) // btn_count)
        btn_h = 50
        gap = 5
        start_x = (w - (btn_w * btn_count + gap * (btn_count-1))) // 2
        
        self.buttons = {
            "Rectangle": (start_x, 10, start_x + btn_w, 10 + btn_h),
            "Circle": (start_x + (btn_w + gap), 10, start_x + (btn_w + gap) + btn_w, 10 + btn_h),
            "Square": (start_x + (btn_w + gap)*2, 10, start_x + (btn_w + gap)*2 + btn_w, 10 + btn_h),
            "Eraser": (start_x + (btn_w + gap)*3, 10, start_x + (btn_w + gap)*3 + btn_w, 10 + btn_h),
            "Move": (start_x + (btn_w + gap)*4, 10, start_x + (btn_w + gap)*4 + btn_w, 10 + btn_h),
            "Clear": (start_x + (btn_w + gap)*5, 10, start_x + (btn_w + gap)*5 + btn_w, 10 + btn_h),
            "Exit": (start_x + (btn_w + gap)*6, 10, start_x + (btn_w + gap)*6 + btn_w, 10 + btn_h)
        }

        
        # Dragging state
        self.dragging_idx = -1
        self.drag_offset = (0, 0)
        
        # Stability Buffer
        self.lost_frame_count = 0
        self.max_lost_frames = 10
        self.min_shape_size = 20




    def update(self, landmarks, frame_shape):
        h, w, _ = frame_shape
        self._update_layout(w, h)
        
        # 1. Check all hands for UI Button interaction FIRST
        if landmarks:
            for i in range(len(landmarks)):
                if self.detector.is_pinch(landmarks, i):
                    tip = self.detector.get_index_finger_tip(landmarks, i)
                    if tip:
                        cx, cy = int(tip.x * w), int(tip.y * h)
                        for label, (x1, y1, x2, y2) in self.buttons.items():
                            if x1 < cx < x2 and y1 < cy < y2:
                                if label in ["Rectangle", "Circle", "Square", "Eraser", "Move"]: 
                                    self.mode = label
                                    self.dragging_idx = -1
                                elif label == "Clear": self.shapes = []
                                elif label == "Exit": return "HOME"
                                return "SHAPES"

        # 2. Logic for two-hand stretch (Building shapes)
        if landmarks and len(landmarks) >= 2:
            h1_is_pinch = self.detector.is_pinch(landmarks, 0)
            h2_is_pinch = self.detector.is_pinch(landmarks, 1)
            h1_tip = self.detector.get_index_finger_tip(landmarks, 0)
            h2_tip = self.detector.get_index_finger_tip(landmarks, 1)
            
            if h1_tip and h2_tip and h1_is_pinch and h2_is_pinch:
                self.lost_frame_count = 0
                p1 = (int(h1_tip.x * w), int(h1_tip.y * h))
                p2 = (int(h2_tip.x * w), int(h2_tip.y * h))
                if self.mode == "Square":
                    dx, dy = abs(p2[0] - p1[0]), abs(p2[1] - p1[1])
                    side = min(dx, dy)
                    sx = 1 if p2[0] > p1[0] else -1
                    sy = 1 if p2[1] > p1[1] else -1
                    p2 = (p1[0] + sx * side, p1[1] + sy * side)
                self.current_shape = (self.mode, p1, p2)
                return "SHAPES"

        # 3. Finalize current shape if hands lost or pinch released
        if self.current_shape:
            self.lost_frame_count += 1
            if self.lost_frame_count >= self.max_lost_frames:
                stype, p1, p2 = self.current_shape
                if abs(p2[0]-p1[0]) > self.min_shape_size or abs(p2[1]-p1[1]) > self.min_shape_size:
                    self.shapes.append(self.current_shape + (self.colors[self.current_color_idx],))
                self.current_shape = None
                self.lost_frame_count = 0

        # 4. Logic for Move/Eraser (Now works even if multiple hands are visible)
        if landmarks and self.mode in ["Eraser", "Move"]:
            for i in range(len(landmarks)):
                is_pinch = self.detector.is_pinch(landmarks, i)
                index_tip = self.detector.get_index_finger_tip(landmarks, i)
                if index_tip:
                    cx, cy = int(index_tip.x * w), int(index_tip.y * h)
                    
                    if self.mode == "Eraser" and is_pinch:
                        self.erase_at(cx, cy)
                    elif self.mode == "Move":
                        if is_pinch:
                            if self.dragging_idx == -1:
                                self.dragging_idx = self.find_shape_at(cx, cy)
                                if self.dragging_idx != -1:
                                    s = self.shapes[self.dragging_idx]
                                    self.drag_offset = (cx - s[1][0], cy - s[1][1])
                            else:
                                s = self.shapes[self.dragging_idx]
                                dx, dy = s[2][0] - s[1][0], s[2][1] - s[1][1]
                                new_p1 = (cx - self.drag_offset[0], cy - self.drag_offset[1])
                                new_p2 = (new_p1[0] + dx, new_p1[1] + dy)
                                self.shapes[self.dragging_idx] = (s[0], new_p1, new_p2, s[3])
                        else:
                            # Only reset if THIS hand was the one dragging? 
                            # To keep it simple, if no pinch detected on this hand, 
                            # we stop dragging if it was the dragging hand.
                            self.dragging_idx = -1
        
        return "SHAPES"




                
        return "SHAPES"

    def render(self, canvas):
        h, w = canvas.shape[:2]
        self._update_layout(w, h)
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

    def find_shape_at(self, cx, cy):
        """Finds the closest shape based on distance to its edge/surface."""
        closest_idx = -1
        min_dist = 50 # Capture radius (pixels)
        
        for i, (stype, p1, p2, _) in enumerate(self.shapes):
            dist = 1000
            if stype == "Rectangle" or stype == "Square":
                # Distance to the boundary of the rectangle
                x1, x2 = min(p1[0], p2[0]), max(p1[0], p2[0])
                y1, y2 = min(p1[1], p2[1]), max(p1[1], p2[1])
                
                # Check if inside
                if x1 <= cx <= x2 and y1 <= cy <= y2:
                    # Distance to nearest edge
                    dist = min(abs(cx-x1), abs(cx-x2), abs(cy-y1), abs(cy-y2))
                else:
                    # Distance to nearest edge (external)
                    dx = max(x1 - cx, 0, cx - x2)
                    dy = max(y1 - cy, 0, cy - y2)
                    dist = np.hypot(dx, dy)

            elif stype == "Circle":
                center = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
                radius = np.hypot(p2[0] - p1[0], p2[1] - p1[1]) // 2
                dist_to_center = np.hypot(cx - center[0], cy - center[1])
                dist = abs(dist_to_center - radius) # Distance to circumference
                
                # If inside, also consider distance to surface
                if dist_to_center < radius:
                    dist = min(dist, dist_to_center) # Allow grabbing by center too

            if dist < min_dist:
                min_dist = dist
                closest_idx = i
                
        return closest_idx


    def erase_at(self, cx, cy):
        idx = self.find_shape_at(cx, cy)
        if idx != -1:
            self.shapes.pop(idx)

