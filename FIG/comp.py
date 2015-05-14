#!/usr/bin/python
from gen import Gen, AnnularCompGen
from serp_concept import CylSurf, ConeSurf, PzSurf
from mat import Mat
from sets import Set
from comparable_object import CmpObj


class Comp(CmpObj):

    def __init__(self, temp, name, filling, gen=Gen()):
        self.filling = filling
        self.gen = gen
        self.matSet = self.collect_mat_from_filling(self.filling)
        CmpObj.__init__(self, temp, name)

    def collect_mat_from_filling(self, filling):
        matSet = Set()
        for fil in filling:
            if isinstance(fil, Mat):
                matSet = matSet | Set([fil])
            else:
                if hasattr(fil, 'filling'):
                    matSet = matSet | self.collect_mat_from_filling(fil.filling)
                else:
                    print 'error, %s is type %s, has no attribute filling' % \
                        (fil.name, fil.__class__.__name__)
        return matSet

    def generate_output(self):
        return self.gen.parse(self, 's')

    def generate_capture_detector(self):
        return self.gen.parse_capture_det(self, 's')

    def __eq__(self, other):
        id_check = True
        if hasattr(self.gen, 'cell'):
            id_check = (self.gen.cell.id == other.gen.cell.id)
        elif hasattr(self.gen, 'univ'):
            id_check = (self.gen.univ.id == other.gen.univ.id)
        else:
            print 'this comp has no cell id or univ id'
        return (isinstance(other, self.__class__) and
                self.temp == other.temp and
                self.name == other.name and
                id_check
                )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        if not isinstance(self.name, str):
            print self.name
            print 'is not string but %s' % type(self.name)
        else:
            if hasattr(self.gen, 'cell'):
                return hash(self.__class__.__name__ +
                            self.name +
                            str(self.gen.cell.id) +
                            str(self.temp))
            elif hasattr(self.gen, 'univ'):
                return hash(self.__class__.__name__ +
                            self.name +
                            str(self.gen.univ.id) +
                            str(self.temp))
            else:
                return hash(self.__class__.__name__+self.name +
                            str(self.temp))


class AnnularComp(Comp):
    # general core component with the geometry that can be described by 4 or
    # less surfaces: surf_i, surf_o are inside and outside surfaces, normally
    # cylindrical  or conical; surf_t, surf_b are top and bottom surfaces,
    # normally flat

    def __init__(
            self,
            temp,
            name,
            filling,
            surf_i,
            surf_o,
            surf_t=None,
            surf_b=None):
        Comp.__init__(self, temp, name, filling, AnnularCompGen())
        self.surf_list = []
        self.surf_list.append(surf_i)
        self.surf_list.append(surf_o)
        self.surf_list.append(surf_b)
        self.surf_list.append(surf_t)
        self.filling = filling


class TruncConeComp(AnnularComp):

    def __init__(
            self,
            temp,
            name,
            filling,
            zb,
            zt,
            z_cone,
            h_cone,
            r,
            x=0,
            y=0):
        tsurf = PzSurf(zt)
        bsurf = PzSurf(zb)
        osurf = ConeSurf(r, h_cone, z_cone, x, y)
        AnnularComp.__init__(self,  temp, name, filling, None, osurf,
                             tsurf, bsurf)


class AnnuCylComp(AnnularComp):
    # a component between two cylinders

    def __init__(self,  temp, name, filling, ri, ro, zb, zt,
                 xi=0.0, yi=0.0, xo=0.0, yo=0.0):
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
        AnnularComp.__init__(self,  temp, name, filling,
                             surf_i, surf_o, tsurf, bsurf)


class AnnuCylConeComp(AnnularComp):
    # a component inside a cylinder and outside of a cone

    def __init__(self,  temp, name, filling, ri, hi, zi, ro, zb, zt,
                 xi=0.0, yi=0.0, xo=0.0, yo=0.0):
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
        AnnularComp.__init__(self,  temp, name, filling,
                             surf_i, surf_o, tsurf, bsurf)


class AnnuConeCylComp(AnnularComp):
    # a component outside of a cylinder and inside a cone

    def __init__(self,  temp, name, filling, ro, ho, zo, ri, zb, zt,
                 xi=0.0, yi=0.0, xo=0.0, yo=0.0):
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
        AnnularComp.__init__(self,  temp, name, filling,
                             surf_i, surf_o, surf_t, surf_b)


class AnnuConeConeComp(AnnularComp):

    def __init__(self,  temp, name, filling, ri, hi, zi, ro, ho, zo, zb, zt,
                 xi=0.0, yi=0.0, xo=0.0, yo=0.0):
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
        AnnularComp.__init__(self,  temp, name, filling,
                             surf_i, surf_o, surf_t, surf_b)


class CylComp(AnnularComp):
    # a cylindrical component

    def __init__(self,  temp, name, filling, zb, zt, r, x=0, y=0):
        surf = CylSurf(r, zb, zt, x, y)
        tsurf = PzSurf(zt)
        bsurf = PzSurf(zb)
        AnnularComp.__init__(self,  temp, name, filling,
                             None, surf, tsurf, bsurf)


class ConeComp(AnnularComp):
    # a component inside a conical surface

    def __init__(
            self,
            temp,
            name,
            filling,
            zb,
            zt,
            z_cone,
            h_cone,
            r,
            x=0,
            y=0):
        surf = ConeSurf(r, h_cone, z_cone, x, y)
        AnnularComp.__init__(self,  temp, name, filling, None, surf)
