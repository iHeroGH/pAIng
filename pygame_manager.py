import pygame
import random
from abstract import GameObject

from paddle import Paddle
from ball import Ball

class Manager:

    WIDTH = 600
    HEIGHT = 600
    SCREEN_SIZE = (WIDTH, HEIGHT)

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("You want to play? Let's play.")
        self.font = pygame.font.Font('freesansbold.ttf', 22)

        self.clock = pygame.time.Clock()
        self.refresh_rate = 45

        self.player = Paddle(10, self.HEIGHT)
        self.enemy = Paddle(self.WIDTH - 10 - Paddle.WIDTH, self.HEIGHT)
        self.ball = Ball(self.SCREEN_SIZE)

        self.done = False
        self.game_loop()

    def handle_events(self) -> None:
        """
        Handles all events in the Pygame event queue
        """
        # The general Pygame event handling method
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If the user is quitting
                self.done = True # We are done
            elif event.type == pygame.KEYDOWN: # If a key is pressed
                self.handle_key_events(event) # Delegate to a different function

    def handle_key_events(self, event: pygame.event.Event) -> None:
        if self.ball.is_dead:
            self.ball.launch()

    def handle_paddle_movement(self) -> None:
        # Which key corresponds to what movement
        player_to_move = {
            pygame.K_w: Paddle.move_up,
            pygame.K_s: Paddle.move_down
        }

        enemy_to_move = {
            pygame.K_UP: Paddle.move_up,
            pygame.K_DOWN: Paddle.move_down
        }

        # Move depending on the move key
        keys_pressed = pygame.key.get_pressed()
        for key, move_func in player_to_move.items():
            if keys_pressed[key]:
                move_func(self.player, self.SCREEN_SIZE)

        # enemy_choice = random.choice(list(enemy_to_move.values()))
        for key, move_func in enemy_to_move.items():
            if keys_pressed[key]:
                move_func(self.enemy, self.SCREEN_SIZE)


    def draw(self, *objects: GameObject):
        self.screen.fill((0, 0, 0))

        pygame.draw.line(
            self.screen,
            (255, 255, 255),
            (self.WIDTH//2, 0),
            (self.WIDTH//2, self.HEIGHT)
        )

        self.draw_scores()

        for object in objects:
            drawable = object.get_drawable()
            match len(drawable):
                case 4:
                    object.set_rect(pygame.draw.rect(
                        self.screen, (255,255,255), drawable
                    ))
                case 2:
                    object.set_rect(pygame.draw.circle(
                        self.screen, (255, 0, 0), *drawable # type: ignore
                    ))

    def draw_scores(self):
        player_score = self.font.render(
            str(self.player.points), True, (255, 255, 255), (0, 0, 0)
        )
        enemy_score = self.font.render(
            str(self.enemy.points), True, (255, 255, 255), (0, 0, 0)
        )

        self.screen.blit(player_score, (self.WIDTH//2 - 30, 10))
        self.screen.blit(enemy_score, (self.WIDTH//2 + 30, 10))

    def game_loop(self):
        while not self.done:
            self.clock.tick(self.refresh_rate)

            self.draw(self.ball, self.player, self.enemy)

            self.handle_events()
            self.handle_paddle_movement()

            self.ball.move(self.SCREEN_SIZE, self.player, self.enemy)

            pygame.display.flip()
