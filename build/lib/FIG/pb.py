#!/usr/bin/python
from pb_gen import FuelPbGen, GPbGen
from comp import Comp
from triso import Triso, TrisoLattice
from mat import Graphite, Shell, CentralGraphite
from sets import Set

class GPb(Comp):

    def __init__(self, temp):
        self.r = 1.5   # cm
        self.temp = temp
        # self.filling = {'Graphite':Graphite(self.temp)}
        self.filling = Set([Graphite(self.temp)])
        self.name = 'Graphite'+str(self.temp)
        Comp.__init__(self, self.temp, self.name, self.filling, GPbGen())


class FuelPebble(Comp):

    def __init__(self, triso, pb_kernel_temp, pb_shell_temp, dr_config=None):
        self.triso = triso
        self.tr_lat = TrisoLattice(self.triso, 8.86062E-02)
        self.filling_order =[
            'CentralGraphite',
            'TrLat',
            'Shell']
        self.filling = Set([
            CentralGraphite(pb_kernel_temp),
            self.tr_lat,
            Shell(pb_shell_temp)])|self.tr_lat.filling

        # self.filling = {
        #     'CentralGraphite':CentralGraphite(self.fuel_temp - 50),
        #     'Trlat':self.tr_lat,
        #     'Shell':Shell(self.fuel_temp - 110)}.update(self.tr_lat.filling)

        # assumptions on temperature distribution
        if not dr_config:
            self.dr_config = {
                'CentralGraphite': 1.25000, # cm
                 'TrLat': 0.15000, # cm
                'Shell': 0.1000 #cm
            }
        self.calculate_r()
        self.name = 'fuelPb'+self.tr_lat.name
        Comp.__init__(self, self.triso.temp, self.name, self.filling, FuelPbGen())

    def calculate_r(self):
        self.r_config = {}
        self.r_config['CentralGraphite'] = self.dr_config['CentralGraphite']
        for i in xrange(1, len(self.filling_order)):
            prev_name = self.filling_order[i-1]
            curr_name = self.filling_order[i]
            self.r_config[curr_name] = (self.r_config[prev_name] +
                                        self.dr_config[curr_name])
