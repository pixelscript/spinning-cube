import app
import math
from tildagonos import tildagonos
from app_components import clear_background
from events.input import Buttons, BUTTON_TYPES
from system.eventbus import eventbus
from system.patterndisplay.events import *
from tildagonos import tildagonos
import asyncio
class Cube:
    def __init__(self, size):
        self.size = size
        self.vertices = [
            [-size, -size, -size],
            [size, -size, -size],
            [size, size, -size],
            [-size, size, -size],
            [-size, -size, size],
            [size, -size, size],
            [size, size, size],
            [-size, size, size]
        ]
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

    def rotate(self, angle_x, angle_y, angle_z):
        cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
        cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
        cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)

        for vertex in self.vertices:
            x, y, z = vertex
            # Rotate around x-axis
            y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
            vertex[1], vertex[2] = y, z
            # Rotate around y-axis
            x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
            vertex[0], vertex[2] = x, z
            # Rotate around z-axis
            x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z
            vertex[0], vertex[1] = x, y

class SpinningCube(app.App):
    def __init__(self):
        eventbus.emit(PatternDisable())
        self.currentLed = 0
        self.trail_length = 1
        self.button_states = Buttons(self)
        self.cube = Cube(0.4)
        self.colors = [
            (1, 1, 1), (0, 1, 0), (1, 0, 0), (0, 0, 1),
            (1, 1, 0), (0, 1, 1), (1, 0, 1), (1, 0.5, 0),
            (0.5, 0, 0.5), (0.5, 0.5, 0.5)
        ]
        self.colors_neo = [
            (255, 255, 255),  # White
            (0, 255, 0),      # Green
            (255, 0, 0),      # Red
            (0, 0, 255),      # Blue
            (255, 255, 0),    # Yellow
            (0, 255, 255),    # Cyan
            (255, 0, 255),    # Magenta
            (255, 128, 0),    # Orange
            (128, 0, 128),    # Purple
            (128, 128, 128)   # Gray
        ]
        self.current_color_index = 0
        self.angle_x, self.angle_y, self.angle_z = 0.05, 0.05, 0.10
        self.trail = []

    def _make_black(self):
        asyncio.sleep(0.5)
        for i in range(1, 13):
            tildagonos.leds[i] = (0, 0, 0)
        tildagonos.leds.write()
    
    def make_next_white(self):
        for i in range(1, 13):
            if self.currentLed == i:
                tildagonos.leds[i] = (self.colors_neo[self.current_color_index])
            else:
                tildagonos.leds[i] = (0, 0, 0)
        self.currentLed += 1
        if self.currentLed > 12:
            self.currentLed = 1
        tildagonos.leds.write()
        
    def update(self, delta):
        self.make_next_white()
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

        if self.button_states.get(BUTTON_TYPES["RIGHT"]):
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
            self.button_states.clear()

        if self.button_states.get(BUTTON_TYPES["CONFIRM"]):
            self.angle_y += 0.05
            if self.angle_y >= 0.5:
               self.angle_y = 0
            self.button_states.clear()

        if self.button_states.get(BUTTON_TYPES["LEFT"]):
           self.angle_z += 0.05
           if self.angle_z >= 0.5:
               self.angle_z = 0
           self.button_states.clear()

        if self.button_states.get(BUTTON_TYPES["UP"]):
            self.angle_x += 0.05
            if self.angle_x >= 0.5:
               self.angle_x = 0
            self.button_states.clear()

        if self.button_states.get(BUTTON_TYPES["DOWN"]):
            self.trail_length += 1
            if self.trail_length >= 8:
               self.trail_length = 1
            self.button_states.clear()

        self.cube.rotate(self.angle_x, self.angle_y, self.angle_z)
        self.trail.append([vertex.copy() for vertex in self.cube.vertices])
        while len(self.trail) > self.trail_length:  # Keep only the last 10 states
            self.trail.pop(0)

    def draw(self, ctx):
        clear_background(ctx)
        ctx.save()

        for i, vertices in enumerate(self.trail):
            alpha = (i + 1) / len(self.trail)  # Adjust opacity
            color = self.colors[self.current_color_index]
            ctx.rgba(color[0], color[1], color[2], alpha)  # Use rgba to set color with transparency

            for edge in self.cube.edges:
                p1 = self.project(vertices[edge[0]])
                p2 = self.project(vertices[edge[1]])
                ctx.move_to(*p1)
                ctx.line_to(*p2)
                ctx.stroke()

        ctx.restore()

    def project(self, vertex):
        fov = 500
        distance = 3
        factor = fov / (distance + vertex[2])
        x = vertex[0] * factor
        y = vertex[1] * factor
        return x, y

__app_export__ = SpinningCube
