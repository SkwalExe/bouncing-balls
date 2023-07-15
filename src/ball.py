from os import get_terminal_size, system
from random import randint
from math import floor
from colors import *

PURPLE_BLOCK = f'{BG_PURPLE}  {RESET}'
RED_BLOCK = f'{BG_RED}  {RESET}'
YELLOW_BLOCK = f'{BG_YELLOW}  {RESET}'
GREEN_BLOCK = f'{BG_GREEN}  {RESET}'
EMPTY = f'  '
PATH = f'. '

RED_HEART = f'{RED}❤ {RESET}'
PURPLE_HEART = f'{PURPLE}❤ {RESET}'

size = get_terminal_size()

# Divide the width by 2 to account for the fact that a block is 2 characters wide
width = floor(size.columns / 2) 
height = floor(size.lines)


def print_at(x, y, value):
    print(f"\033[{y + 1};{x * 2 + 1}H{value}", end="")

def abs(x):
    return x if x > 0 else -x


class Ball():
    def __init__(self, gravity, restitution, air_frictions, show_path, heart):
        
        self.x = width / 2
        self.y = height / 2
        self._x = int(self.x)
        self._y = int(self.y) + 1

        self.selected = False

        self.dx = 0
        self.dy = 0
        self.set_gravity(gravity)

        self.restitution = restitution
        self.air_frictions = air_frictions
        
        self.use_heart = heart

        self.show_path = show_path

    def set_gravity(self, gravity):
        self.gravity = gravity / 1000 * 2

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def wtf(self):
        self.dx = randint(-10, 10)
        self.dy = randint(-15, 15)
    
    def draw_1(self):
        # Erase old ball position
        print_at(self._x, self._y, PATH if self.show_path else EMPTY)

    def draw_2(self):
         
        # Draw new ball position
        if self.use_heart:
            print_at(int(self.x), int(self.y), RED_HEART if self.selected else PURPLE_HEART)
        else:
            print_at(int(self.x), int(self.y), RED_BLOCK if self.selected else PURPLE_BLOCK)

        self._x = int(self.x)
        self._y = int(self.y)


    def update(self):
        # Bounce off the edges
        if (int(self.x) <= 0 and self.dx < 0) or (int(self.x) >= width - 1 and self.dx > 0):
            self.dx *= -self.restitution 
        if (int(self.y) <= 0 and self.dy < 0) or (int(self.y) >= height - 1 and self.dy > 0):
            self.dy *= -self.restitution 
            
        # Gravity
        # Dont make the ball fall if it's on the ground and not moving
        if int(self.y) >= height and abs(self.dy) < 0.001:
            self.dy = 0
        else:
            self.dy += self.gravity
        
        # Ground Friction
        if int(self.y) >= height and int(self.y) == self._y:
            self.dx *= 0.99

        # Air Friction
        if self.air_frictions:
            self.dx *= 0.999
            self.dy *= 0.999


        # Move the ball according to its velocity
        self.x += self.dx
        self.x = max(0, min(self.x, width - 1))
        self.y += self.dy
        self.y = max(0, min(self.y, height - 1))
