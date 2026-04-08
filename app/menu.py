import cv2

class Menu:
    def __init__(self):
        self.modules = ["Drawing Board", "Fruit Ninja (Soon)"]
        self.buttons = {
            "Drawing Board": (200, 150, 440, 210),
            "Fruit Ninja (Soon)": (200, 250, 440, 310)
        }

    def update(self, landmarks, is_pinch, frame_shape):
        if not landmarks or not is_pinch:
            return None
        
        h, w, _ = frame_shape
        hand = landmarks[0]
        index_tip = hand.landmark[8]
        cx, cy = int(index_tip.x * w), int(index_tip.y * h)
        
        for name, (x1, y1, x2, y2) in self.buttons.items():
            if x1 < cx < x2 and y1 < cy < y2:
                if name == "Drawing Board":
                    return "DRAWING"
        
        return "HOME"

    def render(self, canvas):
        cv2.putText(canvas, "🖐️ Hand Gesture Menu", (150, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
        
        for name, (x1, y1, x2, y2) in self.buttons.items():
            cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(canvas, name, (x1 + 20, y1 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1)
        
        cv2.putText(canvas, "Pinch to Select", (230, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        return canvas
