import glm
import math

class Light:
    def __init__(self, position, color=None):
        self.position = position

        # Default white light if color not provided
        if color is None:
            self.color = glm.vec3(1.0, 1.0, 1.0)
        else:
            self.color = color

        self.angle = 0.0

    def animate(self):
        # Simple circular orbit animation
        self.angle += 0.01
        radius = 3.0

        self.position.x = math.cos(self.angle) * radius
        self.position.z = math.sin(self.angle) * radius
