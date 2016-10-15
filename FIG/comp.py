#!/usr/bin/python
from gen import Gen, AnnularCompGen, EmbeddedCompGen
from serp_concept import CylSurf, ConeSurf, PzSurf
from comparable_object import CmpObj
from types import *
from mat import Mat
from numbers import Number


class Comp(CmpObj):

    '''
    a Comp is a component in the reactor core
    TRISO particle, fuel pebble, reflector or any physical component are
    all inherant from this class
    '''

    def __init__(self, temp, name, mat_list, gen=Gen(), fill=None):
        assert isinstance(temp, Number), '''
        temp is not a number:%r''' % temp
        assert isinstance(name, str), "name is not a string:%r" % name
        assert isinstance(
            mat_list, list), "%r mat_list is not a list:%r" % (
            name, mat_list)
        assert all(isinstance(x, Mat) for x in mat_list), '''mat_list contains
        non mat object: %r''' % mat_list
        self.mat_list = mat_list  # self.collect_mat()
        self.gen = gen
        self.fill = fill
        CmpObj.__init__(self, temp, name)

    def generate_output(self):
        '''
        using generator to generate output
        '''
        return self.gen.parse(self, 's')

    def generate_capture_detector(self):
        return self.gen.parse_capture_det(self, 's')


class AnnularComp(Comp):
    # general core component with the geometry that can be described by 4 or
    # less surfaces: surf_i, surf_o are inside and outside surfaces, normally
    # cylindrical  or conical; surf_t, surf_b are top and bottom surfaces,
    # normally flat

    def __init__(
            self,
            temp,
            name,
            mat_list,
            surf_i,
            surf_o,
            surf_t=None,
            surf_b=None,
            fill=None):
        Comp.__init__(self, temp, name, mat_list, AnnularCompGen(), fill=fill)
        self.surf_list = []
        self.surf_list.append(surf_i)
        self.surf_list.append(surf_o)
        self.surf_list.append(surf_b)
        self.surf_list.append(surf_t)


class EmbeddedComp(Comp):
    '''
    one comp inside another, eg:center reflector with coolant channels
    as implemented currently, it only works for cylindrical children comps
    '''
    def __init__(self, mother_comp, children_comps):
        '''
        mother_comp: the main component
        children_comps: a dictionary of the smaller component
        inside the mother_component
        '''
        self.mother_comp = mother_comp
        self.children_comps = children_comps
        self.gen = EmbeddedCompGen()


class TruncConeComp(AnnularComp):

    def __init__(
            self,
            temp,
            name,
            mat_list,
            zb,
            zt,
            z_cone,
            h_cone,
            r,
            x=0,
            y=0,
            fill = None):
        tsurf = PzSurf(zt)
        bsurf = PzSurf(zb)
        osurf = ConeSurf(r, h_cone, z_cone, x, y)
        AnnularComp.__init__(self, temp, name, mat_list, None, osurf,
                             tsurf, bsurf, fill)


class AnnuCylComp(AnnularComp):
    # a component between two cylinders

    def __init__(self, temp, name, mat_list, ri, ro, zb, zt,
                 xi=0.0, yi=0.0, xo=0.0, yo=0.0, fill=None):
        self.ri = ri
        self.ro = ro
        self.zb = zb
        self.zt = zt
        self.xi = xi
        self.yi = yi
        self.xo = xo
        self.yo = yo
        surf_i = CylSurf(ri, zb, zt)
        surf_o = CylSurf(ro, zb, zt)
        tsurf = PzSurf(zt)
        bsurf = PzSurf(zb)
        AnnularComp.__init__(self, temp, name, mat_list,
                             surf_i, surf_o, tsurf, bsurf, fill)


class AnnuCylConeComp(AnnularComp):
    # a component inside a cylinder and outside of a cone

    def __init__(self, temp, name, mat_list, ri, hi, zi, ro, zb, zt,
                 xi=0.0, yi=0.0, xo=0.0, yo=0.0, fill=None):
        self.ri = ri
        self.hi = hi
        self.zi = zi
        self.ro = ro
        self.zb = zb
        self.zt = zt
        self.xi = xi
        self.yi = yi
        self.xo = xo
        self.yo = yo
        surf_i = ConeSurf(ri, hi, zi, xi, yi)
        surf_o = CylSurf(ro, zb, zt, xo, yo)
        tsurf = PzSurf(zt)
        bsurf = PzSurf(zb)
        AnnularComp.__init__(self, temp, name, mat_list,
                             surf_i, surf_o, tsurf, bsurf, fill)


class AnnuConeCylComp(AnnularComp):
    # a component outside of a cylinder and inside a cone

    def __init__(self,  temp, name, mat_list, ro, ho, zo, ri, zb, zt,
                 xi=0.0, yi=0.0, xo=0.0, yo=0.0, fill=None):
        self.ro = ro
        self.ho = ho
        self.zo = zo
        self.ri = ri
        self.zb = zb
        self.zt = zt
        self.xi = xi
        self.yi = yi
        self.xo = xo
        self.yo = yo
        surf_i = CylSurf(ri, zb, zt, xi, yi)
        surf_o = ConeSurf(ro, ho, zo, xo, yo)
        surf_t = PzSurf(zt)
        surf_b = PzSurf(zb)
        AnnularComp.__init__(self,  temp, name, mat_list,
                             surf_i, surf_o, surf_t, surf_b, fill)


class AnnuConeConeComp(AnnularComp):

    def __init__(self,  temp, name, mat_list, ri, hi, zi, ro, ho, zo, zb, zt,
                 xi=0.0, yi=0.0, xo=0.0, yo=0.0, fill = None):
        self.ri = ri
        self.hi = hi
        self.zi = zi
        self.ro = ro
        self.ho = ho
        self.zb = zb
        self.zt = zt
        self.xi = xi
        self.yi = yi
        self.xo = xo
        self.yo = yo
        surf_i = ConeSurf(ri, hi, zi, xi, yi)
        surf_o = ConeSurf(ro, ho, zo, xo, yo)
        surf_t = PzSurf(zt)
        surf_b = PzSurf(zb)
        AnnularComp.__init__(self,  temp, name, mat_list,
                             surf_i, surf_o, surf_t, surf_b, fill)


class CylComp(AnnularComp):
    # a cylindrical component

    def __init__(self, temp, name, mat_list, zb, zt, r, x=0, y=0, fill = None):
        surf = CylSurf(r, zb, zt, x, y)
        tsurf = PzSurf(zt)
        bsurf = PzSurf(zb)
        AnnularComp.__init__(self, temp, name, mat_list,
                             None, surf, tsurf, bsurf, fill)


class ConeComp(AnnularComp):
    # a component inside a conical surface

    def __init__(
            self,
            temp,
            name,
            mat_list,
            zb,
            zt,
            z_cone,
            h_cone,
            r,
            x=0,
            y=0,
            fill = None):
        surf = ConeSurf(r, h_cone, z_cone, x, y)
        AnnularComp.__init__(self,  temp, name, mat_list, None, surf, fill = fill)
