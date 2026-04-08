import cv2
import numpy as np
import mediapipe as mp

class Canvas:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.drawing_styles = mp.solutions.drawing_styles
        self.window_initialized = False

    def create_black_canvas(self, h, w, c):
        return np.zeros((h, w, c), dtype=np.uint8)

    def draw_skeleton(self, canvas, landmarks):
        if landmarks:
            for hand_landmarks in landmarks:
                self.mp_draw.draw_landmarks(
                    canvas,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.drawing_styles.get_default_hand_landmarks_style(),
                    self.drawing_styles.get_default_hand_connections_style()
                )

    def draw_ui_box(self, canvas, label, x1, y1, x2, y2, color, active=False):
        """Helper to draw a prettier UI box."""
        thickness = -1 if active else 2
        # Shadow
        cv2.rectangle(canvas, (x1+3, y1+3), (x2+3, y2+3), (30, 30, 30), -1)
        # Main box
        cv2.rectangle(canvas, (x1, y1), (x2, y2), color, thickness)
        if not active:
            # Draw outline if not filled
            cv2.rectangle(canvas, (x1, y1), (x2, y2), (200, 200, 200), 1)
        
        # Label
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        tx = x1 + (x2 - x1 - text_size[0]) // 2
        ty = y1 + (y2 - y1 + text_size[1]) // 2
        cv2.putText(canvas, label, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    def show(self, canvas, status=""):
        if not self.window_initialized:
            cv2.namedWindow("Hand Gesture UI", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Hand Gesture UI", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            self.window_initialized = True

        if status:
            # Prettier status bar at bottom
            h, w = canvas.shape[:2]
            cv2.rectangle(canvas, (0, h-40), (w, h), (40, 40, 40), -1)
            cv2.putText(canvas, f"MODE: {status}", (20, h-12), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
        
        cv2.imshow("Hand Gesture UI", canvas)
        
        if cv2.waitKey(1) & 0xFF == 27:
            cv2.destroyAllWindows()
            exit()