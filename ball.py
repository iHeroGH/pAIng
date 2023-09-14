from math import sin

from abstract import GameObject
from paddle import Paddle

class Ball(GameObject):

    RADIUS = 10

    def __init__(self, screen_size):
        self.x, self.y = screen_size[0]//2, screen_size[1]//2

        self.v_x = -10
        self.v_y = 10
        self.angle = 0

    def get_drawable(self) -> tuple[tuple[int, int], int]:
        return ((self.x, self.y), self.RADIUS)

    def move(
            self,
            screen_size: tuple,
            player: Paddle, enemy: Paddle,
            time: int = 1) -> None:
        """
        Moves the projectile based on its velocity

        Parameters
        ----------
        screen_size : tuple
            The size of the screen
        time : int
            The time step multiplier for the velocity (default 1)
        """
        # Change position based on velocity
        self.x += time * self.v_x
        self.y += time * self.v_y * sin(self.angle)

        # Check screen collisions to make sure we don't go off-screen
        self.check_collision(screen_size, player, enemy)

    def check_collision(
            self,
            screen_size,
            player: Paddle, enemy: Paddle) -> None:
        """
        Implements rebound when the projectile hits a paddle

        Parameters
        ----------
        screen_size : tuple
            The size of the screen
        player : Paddle
            The left paddle
        enemy : Paddle
            The right paddle
        """

        # Player Collision
        if self.x - self.RADIUS <= player.x + player.WIDTH:
            if player.y < self.y < player.y + player.HEIGHT:
                self.v_x *= -1
                self.angle = (self.y - (player.y + player.HEIGHT//2)) / player.HEIGHT

        # Enemy Collision
        if self.x + self.RADIUS >= enemy.x:
            if enemy.y < self.y < enemy.y + enemy.HEIGHT:
                self.v_x *= -1
                self.angle = (self.y - (enemy.y + enemy.HEIGHT//2)) / enemy.HEIGHT

        # Screen Collision
        if self.y - self.RADIUS <= 0 or self.y + self.RADIUS >= screen_size[1]:
            self.v_y *= -1

        # Death Collision
        if self.x - self.RADIUS <= 0 or self.x + self.RADIUS >= screen_size[0]:
            self.die(screen_size)

    def die(self, screen_size):
        self.v_x = 0
        self.v_y = 0
        self.x, self.y = screen_size[0]//2, screen_size[1]//2