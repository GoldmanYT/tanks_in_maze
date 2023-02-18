from consts import *
from maze import Maze
from tanks import Bullet

import pygame as pg
import pymunk.pygame_util

from sys import exit


pymunk.pygame_util.positive_y_is_up = False


class Draw:
    def __init__(self):
        self.x0, self.y0, self.a, self.w, self.walls = [None] * 5

    def update_draw_options(self, w, h, maze, screen_w, screen_h):
        self.a = min(w / maze.w, h / maze.h)
        self.w = self.a / 12
        self.x0, self.y0 = (screen_w - self.a * maze.w - self.w) / 2, (screen_h - self.a * maze.h - self.w) / 2
        self.walls = {
            'up': ((self.a + self.w) / 2, self.w / 2, self.a + self.w, self.w),
            'down': ((self.a + self.w) / 2, self.a + self.w / 2, self.a + self.w, self.w),
            'left': (self.w / 2, (self.a + self.w) / 2, self.w, self.a + self.w),
            'right': (self.a + self.w / 2, (self.a + self.w) / 2, self.w, self.a + self.w),
        }


class Game:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.screen = pg.display.set_mode((w, h))
        self.clock = pg.time.Clock()

        self.maze = None
        self.bullets = None
        self.walls = None

        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.draw = Draw()

        self.space = pymunk.Space()

        self.new_game()
        self.main()

    def add_bullet(self, position):
        x, y = position
        Bullet(x, y, 5, 0, self.space)

    def add_wall(self, x, y, w, h, i, j):
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.position = self.draw.x0 + j * self.draw.a + x, self.draw.y0 + i * self.draw.a + y
        shape = pymunk.Poly.create_box(body, (w, h))
        shape.elasticity = 1.
        self.space.add(body, shape)

    def new_game(self):
        self.maze = Maze()
        self.maze.generate()
        self.bullets = []
        self.walls = []

        self.draw.update_draw_options(self.w - D_W, self.h - D_H, self.maze, self.w, self.h)

        for i, row in enumerate(self.maze.field):
            for j, node in enumerate(row):
                walls = node.walls
                for wall in walls:
                    if walls[wall]:
                        x, y, w, h = self.draw.walls[wall]
                        self.add_wall(x, y, w, h, i, j)

    def main(self):
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                    exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.add_bullet(event.pos)

            self.screen.fill(BLACK)

            self.space.step(1 / FPS)
            self.space.debug_draw(self.draw_options)

            pg.display.flip()
            self.clock.tick(FPS)


if __name__ == '__main__':
    pg.init()
    game = Game(WINDOW_W, WINDOW_H)
