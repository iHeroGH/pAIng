from abstract import GameObject
from pygame import Rect

class Paddle(GameObject):

    WIDTH = 10
    HEIGHT = 70

    def __init__(self, x, screen_height):
        self.x: int = x
        self.y: int = screen_height // 2 - self.HEIGHT // 2

        self.v_y = 10

        self.rect: Rect | None = None

    def get_drawable(self) -> tuple[int, int, int, int]:
        return (self.x, self.y, self.WIDTH, self.HEIGHT)

    def set_rect(self, rect: Rect):
        self.rect = rect

    def move(
            self,
            screen_size: tuple,
            move_y: int = 0) -> None:
        """
        Changes the position of the cannon based on its velocity and a multiplier

        The move_y multiplier should be -1, 0, or 1 depending on if
        the object is moving backwards or not moving at all.

        It can also be used as any other int for a multiplier to the speed

        Parameters
        ----------
        move_y : int
            The y movement multiplier (default 0)
        """
        # Move y based on its velocity and constrict it to the screen size
        self.y += move_y * self.v_y
        self.y = max(0, min(self.y, screen_size[1] - self.HEIGHT))

    def move_up(self, screen_size: tuple) -> None:
        """
        Delagates to the move function the parameters necessary to move up

        move(-1)

        Parameters
        ----------
        screen_size : tuple
            The size of the screen
        """
        self.move(screen_size, -1)

    def move_down(self, screen_size: tuple) -> None:
        """
        Delagates to the move function the parameters necessary to move down

        move(1)

        Parameters
        ----------
        screen_size : tuple
            The size of the screen
        """
        self.move(screen_size, 1)