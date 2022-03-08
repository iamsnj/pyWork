#!/usr/bin/python3

import pygame
from pygame.locals import *
import time
import random

SIZE = 40
X = 1040
Y = 640


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load('assets/apple.jpg').convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 25) * SIZE
        self.y = random.randint(0, 15) * SIZE


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.block = pygame.image.load('assets/block.jpg').convert()
        self.direction = 'right'

        self.length = 1
        self.x = [SIZE]
        self.y = [SIZE]

    def draw(self):
        head = pygame.image.load('assets/square.png').convert()
        self.parent_screen.fill((10, 55, 43))
        self.parent_screen.blit(head, (self.x[0], self.y[0]))

        for i in range(1, self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake And Apple Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((X, Y))
        self.render_background()
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        pygame.mixer.music.load('assets/bg_music.ogg')
        pygame.mixer.music.play(-1, 0)

    def render_background(self):
        bg = pygame.image.load("assets/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play_sound(self, sound_name):
        sound = pygame.mixer.Sound(f"assets/{sound_name}.wav")
        pygame.mixer.Sound.play(sound)

    def is_collision(self, x2, y2):
        x1 = self.snake.x[0]
        y1 = self.snake.y[0]

        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    def game_over(self):
        # snake eat itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i]):
                return True

        # collision with boundary
        x1 = self.snake.x[0]
        y1 = self.snake.y[0]
        if SIZE - abs(x1 - X) > 0 or x1 < 0 or \
            SIZE - abs(y1 - Y) > 0 or y1 < 0:
            return True
        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # collision with apple
        if self.is_collision(self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        if self.game_over():
            self.play_sound('crash')
            raise 'Game Over'

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'Score: {self.snake.length}', True,
                            (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        msg = font.render('Game Over', True, (255, 255, 255))
        self.surface.blit(msg, (400, 200))
        score = font.render(f'Score: {self.snake.length}', True,
                            (255, 255, 255))
        self.surface.blit(score, (400, 250))
        score = font.render(f'Press Enter for play again', True,
                            (255, 255, 255))
        self.surface.blit(score, (400, 300))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        pygame.mixer.music.unpause()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    if pause and event.key == K_RETURN:
                        self.reset()
                        pause = False
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                pause = True
                self.show_game_over()
            time.sleep(0.2)


if __name__ == '__main__':
    game = Game()
    game.run()
