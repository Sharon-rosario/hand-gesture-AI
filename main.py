from core.hand_tracker import HandTracker
from core.gesture_detector import GestureDetector
from ui.canvas import Canvas
from app.menu import Menu
from modules.drawing_board import DrawingBoard
from modules.shape_builder import ShapeBuilder
import cv2


def main():
    tracker = HandTracker()
    detector = GestureDetector()
    canvas_ui = Canvas()
    menu = Menu()
    drawing_board = DrawingBoard()
    shape_builder = ShapeBuilder()

    state = "HOME" # HOME, DRAWING, SHAPES


    print("Starting Hand Gesture Detection...")
    print("Press ESC to exit.")

    while True:
        frame, landmarks = tracker.get_frame()
        if frame is None:
            print("Loop interrupted: No frame received from camera.")
            break


        is_pinch = detector.is_pinch(landmarks)
        status = ""

        # Update and Render based on state
        if state == "HOME":
            next_state = menu.update(landmarks, is_pinch, frame.shape)
            if next_state:
                state = next_state
            
            # Create a black canvas for the menu
            h, w, c = frame.shape
            canvas = canvas_ui.create_black_canvas(h, w, c)
            canvas = menu.render(canvas)
            status = "Menu Mode"
        
        elif state == "DRAWING":
            result = drawing_board.update(landmarks, frame.shape)
            if result == "HOME":
                state = "HOME"
            
            h, w, c = frame.shape
            canvas = canvas_ui.create_black_canvas(h, w, c)
            canvas = drawing_board.render(canvas)
            status = "Drawing Board"
        
        elif state == "SHAPES":
            result = shape_builder.update(landmarks, frame.shape)
            if result == "HOME":
                state = "HOME"
            
            h, w, c = frame.shape
            canvas = canvas_ui.create_black_canvas(h, w, c)
            canvas = shape_builder.render(canvas)
            status = "Shape Builder"


        # Always draw the hand skeleton on top if needed (optional)
        canvas_ui.draw_skeleton(canvas, landmarks)
        canvas_ui.show(canvas, status)


if __name__ == "__main__":
    main()
