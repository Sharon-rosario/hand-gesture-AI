import cv2

def get_landmark_coords(hand_landmarks, landmark_id, w, h):
    """Convert normalized landmark coordinates to pixel coordinates."""
    lm = hand_landmarks.landmark[landmark_id]
    return int(lm.x * w), int(lm.y * h)

def draw_text(frame, text, pos=(20, 50), color=(0, 255, 0)):
    """Draw text on frame for status updates."""
    cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
