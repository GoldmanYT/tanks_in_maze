import pymunk.pygame_util
from pymunk import Vec2d
from math import sin, cos
from consts import BULLET_V
# from math import pi
# from random import random


class Bullet:
    def __init__(self, x, y, r, direction, space):
        ball_body = pymunk.Body(1, float('inf'))
        ball_body.position = x, y

        ball_shape = pymunk.Circle(ball_body, r)
        ball_shape.elasticity = 1.0

        a = direction
        # a = random() * 2 * pi
        ball_body.apply_impulse_at_local_point(Vec2d(cos(a), sin(a)))

        def constant_velocity(body, gravity, damping, dt):
            body.velocity = body.velocity.normalized() * BULLET_V

        ball_body.velocity_func = constant_velocity

        space.add(ball_body, ball_shape)
