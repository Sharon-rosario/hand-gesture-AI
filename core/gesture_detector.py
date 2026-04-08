import math

class GestureDetector:
    def __init__(self):
        # Finger indices: Thumb(0), Index(1), Middle(2), Ring(3), Pinky(4)
        self.finger_tips = [4, 8, 12, 16, 20]
        self.finger_pips = [2, 6, 10, 14, 18]

    def get_distance(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def get_fingers_up(self, landmarks, hand_index=0):
        """Returns a list of 5 booleans representing each finger's up/down state."""
        if not landmarks or len(landmarks) <= hand_index:
            return [False] * 5
            
        hand = landmarks[hand_index]
        fingers = []
        
        # Thumb: Check if tip is further left/right than pip (depending on hand orientation, but simple x check for now)
        # Actually, for thumb, checking if tip is above pip (y) is more common if hand is upright
        if hand.landmark[self.finger_tips[0]].y < hand.landmark[self.finger_pips[0]].y:
            fingers.append(True)
        else:
            fingers.append(False)
            
        # Other fingers: Check if tip is above pip
        for i in range(1, 5):
            if hand.landmark[self.finger_tips[i]].y < hand.landmark[self.finger_pips[i]].y:
                fingers.append(True)
            else:
                fingers.append(False)
        
        return fingers

    def is_drawing_mode(self, landmarks, hand_index=0):
        """Drawing mode: Only index finger is up."""
        fingers = self.get_fingers_up(landmarks, hand_index)
        # Index is fingers[1]
        return fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]

    def is_pinch(self, landmarks, hand_index=0):
        if not landmarks or len(landmarks) <= hand_index:
            return False
        hand = landmarks[hand_index]
        thumb_tip = hand.landmark[4]
        index_tip = hand.landmark[8]
        dist = self.get_distance((thumb_tip.x, thumb_tip.y), (index_tip.x, index_tip.y))
        return dist < 0.03


    def get_index_finger_tip(self, landmarks, hand_index=0):
        if not landmarks or len(landmarks) <= hand_index:
            return None
        return landmarks[hand_index].landmark[8]
