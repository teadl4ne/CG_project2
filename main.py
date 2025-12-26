import glfw
import glm
import time
from OpenGL.GL import *

from shader import Shader
from camera import Camera
from mesh import create_sphere, create_pyramid
from texture import load_texture_raw

WIDTH, HEIGHT = 1280, 800
last_x, last_y = WIDTH//2, HEIGHT//2
first_mouse = True

def mouse_callback(w,x,y):
    global last_x,last_y,first_mouse
    cam = glfw.get_window_user_pointer(w)
    if first_mouse:
        last_x,last_y=x,y
        first_mouse=False
    cam.process_mouse(x-last_x,last_y-y)
    last_x,last_y=x,y

def scroll_callback(w,xo,yo):
    glfw.get_window_user_pointer(w).process_scroll(yo)

def main():
    glfw.init()
    window = glfw.create_window(WIDTH,HEIGHT,"CG Practical 2",None,None)
    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)

    camera = Camera()
    glfw.set_window_user_pointer(window,camera)
    glfw.set_cursor_pos_callback(window,mouse_callback)
    glfw.set_scroll_callback(window,scroll_callback)
    glfw.set_input_mode(window,glfw.CURSOR,glfw.CURSOR_DISABLED)

    shader = Shader()

    sphere = create_sphere()
    pyramid = create_pyramid()

    water = load_texture_raw("textures/waternoise.bmp")
    stone = load_texture_raw("textures/stonenoise.bmp")

    start=time.time()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        camera.process_keyboard(window)

        glClearColor(0.01,0.01,0.03,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        shader.use()
        shader.set_mat4("view",camera.view())
        shader.set_mat4("proj",glm.perspective(glm.radians(camera.fov),WIDTH/HEIGHT,0.1,100))
        shader.set_vec3("viewPos",camera.pos)

        shader.set_vec3("lightPos1",glm.vec3(0,0,0))
        shader.set_vec3("lightColor1",glm.vec3(1.8,1.3,0.8))
        shader.set_vec3("lightPos2",glm.vec3(-6,3,-4))
        shader.set_vec3("lightColor2",glm.vec3(0.2,0.3,0.6))

        t=time.time()-start
        shader.set_float("time",t*0.05)
        glActiveTexture(GL_TEXTURE0)
        shader.set_int("noiseTex",0)

        # Sun
        glBindTexture(GL_TEXTURE_2D,water)
        shader.set_bool("emissive",True)
        shader.set_vec3("baseColor",glm.vec3(1.1,0.6,0))
        shader.set_mat4("model",glm.scale(glm.mat4(1),glm.vec3(1.3)))
        sphere.draw()

        # Planet
        glBindTexture(GL_TEXTURE_2D,stone)
        shader.set_bool("emissive",False)
        shader.set_vec3("baseColor",glm.vec3(0.5,0.75,1.0))
        angle=t*0.1
        model=glm.translate(glm.mat4(1),glm.vec3(4*glm.cos(angle),0,4*glm.sin(angle)))
        model=glm.scale(model,glm.vec3(0.8))
        shader.set_mat4("model",model)
        sphere.draw()

        # Random cosmic body / pyramid
        model=glm.translate(glm.mat4(1),glm.vec3(-4,1.5,0))
        model=glm.rotate(model,t*0.1,glm.vec3(0.5,1,0.2))
        model=glm.scale(model,glm.vec3(0.6))
        shader.set_vec3("baseColor",glm.vec3(0.6,0.6,0.6))
        shader.set_mat4("model",model)
        pyramid.draw()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__=="__main__":
    main()
