from random import choice, randint
import pymunk.pygame_util
from consts import *


class Hole:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {}
        self.color = WHITE

    def coord(self):
        return self.x, self.y


class Node:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {
            'up': True,
            'down': True,
            'left': True,
            'right': True
        }
        self.visited = False
        self.color = choice((NODE_COLOR1, NODE_COLOR2))

    def coord(self):
        return self.x, self.y

    def delete_wall(self, direction):
        self.walls[direction] = False

    def __sub__(self, other):
        k = {
            (0, 1): ('up', 'down'),
            (0, -1): ('down', 'up'),
            (1, 0): ('left', 'right'),
            (-1, 0): ('right', 'left'),
        }
        x1, y1 = self.coord()
        x2, y2 = other.coord()
        return k.get((x1 - x2, y1 - y2))


class Maze:
    def __init__(self, width=None, height=None, hole_percent=10):
        self.w, self.h = width, height
        if self.w is None:
            self.w = randint(6, 9)
        if self.h is None:
            self.h = randint(4, 6)
        self.field = None
        self.hole_percent = hole_percent

    def generate(self):
        self.field = [[Node(x, y) for x in range(self.w)] for y in range(self.h)]
        n_holes = self.w * self.h * self.hole_percent // 100
        for _ in range(n_holes):
            x, y = randint(0, self.w - 1), randint(0, self.h - 1)
            if (x, y) != (0, 0):
                self.field[y][x] = Hole(x, y)

        current_node = self.get_node(0, 0)
        current_node.visited = True
        stack = [current_node]
        while stack:
            current_node = stack[-1]
            next_nodes = self.next_nodes(current_node)
            if next_nodes:
                next_node = choice(next_nodes)
                next_node.visited = True
                wall1, wall2 = current_node - next_node
                current_node.delete_wall(wall1)
                next_node.delete_wall(wall2)
                stack.append(next_node)
            else:
                stack.pop()

        for y, row in enumerate(self.field):
            for x, node in enumerate(row):
                if isinstance(node, Node) and all(node.walls[wall] for wall in node.walls):
                    self.field[y][x] = Hole(x, y)
        if not any(isinstance(self.get_node(x, y), Node) for x in range(self.w) for y in (self.h - 1, )) or \
                not any(isinstance(self.get_node(x, y), Node) for x in (self.w - 1, ) for y in range(self.h)):
            self.generate()

    def next_nodes(self, node):
        directions = (0, 1), (0, -1), (1, 0), (-1, 0)
        x, y = node.coord()
        return [self.get_node(x + dx, y + dy) for dx, dy in directions
                if self.on_field(x + dx, y + dy) and isinstance(self.get_node(x + dx, y + dy), Node) and
                not self.get_node(x + dx, y + dy).visited]

    def on_field(self, x, y):
        return self.w > x >= 0 <= y < self.h

    def get_node(self, x, y):
        return self.field[y][x]


class Wall:
    def __init__(self, x, y, w, h, space):
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.position = x, y
        shape = pymunk.Poly.create_box(body, (w, h))
        shape.elasticity = 1.
        space.add(body, shape)
        self.body = body
        self.w, self.h = w, h


if __name__ == '__main__':
    import pygame as pg

    W, H = 1366, 768
    MAZE_W, MAZE_H = randint(6, 9), randint(4, 6)
    A = min(W // MAZE_W, H // MAZE_H)
    BORDER_W = A // 12
    WALL_DRAW = {
        'up': (0, 0, A, 0),
        'down': (0, A, A, A),
        'left': (0, 0, 0, A),
        'right': (A, 0, A, A),
    }

    pg.init()

    screen = pg.display.set_mode((W, H))
    maze = Maze(MAZE_W, MAZE_H)
    maze.generate()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        screen.fill('white')
        for y, row in enumerate(maze.field):
            for x, node in enumerate(row):
                if isinstance(node, Node):
                    pg.draw.rect(screen, 'lightgray', (x * A, y * A, A, A))
        for y, row in enumerate(maze.field):
            for x, node in enumerate(row):
                if isinstance(node, Node):
                    walls = node.walls
                    for wall in walls:
                        if walls[wall]:
                            x1, y1, x2, y2 = WALL_DRAW.get(wall)
                            pg.draw.line(screen, 'darkgray',
                                         (x * A + x1, y * A + y1),
                                         (x * A + x2, y * A + y2), BORDER_W)
        pg.display.update()
