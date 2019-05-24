from vpython import *
from surface import *
from particle import *
from particleSwarm import *
import numpy as np
import random

scene.width = 1400
scene.height = 500
scene.range = 10
scene.forward = vec(0, -3, 2)
scene.title = "<b>Particle Swarm Optimisation</b> <i> Press </i> <b>--></b>"
#####################################################################
def sinus_x(x, z):
    return sin(x)

def test_f(x, z):
    #return x * z
    #return sin(sqrt(x*x + z*z))
    return sin(sin(sin(x)))*sin(sin(sin(z)))

def sin_cos(x, z):
    return sin(x) * cos(z)

def schaffers(x, z):
    t = x**2 + z**2
    return 0.5 + (sin(sqrt(t))**2 - 0.5) / (1+0.001*(t))**2

def sphere(x, z):
    return x*x + z*z

def rastrigin(x, z):
    return 20 + x*x - 10*cos(2*np.pi*x) + z*z - 10*cos(2*np.pi*z)

def booth(x, z):
    #return (x + 2*z + 7)**2 + (2*x + z - 5)**2
    return 100 * sqrt(abs(z - 0.01*x*x)) + 0.01*abs(x+10)
#####################################################################
grid_size = 100
swarm_size = 20
domain = 20
start_velocity = 0.00
velocity_limit = 0.005
cognitive = 0.5
social = 0.5
coord_center = vec(0, 0, 0)
mode = "gbest"
neighbour_size = 50.0

test_function = schaffers

should_draw_plane = False
plane = Surface(test_function, domain, grid_size)
optimization = None
running = False

def start():
    global should_draw_plane, plane, optimization, running
    if should_draw_plane:
        running = False
        plane.destroy()
        plane = Surface(test_function, domain, grid_size)
        should_draw_plane = False

    if optimization is not None:
        optimization.destroy()

    optimization = ParticleSwarm(
            test_function, swarm_size, domain, cognitive, social, 
            mode, neighbour_size, velocity_limit, start_velocity)
    running = True

#######################################################################
def set_cognitive(slider):
    global cognitive
    cognitive = slider.value
    texts["Cognition"].text = "{:1.2f}".format(slider.value)

def set_social(slider):
    global social
    social = slider.value
    texts["Social"].text = "{:1.2f}".format(slider.value)

def set_domain(slider):
    global domain, should_draw_plane
    domain = slider.value
    texts["Domain size"].text = "{:1.2f}".format(slider.value)
    should_draw_plane = True

def set_swarm_size(slider):
    global swarm_size
    swarm_size = int(slider.value)
    texts["Swarm size"].text = "{:1}".format(int(slider.value))

def set_neighbour_size(slider):
    global neighbour_size
    neighbour_size = slider.value
    texts["Neighbourhood size"].text = "{:1.2f}".format(slider.value)

def set_velocity_limit(slider):
    global velocity_limit
    velocity_limit = slider.value
    texts["Velocity limit"].text = "{:1.3f}".format(slider.value)

def set_start_velocity(slider):
    global start_velocity
    start_velocity = slider.value
    texts["Start velocity"].text = "{:1.3f}".format(slider.value)

def set_grid_size(slider):
    global grid_size, should_draw_plane
    grid_size = int(slider.value)
    texts["Function smoothness"].text = "{:1}".format(int(slider.value))
    should_draw_plane = True

def select_mode(m):
    global mode
    mode = m.selected

def select_function(func):
    global test_function, should_draw_plane
    if func.selected == "first":
        test_function = schaffers
    elif func.selected == "second":
        test_function = sinus_x
    elif func.selected == "third":
        test_function = sin_cos
    elif func.selected == "forth":
        test_function = booth
    should_draw_plane = True

#######################################################################
def create_slider_with_text(caption, mini, maxi, val, leng, func, off, is_int=False):
    global texts
    scene.append_to_caption("\n" + caption + ":\n")
    slide = slider(min = mini, max = maxi, value = val, length = leng,
            bind = func, right = off)
    if is_int:
        texts[caption] = wtext(text="{:1}".format(int(slide.value)))
    else:
        texts[caption] = wtext(text="{:1.2f}".format(slide.value))
#######################################################################
# UI
slider_length = 250
offset = 50
scene.caption = ("\n")
button_t = button(text='<b>Start</b>', color=color.blue, 
        bind=start, pos = scene.title_anchor)
scene.append_to_caption("Mode:  ")
menu(choices = ["gbest", "ring", "4 clusters"], index = 0, bind = select_mode)
scene.append_to_caption("               Function:  ")
menu(choices = ["first", "second", "third", "forth"], 
        index = 0, bind = select_function)

texts = {}
# COGNITION
create_slider_with_text("Cognition", 0.0, 1.0, cognitive, slider_length,
        set_cognitive, offset)
# SOCIAL
create_slider_with_text("Social", 0.0, 1.0, social, slider_length,
        set_social, offset)
# DOMAIN
create_slider_with_text("Domain size", 1.0, 30.0, domain, slider_length,
        set_domain, offset)
# SWARM SIZE
create_slider_with_text("Swarm size", 2.0, 50.0, swarm_size, slider_length,
        set_swarm_size, offset, True)
# NEIGHBOUR SIZE
create_slider_with_text("Neighbourhood size", 1.0, 100.0, neighbour_size, 
        slider_length, set_neighbour_size, offset)
# VELOCITY LIMIT
create_slider_with_text("Velocity limit", 0.0001, 0.05, velocity_limit, 
        slider_length, set_velocity_limit, offset)
# START VELOCITY
create_slider_with_text("Start velocity", 0.0, 0.05, start_velocity, 
        slider_length, set_start_velocity, offset)
# FUNCTION SMOOTHNESS
create_slider_with_text("Function smoothness", 10, 120, grid_size, 
        slider_length, set_grid_size, offset, True)
#######################################################################
# MAIN LOOP
while True:
    rate(250)
    if running:
        optimization.simulate()
