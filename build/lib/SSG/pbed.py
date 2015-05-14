#!/usr/bin/python
from pbed_gen import PBedGen, PBedLatGen, FCCGen, GFCCGen
from coolant import Coolant
from comp import Comp
from pb import FuelPebble, GPb
from triso import Triso
from mat import Fuel
from sets import Set


class PBed(Comp):

    def __init__(self, temp, name, surrounding, pb_list, gen=PBedGen()):
        self.surrounding = surrounding
        self.pb_list = pb_list
        self.collect_fillings()
        self.input_file = 'pb_pos.inp'
        Comp.__init__(self, temp, name, self.filling, gen)

    def collect_fillings(self):
        self.filling = Set([self.surrounding]) | self.surrounding.filling
        for pb in self.pb_list:
            # self.filling = self.filling.update(pb.filling)
            self.filling = self.filling | pb.filling


class PBedLat(Comp):

    def __init__(self, pbed, pitch):
        self.pbed = pbed
        self.temp = pbed.temp
        self.name = 'pbedLat' + pbed.name
        self.pitch = pitch
        self.filling = Set([self.pbed]) | self.pbed.filling
        Comp.__init__(self, self.temp, self.name, self.filling, PBedLatGen())


class FCC(PBed):

    def __init__(self, temp, name,
                 surrounding, pb_list, pb_pos_file_name, gen=FCCGen()):
        assert (len(pb_list) ==14), "pb_list length is not 14, but %d" %len(pb_list)
        PBed.__init__(self, temp, name, surrounding, pb_list, gen)
        self.p = 2.27541  # fcc pitch for 3cm diam pb at packing frac = 40%
        self.input_file = pb_pos_file_name


class FuelFCC(FCC):

    def __init__(self, fpb_list, cool_temp, pb_pos_file_name):
        # list of temperatures:central graphie kernel;
        # fuel, buffer, iPyC, SiC, oPyC, matrix; shell
        assert (len(fpb_list) ==14), "pb_list length is not 14, but %d" %len(fpb_list)
        self.cool_temp = cool_temp
        self.cool = Coolant(cool_temp, 'FuelFCCCoolant')
        temp = cool_temp
        # this temp is only an identifier for the FCC, is not used for any calculati            on
        name = 'fuel_unit_cell'
        FCC.__init__(self,
                     temp,
                     name, self.cool, fpb_list, pb_pos_file_name)


class GFCC(FCC):

    def __init__(self, pb_temp, cool_temp, pb_pos_input_name):
        # ''' assuming all the graphite pebbles in an FCC unit cell are identical'''
        self.cool = Coolant(cool_temp, 'GFCCCoolant')
        # define the 8 fuel pebbles
        self.gpb_list = []
        self.gpb = GPb(pb_temp)
        for i in xrange(0, 14):
            self.gpb_list.append(self.gpb)
        name = 'graphite_unit_cell'
        FCC.__init__(
            self,
            pb_temp,
            name,
            self.cool,
            self.gpb_list,
            pb_pos_input_name,
            GFCCGen())
