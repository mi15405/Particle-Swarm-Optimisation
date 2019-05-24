from vpython import *

class Particle:
    def __init__(self, function, pos_x, pos_z, vel_x, vel_z):
        self.function = function
        self.position = vec(pos_x, function(pos_x, pos_z), pos_z)
        self.personal_best = vec(self.position)
        self.neighbourhood_best = vec(self.position)
        self.set_velocity(vel_x, vel_z)
        self.model = simple_sphere(pos = self.position, radius = 0.2)
        self.neighbours = []

    def set_position(self, x, z):
        self.position.x = x
        self.position.y = self.function(x, z)
        self.position.z = z

    def set_velocity(self, vel_x, vel_z):
        self.velocity_x = vel_x
        self.velocity_z = vel_z

    def update_personal_best(self):
        if self.position.y < self.personal_best.y:
            self.personal_best = vec(self.position)
    
    def update_neighbourhood_best(self):
        if self.personal_best.y < self.neighbourhood_best.y:
            self.neighbourhood_best = vec(self.personal_best)

        for n in self.neighbours:
            if n.personal_best.y < self.neighbourhood_best.y:
                self.neighbourhood_best = vec(n.personal_best)
    
    def update_position(self):
        self.set_position(
                self.position.x + self.velocity_x,
                self.position.z + self.velocity_z)
        self.model.pos = self.position

    def destroy(self):
        self.model.visible = False

