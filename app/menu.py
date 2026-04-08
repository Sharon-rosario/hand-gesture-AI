import cv2
from ui.canvas import Canvas

class Menu:
    def __init__(self):
        self.canvas_tools = Canvas()
        self.buttons = {}
        self.last_w, self.last_h = 0, 0

    def _update_layout(self, w, h):
        if w == self.last_w and h == self.last_h:
            return
        self.last_w, self.last_h = w, h
        
        btn_w, btn_h = 300, 60
        center_x = w // 2
        start_y = h // 2 - 100
        
        self.buttons = {
            "Drawing Board": (center_x - btn_w // 2, start_y, center_x + btn_w // 2, start_y + btn_h),
            "Fruit Ninja": (center_x - btn_w // 2, start_y + 100, center_x + btn_w // 2, start_y + 100 + btn_h),
            "Exit App": (center_x - btn_w // 2, start_y + 200, center_x + btn_w // 2, start_y + 200 + btn_h)
        }

    def update(self, landmarks, is_pinch, frame_shape):
        h, w, _ = frame_shape
        self._update_layout(w, h)
        
        if not landmarks or not is_pinch:
            return None
        
        hand = landmarks[0]
        index_tip = hand.landmark[8]
        cx, cy = int(index_tip.x * w), int(index_tip.y * h)
        
        for name, (x1, y1, x2, y2) in self.buttons.items():
            if x1 < cx < x2 and y1 < cy < y2:
                if name == "Drawing Board": return "DRAWING"
                elif name == "Exit App": exit()
        
        return "HOME"

    def render(self, canvas):
        h, w = canvas.shape[:2]
        self._update_layout(w, h)
        
        # Centered Title
        title = "HAND GESTURE SYSTEM"
        font_scale = 1.1
        thickness = 2
        text_size = cv2.getTextSize(title, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
        tx = (w - text_size[0]) // 2
        
        cv2.putText(canvas, title, (tx, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), thickness, cv2.LINE_AA)
        cv2.line(canvas, (tx, 115), (tx + text_size[0], 115), (0, 80, 0), 2)


        for name, (x1, y1, x2, y2) in self.buttons.items():
            color = (0, 200, 0) if name != "Exit App" else (0, 0, 200)
            self.canvas_tools.draw_ui_box(canvas, name, x1, y1, x2, y2, color)
        
        cv2.putText(canvas, "PINCH TO SELECT", (w//2 - 80, h - 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1, cv2.LINE_AA)
        return canvas
