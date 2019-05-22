from vpython import *
from surface import *
from particle import *

import random

scene.width = 1000
scene.height = 700
scene.caption = "Particle Swarm Optimisation"
scene.range = 15

grid_size = 80
swarm_size = 20
domain = 3 * np.pi
start_velocity = 0.00
velocity_limit = 0.001
cognitive = 0.2
social = 0.5
coord_center = vec(0, 0, 0)
axis_length = domain * 1.5
axis_width = domain * 0.01

axis_x = arrow(pos = coord_center, axis = vec(axis_length, 0, 0), 
        shaftwidth = axis_width, color = color.red)
axis_y = arrow(pos = coord_center, axis = vec(0, axis_length, 0), 
        shaftwidth = axis_width, color = color.green)
axis_z = arrow(pos = coord_center, axis = vec(0, 0, axis_length), 
        shaftwidth = axis_width, color = color.blue)

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

class ParticleSwarm:
    def __init__(self, function, swarm_size, 
            domain, start_vel, cognitive, social, vel_limit):
        self.function = function
        self.swarm_size = swarm_size
        self.global_best = None
        self.cognitive = cognitive
        self.social = social
        self.vel_limit = vel_limit

        self.swarm = []
        for i in range(swarm_size):
            self.swarm.append(Particle(
                function,
                random.uniform(-domain, domain),
                random.uniform(-domain, domain),
                random.uniform(-start_vel, start_vel),
                random.uniform(-start_vel, start_vel)))

    def is_better_solution(self, particle):
        return particle.personal_best.y < self.global_best.y

    def update_velocity(self, p):
        rx1 = random.uniform(0, 1)
        rx2 = random.uniform(0, 1)
        rz1 = random.uniform(0, 1)
        rz2 = random.uniform(0, 1)

        new_x = \
            p.velocity_x +\
            self.cognitive * rx1 * (p.personal_best.x - p.position.x) +\
            self.social * rx2 * (self.global_best.x - p.position.x)


        new_z = \
            p.velocity_z +\
            self.cognitive * rz1 * (p.personal_best.z - p.position.z) +\
            self.social * rz2 * (self.global_best.z - p.position.z)

        new_x = clamp(new_x, -self.vel_limit, self.vel_limit)
        new_z = clamp(new_z, -self.vel_limit, self.vel_limit)
            
        p.set_velocity(new_x, new_z)


    def simulate(self):
        while True:
            rate(250)

            for particle in self.swarm:
                particle.update_position()

                if self.global_best is None or self.is_better_solution(particle):
                    self.global_best = vec(particle.personal_best) 

                self.update_velocity(particle)

def zero_plane(x, z):
    return 0

def sinus_x(x, z):
    return sin(x)

def jecina_fja(x, z):
    return x * z
    #return sin(sqrt(x*x + z*z))
    #return sin(sin(sin(x)))*sin(sin(sin(z)))

def sin_cos(x, z):
    return sin(x) * cos(z)

def schaffers(x, z):
    return 0.5 + (sin(sqrt(x**2 + z**2))**2 - 0.5) / (1 + 0.001 * (x**2 + z**2)**2)

test_function = schaffers

plane = Surface(test_function, domain, grid_size)
optimization = ParticleSwarm(
        test_function, swarm_size, domain, start_velocity, cognitive, social, velocity_limit)
optimization.simulate()
