'''
pebble bed classes, including fuel bed, graphite pebbles bed
'''
#!/usr/bin/python
from pbed_gen import PBedGen, PBedLatGen, FCCGen, GFCCGen
from coolant import Coolant
from comp import Comp
from pb import GPb
import math


class PBed(Comp):

    '''general pebble bed class, including unit cell'''

    def __init__(self, coolant, pb_list, dir_name='serp_input/',
                 gen=PBedGen('serp_input/')):
        self.coolant = coolant
        self.pb_list = pb_list
        temp = coolant.temp
        mat_list = self.collect_mat()
        name = type(self).__name__
        Comp.__init__(self, temp, name,
                      mat_list, gen=gen)

    def collect_mat(self):
        ''' get all the materials contained in
        all the pebbles and the coolant inside the pebble bed
        and make sure no duplications in the mat_list
        Two materials are considered different if their name is different
        the material name is classType+temperature, except for the fuel, fuel
        name is defined by user at the creation of a fuel material
        '''
        mat_list = self.coolant.mat_list
        for pb in self.pb_list:
            for mat in pb.mat_list:
                if mat not in mat_list:
                    mat_list.append(mat)
        return mat_list


class FCC(PBed):
    '''Fcc unit cell
    base class for fuel pebbles and graphite pebbles
    '''
    def __init__(self, coolant, pb_list, dir_name='serp_input/',
                 gen=FCCGen('serp_input/')):
        assert(len(pb_list) == 14), "pb_list length is not 14, but %d" % len(
            pb_list)
        self.packing_fraction = 0.60
        self.pitch = math.pow(4/3.0*math.pi*math.pow(0.15, 3)*4/0.6, 1/3.0)/2
        #2.27541  # fcc pitch for 3cm diam pb at packing frac = 40%
        PBed.__init__(self, coolant, pb_list,
                      dir_name=dir_name,
                      gen=gen)


class FuelUnitCell(FCC):

    def __init__(self, fpb_list, cool_temp,
                 packing_fraction=0.60,
                 dir_name='serp_input/'):
        self.cool = Coolant(cool_temp, 'FuelFCCCoolant')
        FCC.__init__(self, self.cool, fpb_list,
                     dir_name=dir_name,
                     gen=FCCGen(dir_name))
        # TODO: calculate pitch from packing fraction and update FCC class to
        # receive pitch from constructor


class GraphiteUnitCell(FCC):

    def __init__(self, pb_temp, cool_temp,
                 packing_fraction=0.60,
                 dir_name='serp_input/'):
        '''
        assuming all the graphite pebbles in an FCC unit cell are identical
        '''
        cool = Coolant(cool_temp, 'GFCCCoolant')
        gpb_list = []
        for i in range(0, 14):
            gpb_list.append(GPb(pb_temp, dir_name))
        FCC.__init__(
            self,
            cool,
            gpb_list,
            dir_name=dir_name,
            gen=GFCCGen(dir_name))


class PBedLat(Comp):

    ''' Lattice of pebble bed(Fcc unit cell) '''

    def __init__(self, pbed, pitch, dir_name='serp_input'):
        ''' arg:
            pbed: fuel pebble or graphite pebble unit cell
            pitch: pitch between two fcc unit cells
        '''
        name = 'pbedLat' + pbed.name
        self.pitch = pitch
        mat_list = pbed.mat_list
        self.pbed = pbed
        Comp.__init__(self, pbed.temp, name,
                      mat_list, gen=PBedLatGen(dir_name))
