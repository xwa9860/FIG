#!/usr/bin/python


class SerpConcept(object):
    id = 1

    def __init__(self):
        SerpConcept.id += 1


class Cell(SerpConcept):
    id = 1

    def __init__(self):
        self.id = Cell.id
        Cell.id += 1


class Detector(SerpConcept):
    id = 1

    def __init__(self, text):
        self.id = Detector.id
        Detector.id += 1
        self.text = text

    def generate_output(self):
        return ('det %d %s' % (self.id, self.text))


class Universe(SerpConcept):
    id = 1

    def __init__(self):
        self.id = Universe.id
        Universe.id += 1

    def setId(self, id):
        self.id = id


class Surface:
    id = 1

    def __init__(self):
        self.id = Surface.id
        Surface.id += 1


class CylSurf(Surface):

    def __init__(self, r, z1, z2, x=0.0, y=0.0):
        Surface.__init__(self)
        self.r = r
        self.z1 = z1
        self.z2 = z2
        self.x = x
        self.y = y
        self.text = 'surf %d cylz %f %f %f %f %f\n' % (self.id, self.x,
                                                       self.y, self.r,
                                                       self.z1, self.z2)


class SphSurf(Surface):

    def __init__(self, r=0.0, x=0.0, y=0.0, z=0.0):
        Surface.__init__(self)
        self.r = r
        self.x = x
        self.y = y
        self.z = z
        self.text = 'surf %d sph %f %f %f %f\n' % (self.id, self.x, self.y,
                                                   self.z, self.r)

    def set_r(self, r0):
        self.r = r0
        self.text = 'surf %d sph %f %f %f %f\n' % (self.id, self.x, self.y,
                                                   self.z, self.r)


class ConeSurf(Surface):

    def __init__(self, r, h, z=0.0, x=0.0, y=0.0):
        Surface.__init__(self)
        self.r = r
        self.h = h
        self.z = z
        self.x = x
        self.y = y
        self.text = 'surf %d cone %f %f %f %f %f\n' % (self.id, self.x,
                                                       self.y, self.z,
                                                       self.r, self.h)


class CubeSurf(Surface):

    def __init__(self, a, x0=0.0, y0=0.0, z0=0.0):
        Surface.__init__(self)
        self.a = a
        self.text = 'surf %d cube %f %f %f  a' % (self.id, x0, y0, z0, a)


class PzSurf(Surface):

    def __init__(self, z):
        Surface.__init__(self)
        self.z = z
        self.text = 'surf %d pz %f\n' % (self.id, self.z)


class CrossSurf(Surface):

    def __init__(self, x0, y0, r, d):
        Surface.__init__(self)
        self.text = 'surf %d cross %f %f %f %f \n' % (self.id, x0, y0, r, d)
