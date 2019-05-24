from particle import *
import random

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

class ParticleSwarm:
    def __init__(self, function, swarm_size, 
            domain, cognitive, social, mode, neighbour_size, vel_limit, start_vel):
        self.function = function
        self.swarm_size = swarm_size
        self.cognitive = cognitive
        self.social = social
        self.vel_limit = vel_limit
        self.mode = mode
        self.neighbour_size = neighbour_size / 100
        self.end = False

        self.swarm = []
        for i in range(swarm_size):
            self.swarm.append(Particle(
                function,
                random.uniform(-domain, domain),
                random.uniform(-domain, domain),
                random.uniform(-start_vel, start_vel),
                random.uniform(-start_vel, start_vel)))

        self.init_neighbourhoods()

    def init_neighbourhoods(self):
        if self.mode == "gbest":
            self.global_best = self.swarm[0].position
            for p in self.swarm[1:]:
                if p.position.y < self.global_best.y:
                    self.global_best = p.position
        elif self.mode == "ring":
            neighbourhood_size = int(self.neighbour_size * self.swarm_size)
            for i, particle in enumerate(self.swarm):
                for j in range(neighbourhood_size // 2):
                    left_neighbour = i - 1 - j
                    right_neighbour = (i + 1 + j) % self.swarm_size
                    particle.neighbours.append(self.swarm[left_neighbour])
                    particle.neighbours.append(self.swarm[right_neighbour])
        elif self.mode == "4 clusters":
            # Podela cestica roja u 4 klastera
            clusters = {0:[], 1:[], 2:[], 3:[]}
            for i, p in enumerate(self.swarm):
                clusters[i % 4].append(p)

            # Unutar svakog klastera, sve cestice su komsije jedna drugoj
            for i in range(4):
                for j, p1 in enumerate(clusters[i]):
                    for k, p2 in enumerate(clusters[i]):
                        if j != k:
                            p1.neighbours.append(p2)
                            p2.neighbours.append(p1)

            # Veze izmedju 4 klastera   
            self.connect_particles(clusters[0][0], clusters[1][0])
            self.connect_particles(clusters[0][1], clusters[2][0])
            self.connect_particles(clusters[0][2], clusters[3][0])
            self.connect_particles(clusters[1][1], clusters[2][1])
            self.connect_particles(clusters[1][2], clusters[3][1])
            self.connect_particles(clusters[2][2], clusters[3][2])

    def connect_particles(self, p1, p2):
        p1.neighbours.append(p2)
        p2.neighbours.append(p1)

    def update_velocity(self, p):
        rx1 = random.uniform(0, 1)
        rx2 = random.uniform(0, 1)
        rz1 = random.uniform(0, 1)
        rz2 = random.uniform(0, 1)

        if self.mode == "gbest":
            local_best = self.global_best
        else:
            local_best = p.neighbourhood_best

        new_x = \
            p.velocity_x +\
            self.cognitive * rx1 * (p.personal_best.x - p.position.x) +\
            self.social * rx2 * (local_best.x - p.position.x)

        new_z = \
            p.velocity_z +\
            self.cognitive * rz1 * (p.personal_best.z - p.position.z) +\
            self.social * rz2 * (local_best.z - p.position.z)

        new_x = clamp(new_x, -self.vel_limit, self.vel_limit)
        new_z = clamp(new_z, -self.vel_limit, self.vel_limit)
            
        p.set_velocity(new_x, new_z)

    def destroy(self):
        self.end = True
        for p in self.swarm:
            p.destroy()
            del p

    def stopping_condition_reached(self):
        return self.end

    def simulate(self):
        if not self.stopping_condition_reached():
            for particle in self.swarm:
                particle.update_personal_best()
                if self.mode == "gbest":
                    if self.global_best.y > particle.personal_best.y:
                        self.global_best = vec(particle.personal_best)
                else:
                    particle.update_neighbourhood_best()

            for particle in self.swarm:
                self.update_velocity(particle)
                particle.update_position()

