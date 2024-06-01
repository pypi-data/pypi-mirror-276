from .scroll_speed_manager import ScrollSpeedManager


class ScrollBarPosition:
    def __init__(self, position: tuple[int, int], scroll_speed_manager: ScrollSpeedManager, margin_between_content_bar: int = 10):
        """
        Initializes the ScrollBarPosition.

        Args:
            position (tuple[int, int]): The initial position of the scroll bar.
            scroll_speed_manager (ScrollSpeedManager): The manager that handles scroll speed.
            margin_between_content_bar (int, optional): The margin between content bars. Defaults to 10.
        """
        self.__scroll_bar_position: tuple[int, int] = position
        self.__margin_between_content_bar: int = margin_between_content_bar
        self.__y: int = 0
        self.__is_scrolled: bool = False
        self.__scroll_speed_manager: ScrollSpeedManager = scroll_speed_manager

    @property
    def margin(self) -> int:
        """
        Returns the margin between content bars.

        Returns:
            int: The margin between content bars.
        """
        return self.__margin_between_content_bar

    @property
    def position(self) -> tuple[int, int]:
        """
        Returns the current position of the scroll bar.

        Returns:
            tuple[int, int]: The current position of the scroll bar.
        """
        return self.__scroll_bar_position

    @property
    def y(self) -> int:
        """
        Returns the current y-coordinate of the scroll bar.

        Returns:
            int: The current y-coordinate of the scroll bar.
        """
        return self.__y

    def scroll_down(self) -> None:
        """
        Scrolls the bar down by increasing the y-coordinate based on the current scroll speed.
        """
        self.__y += self.__scroll_speed_manager.current_speed
        self.__is_scrolled = True

    def scroll_up(self) -> None:
        """
        Scrolls the bar up by decreasing the y-coordinate based on the current scroll speed.
        """
        self.__y -= self.__scroll_speed_manager.current_speed
        self.__is_scrolled = True

    def finish_scroll(self) -> None:
        """
        Resets the scrolling state.
        """
        self.__is_scrolled = False

    @property
    def is_scrolled(self) -> bool:
        """
        Returns whether the bar is currently being scrolled.

        Returns:
            bool: True if the bar is being scrolled, False otherwise.
        """
        return self.__is_scrolled
