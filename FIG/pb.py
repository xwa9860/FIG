#!/usr/bin/python
from pb_gen import FuelPbGen, GPbGen
from comp import Comp
from triso import TrisoLattice
from mat import Graphite, Shell, CentralGraphite


class GPb(Comp):

    def __init__(self, temp, dir_name='serp_input/'):
        self.r = 1.5   # cm
        self.temp = temp
        # self.filling = {'Graphite':Graphite(self.temp)}
        self.mat_list = [Graphite(temp)]
        self.name = 'Graphite'+str(self.temp)
        Comp.__init__(self, self.temp, self.name, self.mat_list, GPbGen(dir_name))


class FPb(Comp):

    def __init__(self, triso, cg_temp, shell_temp, dir_name='serp_input/'):
        '''
        cg_temp: central graphite kernel temperature
        '''
        self.triso = triso
        self.tr_lat = TrisoLattice(self.triso)
        self.layer = [
            'CentralGraphite',
            'TrLat',
            'Shell']
        mat = [CentralGraphite(cg_temp), Shell(shell_temp)]
        mat.extend(self.tr_lat.mat_list)
        self.dr_config = {
            'CentralGraphite': 1.25000,  # cm
            'TrLat': 0.15000,  # cm
            'Shell': 0.1000  # cm
        }
        self.calculate_r()
        self.name = 'fuelPb'+self.tr_lat.name
        Comp.__init__(
            self,
            self.triso.temp,
            self.name,
            mat,
            FuelPbGen(dir_name))

    def calculate_r(self):
        self.r_config = {}
        self.r_config['CentralGraphite'] = self.dr_config['CentralGraphite']
        for i in range(1, len(self.layer)):
            prev_name = self.layer[i-1]
            curr_name = self.layer[i]
            self.r_config[curr_name] = (self.r_config[prev_name] +
                                        self.dr_config[curr_name])
