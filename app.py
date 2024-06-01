import app
import math
from tildagonos import tildagonos
from app_components import clear_background
from events.input import Buttons, BUTTON_TYPES

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
        self.angle = 0

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
        self.button_states = Buttons(self)
        self.cube = Cube(0.3)
        self.colors = [
            (1, 1, 1),  # White
            (0, 1, 0),  # Green
            (1, 0, 0),  # Red
            (0, 0, 1),  # Blue
            (1, 1, 0),  # Yellow
            (0, 1, 1),  # Cyan
            (1, 0, 1),  # Magenta
            (1, 0.5, 0),  # Orange
            (0.5, 0, 0.5),  # Purple
            (0.5, 0.5, 0.5)  # Gray
        ]
        self.current_color_index = 0

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

        if self.button_states.get(BUTTON_TYPES["RIGHT"]):
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
            self.button_states.clear()

        self.cube.rotate(0.01, 0.02, 0.03)

    def draw(self, ctx):
        clear_background(ctx)
        ctx.save()

        current_color = self.colors[self.current_color_index]
        ctx.rgb(*current_color)

        for edge in self.cube.edges:
            p1 = self.project(self.cube.vertices[edge[0]])
            p2 = self.project(self.cube.vertices[edge[1]])
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
