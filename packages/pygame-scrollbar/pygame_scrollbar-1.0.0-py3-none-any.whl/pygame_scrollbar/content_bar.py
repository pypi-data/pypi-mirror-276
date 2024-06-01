from pygame import Surface, Rect, draw, mouse
from .scroll_bar_position import ScrollBarPosition


class ContentBar:
    def __init__(self, size: tuple[int, int]):
        """
        Initializes a ContentBar object that you can customize by making subclass.
        Represents a content bar within a scrollable interface.

        Args:
            size (tuple[int, int]): The size of the content bar.
        """
        self.__position = _ContentBarPosition(size=size)
        self.surface: Surface = Surface(size)
        self.rect: Rect = Rect(0, 0, self.__position.width, self.__position.height)

    def set_y_position(self, index: int, scroll_bar_position: ScrollBarPosition) -> None:
        """
        Sets the vertical position of the content bar based on its index and the scroll bar position.

        Args:
            index (int): The index of the content bar.
            scroll_bar_position (ScrollBarPosition): The position of the scroll bar.
        """
        self.__position.set_position(index=index, scroll_bar_position=scroll_bar_position)

    def show(self, window_height: int) -> None:
        """
        Renders the content bar on its surface.

        Args:
            window_height (int): The height of the window.
        """
        self.__position.check_position()
        if window_height < self.__position.visible_y or self.__position.visible_y < 0:
            return
        draw.rect(self.surface, (100, 100, 100), self.rect)

    def check_if_clicked(self) -> None:
        """
        Checks if the content bar is clicked.
        """
        mouse_buttons = mouse.get_pressed()
        mouse_x, mouse_y = mouse.get_pos()
        if not mouse_buttons[0]:
            return
        if not self.__position.check_if_click(mouse_x, mouse_y):
            return

    def is_scrollable_down(self) -> bool:
        """
        Checks if the content bar is scrollable down.

        Returns:
            bool: True if the content bar is scrollable down, False otherwise.
        """
        return self.__position.y < 0

    def is_scrollable_up(self, scroll_bar_height: int, padding: int = 0) -> bool:
        """
        Checks if the content bar is scrollable up.

        Args:
            scroll_bar_height (int): The height of the scroll bar.
            padding (int, optional): The padding. Defaults to 0.

        Returns:
            bool: True if the content bar is scrollable up, False otherwise.
        """
        return self.__position.y + self.__position.height > scroll_bar_height - padding

    @property
    def position(self) -> tuple[int, int]:
        """
        Gets the position of the content bar.

        Returns:
            tuple[int, int]: The position of the content bar.
        """
        return self.__position.position


class _ContentBarPosition:
    def __init__(self, size: tuple[int, int]):
        """
        Initializes a _ContentBarPosition object.
        Represents the position of a content bar within a scrollable interface.

        Args:
            size (tuple[int, int]): The size of the content bar.
        """
        self.__scroll_bar_position = None
        self.x: int = 0
        self.y: int = 0
        self.__starting_y: int = 0
        self.width, self.height = size

    def check_position(self) -> None:
        """
        Checks the position of the content bar.
        """
        if not self.__scroll_bar_position.is_scrolled:
            return
        self.y = self.__scroll_bar_position.y + self.__starting_y

    def set_position(self, index: int, scroll_bar_position: ScrollBarPosition) -> None:
        """
        Sets the position of the content bar based on its index and the scroll bar position.

        Args:
            index (int): The index of the content bar.
            scroll_bar_position (ScrollBarPosition): The position of the scroll bar.
        """
        self.__scroll_bar_position = scroll_bar_position
        self.__starting_y = index * (self.height + self.__scroll_bar_position.margin)
        self.y = self.__starting_y

    def check_if_click(self, mouse_x: int, mouse_y: int) -> bool:
        """
        Checks if the content bar is clicked.

        Args:
            mouse_x (int): The x-coordinate of the mouse.
            mouse_y (int): The y-coordinate of the mouse.

        Returns:
            bool: True if the content bar is clicked, False otherwise.
        """
        scroll_bar_x, scroll_bar_y = self.__scroll_bar_position.position
        if not scroll_bar_x < mouse_x < self.width + scroll_bar_x:
            return False
        if not scroll_bar_y + self.y < mouse_y < scroll_bar_y + self.y + self.height:
            return False
        return True

    @property
    def visible_y(self) -> int:
        """
        Gets the visible y-coordinate of the content bar.

        Returns:
            int: The visible y-coordinate of the content bar.
        """
        scroll_bar_x, scroll_bar_y = self.__scroll_bar_position.position
        return scroll_bar_y + self.y

    @property
    def position(self) -> tuple[int, int]:
        """
        Gets the position of the content bar.

        Returns:
            tuple[int, int]: The position of the content bar.
        """
        return self.x, self.y

