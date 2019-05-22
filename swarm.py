from vpython import *
from surface import *

scene.width = 1000
scene.height = 700
scene.caption = "Particle Swarm Optimisation"
scene.range = 15

grid_size = 100
domain = 2 * np.pi
coord_center = vec(0, 0, 0)
axis_length = domain * 1.5
axis_width = domain * 0.01

axis_x = arrow(pos = coord_center, axis = vec(axis_length, 0, 0), 
        shaftwidth = axis_width, color = color.red)
axis_y = arrow(pos = coord_center, axis = vec(0, 0, axis_length), 
        shaftwidth = axis_width, color = color.blue)
axis_z = arrow(pos = coord_center, axis = vec(0, axis_length, 0), 
        shaftwidth = axis_width, color = color.green)


def zero_plane(x, y):
    return 0

def sinus_x(x, y):
    return sin(x)

def jecina_fja(x, y):
    return x * y
    #return sin(sqrt(x*x + y*y))
    #return sin(sin(sin(x)))*sin(sin(sin(y)))

#plane = Surface(zero_plane, domain, grid_size)
plane = Surface(sinus_x, domain, grid_size)
#plane = Surface(jecina_fja, domain, grid_size)

