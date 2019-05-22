from vpython import *

class Particle:
    def __init__(self, function, pos_x, pos_z, vel_x, vel_z):
        self.function = function
        self.position = vec(pos_x, function(pos_x, pos_z), pos_z)
        self.personal_best = vec(self.position)
        self.set_position(pos_x, pos_z)
        self.set_velocity(vel_x, vel_z)
        self.model = simple_sphere(pos = self.position, radius = 0.2)

    def set_position(self, x, z):
        self.position.x = x
        self.position.y = self.function(x, z)
        self.position.z = z

    def set_velocity(self, vel_x, vel_z):
        self.velocity_x = vel_x
        self.velocity_z = vel_z
    
    def update_position(self):
        self.set_position(
                self.position.x + self.velocity_x,
                self.position.z + self.velocity_z)

        if self.position.y < self.personal_best.y:
            self.personal_best = vec(self.position)

        self.model.pos = self.position

