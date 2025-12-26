import glm
import glfw

class Camera:
    def __init__(self):
        self.pos = glm.vec3(0, 0, 9)
        self.front = glm.vec3(0, 0, -1)
        self.up = glm.vec3(0, 1, 0)

        self.yaw = -90
        self.pitch = 0
        self.fov = 45

        self.speed = 0.05        # REDUCED SPEED
        self.sensitivity = 0.1

    def view(self):
        return glm.lookAt(self.pos, self.pos + self.front, self.up)

    def process_keyboard(self, window):
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.pos += self.speed * self.front
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.pos -= self.speed * self.front
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.pos -= glm.normalize(glm.cross(self.front, self.up)) * self.speed
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.pos += glm.normalize(glm.cross(self.front, self.up)) * self.speed

    def process_mouse(self, dx, dy):
        self.yaw += dx * self.sensitivity
        self.pitch += dy * self.sensitivity
        self.pitch = max(-89, min(89, self.pitch))

        direction = glm.vec3(
            glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch)),
            glm.sin(glm.radians(self.pitch)),
            glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        )
        self.front = glm.normalize(direction)

    def process_scroll(self, yoffset):
        self.fov -= yoffset
        self.fov = max(20, min(80, self.fov))
