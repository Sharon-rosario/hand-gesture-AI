class BaseModule:
    def update(self, landmarks):
        """Update module state based on hand landmarks."""
        pass

    def render(self, frame):
        """Render module-specific visuals on the frame."""
        pass
