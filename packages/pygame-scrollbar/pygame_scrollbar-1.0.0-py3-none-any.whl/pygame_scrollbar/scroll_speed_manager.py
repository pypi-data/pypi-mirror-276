class ScrollSpeedManager:
    def __init__(self, max_speed: int = 20):
        """
        Initializes the ScrollSpeedManager.

        Args:
            max_speed (int, optional): The maximum speed of scrolling. Defaults to 20.
        """
        self.max_speed: int = max_speed
        self.current_speed: int = 0
