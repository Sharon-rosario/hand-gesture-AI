import cv2
import numpy as np
import random
import time
from modules.base_module import BaseModule
from core.gesture_detector import GestureDetector
from ui.canvas import Canvas

class Fruit:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.radius = 30
        self.x = random.randint(self.radius, w - self.radius)
        self.y = h + self.radius
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-18, -25) # Upward velocity
        self.gravity = 0.8
        self.sliced = False
        self.color = (random.randint(50, 255), random.randint(50, 255), 0) # Random fruity color
        self.slice_time = 0
        self.slice_p1 = (0,0)
        self.slice_p2 = (0,0)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        return self.y < self.h + 100 # Keep alive until well off screen

    def check_slice(self, px, py, last_px, last_py):
        if self.sliced: return False
        
        # Simple collision: if finger is inside radius
        dist = np.hypot(self.x - px, self.y - py)
        if dist < self.radius:
            self.sliced = True
            self.slice_time = time.time()
            return True
        return False

class Bomb(Fruit):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.color = (50, 50, 50) # Gray/Black for bomb
        self.is_bomb = True

class FruitNinja(BaseModule):
    def __init__(self):
        super().__init__()
        self.detector = GestureDetector()
        self.canvas_tools = Canvas()
        self.fruits = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.last_spawn_time = time.time()
        self.spawn_interval = 1.5
        self.last_finger_pos = None
        self.slash_trail = [] # Store (x, y, time)
        self.max_trail_len = 10

    def update(self, landmarks, frame_shape):
        if self.game_over:
            if landmarks and self.detector.is_pinch(landmarks):
                self.__init__()
            return "FRUIT_NINJA"

        h, w, _ = frame_shape
        
        # Spawn logic
        if time.time() - self.last_spawn_time > self.spawn_interval:
            if random.random() < 0.15:
                self.fruits.append(Bomb(w, h))
            else:
                self.fruits.append(Fruit(w, h))
            self.last_spawn_time = time.time()
            self.spawn_interval = max(0.5, self.spawn_interval * 0.99)

        # Hand logic
        current_finger_pos = None
        if landmarks:
            index_tip = self.detector.get_index_finger_tip(landmarks)
            if index_tip:
                current_finger_pos = (int(index_tip.x * w), int(index_tip.y * h))
                self.slash_trail.append(current_finger_pos)
                if len(self.slash_trail) > self.max_trail_len:
                    self.slash_trail.pop(0)
        else:
            if self.slash_trail: self.slash_trail.pop(0)

        # Update fruits and check collisions
        new_fruits = []
        for fruit in self.fruits:
            if fruit.update():
                if not fruit.sliced and current_finger_pos and self.last_finger_pos:
                    # Improved collision: check points between last and current pos
                    # This handles fast movements better
                    steps = 5
                    for i in range(steps):
                        tx = int(self.last_finger_pos[0] + (current_finger_pos[0] - self.last_finger_pos[0]) * (i/steps))
                        ty = int(self.last_finger_pos[1] + (current_finger_pos[1] - self.last_finger_pos[1]) * (i/steps))
                        if fruit.check_slice(tx, ty, 0, 0):
                            if hasattr(fruit, 'is_bomb'):
                                self.lives -= 1
                                if self.lives <= 0: self.game_over = True
                            else:
                                self.score += 1
                            break

                
                # Check if fruit fell without being sliced
                if fruit.y > h and not fruit.sliced and not hasattr(fruit, 'is_bomb'):
                    # Missed a fruit
                    # self.lives -= 0.5 # Optional penalty
                    pass
                
                new_fruits.append(fruit)
        self.fruits = new_fruits
        self.last_finger_pos = current_finger_pos

        # Back to home
        if landmarks and self.detector.is_pinch(landmarks):
            # Check for exit button area
            if current_finger_pos and current_finger_pos[0] < 100 and current_finger_pos[1] < 100:
                return "HOME"

        return "FRUIT_NINJA"

    def render(self, canvas):
        h, w = canvas.shape[:2]
        
        # UI
        cv2.putText(canvas, f"Score: {self.score}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(canvas, f"Lives: {'X' * self.lives}", (w - 200, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Exit Button
        self.canvas_tools.draw_ui_box(canvas, "EXIT", 10, 60, 80, 110, (0, 0, 200))

        # Render Slash Trail
        for i in range(1, len(self.slash_trail)):
            thickness = int(i * 1.5)
            cv2.line(canvas, self.slash_trail[i-1], self.slash_trail[i], (255, 255, 255), thickness, cv2.LINE_AA)

        # Render Fruits

        for fruit in self.fruits:
            if not fruit.sliced:
                cv2.circle(canvas, (int(fruit.x), int(fruit.y)), fruit.radius, fruit.color, -1)
                cv2.circle(canvas, (int(fruit.x), int(fruit.y)), fruit.radius, (255, 255, 255), 2)
            else:
                # Splitting animation
                offset = int((time.time() - fruit.slice_time) * 50)
                # Left half
                cv2.ellipse(canvas, (int(fruit.x) - offset, int(fruit.y)), (fruit.radius, fruit.radius), 
                           0, 90, 270, fruit.color, -1)
                # Right half
                cv2.ellipse(canvas, (int(fruit.x) + offset, int(fruit.y)), (fruit.radius, fruit.radius), 
                           0, -90, 90, fruit.color, -1)

        if self.game_over:
            cv2.rectangle(canvas, (w//2-200, h//2-100), (w//2+200, h//2+100), (0,0,0), -1)
            cv2.rectangle(canvas, (w//2-200, h//2-100), (w//2+200, h//2+100), (0,0,255), 2)
            cv2.putText(canvas, "GAME OVER", (w//2-120, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 3)
            cv2.putText(canvas, "Pinch to Restart", (w//2-100, h//2+50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1)

        return canvas
