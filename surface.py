import numpy as np
from vpython import *

class Surface:
    def __init__(self, function, domain, grid_size):
        self.evaluate = function
        self.domain = domain
        self.grid_size = grid_size

        self.vertices = []
        segments = np.linspace(-domain, domain, grid_size)
        for x in segments:
            for y in segments:
                z = self.evaluate(x, y)
                self.vertices.append(self.make_vertex(x, y, z))

        self.make_quads()
        self.make_normals()
        compound(self.quads)
        
    def make_vertex(self, x, y, z):
        # Zamenjuju se y i z koordinate, jer je Y osa vertikalna u ovom sistemu
        return vertex(pos = vec(x, z, y), color = color.cyan, opacity = 0.5)

    def make_quads(self):
        # Povrsina se aproksimira mrezom kvadrata koja se pravi od tacaka.
        # Krecemo se po Y osi i dodajemo kvadrate, formirajuci traku kvadrata.
        # Zatim se pomerimo po X osi i tako spajamo traku po traku u mrezu kvadrata
        self.quads = []
        for x in range(self.grid_size - 1):
            for y in range(self.grid_size - 1):
                self.quads.append(quad(vs = [
                    self.get_vertex(x, y),
                    self.get_vertex(x+1, y),
                    self.get_vertex(x+1, y+1),
                    self.get_vertex(x, y+1)]))
                            
    def make_normals(self):
        # Racunanje normala tacaka, kao vektorski proizvod vektora
        # ka tacki desno i ka tacki iznad tekuce tacke.
        # Ovako se izracunavaju sve tacke osim tacaka na gornjoj i desnoj
        # ivici, jer one nemaju para desno i iznad od sebe
        for x in range(self.grid_size - 1):
            for y in range(self.grid_size - 1):
                vert = self.get_vertex(x, y)
                right = self.get_vertex(x, y+1)
                up = self.get_vertex(x+1, y)
                vert.normal = cross(right.pos - vert.pos, up.pos - vert.pos)

        # Racunanje normala gornje ivice, kao vektorski proizvod od
        # vektora ka dole i vektora ka desno od tekuce tacke
        for x in range(self.grid_size - 1):
            top = self.get_vertex(x, self.grid_size-1)
            bottom = self.get_vertex(x-1, self.grid_size-1)
            right = self.get_vertex(x+1, self.grid_size-1)
            top.normal = -cross(bottom.pos - top.pos, right.pos - top.pos)

        # Racunanje normala desne ivice, kao vektorski proizvod od 
        # vektora ka gore i vektora ka levo od tekuce tacke
        for y in range(self.grid_size - 1):
            right = self.get_vertex(self.grid_size-1, y)
            top = self.get_vertex(self.grid_size-1, y+1)
            left = self.get_vertex(self.grid_size-2, y)
            right.normal = -cross(top.pos - right.pos, left.pos - right.pos)

    def get_vertex(self, x, y):
        return self.vertices[x * self.grid_size + y]

