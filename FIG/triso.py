#!/usr/bin/python
from triso_gen import TrisoGen
from triso_gen import TrisoLatticeGen
from comp import Comp
from mat import Buffer, iPyC, SiC, oPyC, Matrix
import math


class Triso(Comp):

    def __init__(self,
                 temp_list, 
                 fuel_list, 
                 dr_config=None, 
                 dir_name='serp_input'):
        '''
        fuel: fuel material in a list
        dr_config: thickness of the layers
        '''
        # material
        self.mat_list = []
        print(temp_list)
        if not dr_config:
            assert len(temp_list) == 5, 'wrong temperature number %d' %(len(temp_list))
            for fuel in fuel_list:
                self.mat_list.append(fuel)
            self.mat_list.extend([Buffer(temp_list[0]),
                                  iPyC(temp_list[1]),
                                  SiC(temp_list[2]),
                                  oPyC(temp_list[3]),
                                  Matrix(temp_list[4])])
        else:
            print('not implementd')

        if not dr_config:
            r_3 = 0.02
            r_1 = ((r_3**3.0)/3.0)**(1/3.0)
            r_2 = ((r_3**3.0)/1.5)**(1/3.0)
            dr_list = [r_1, r_2 - r_1, r_3 - r_2, 0.01, 0.0035, 0.0035, 0.0035]
            self.dr_config = {}
            for i, dr in enumerate(dr_list):
                self.dr_config[self.mat_list[i].name] = dr
        else:
            self.dr_config = dr_config

        assert len(temp_list) + len(fuel_list) == 1 + len(self.dr_config), '''
        temp_list and fuel_list for triso particle needs %d
        temperature values, got %d and %d''' % (len(self.dr_config),
                                                len(temp_list),
                                                len(fuel_list))
        name = 'triso'+fuel.name
        self.calculate_r()
        Comp.__init__(self, fuel.temp, name, self.mat_list, TrisoGen(dir_name))
        # triso temp defined as fuel temp, which is expected to be the highest
        # thus most important to safety analysis

    def calculate_r(self):
        self.r_config = {}
        self.r_config[self.mat_list[0].name] =\
        self.dr_config[self.mat_list[0].name]
        for i in range(1, len(self.mat_list)-1):
            prev_name = self.mat_list[i-1].name
            curr_name = self.mat_list[i].name
            self.r_config[curr_name] = self.r_config[
                prev_name] + self.dr_config[curr_name]

    #def volume(self):
        # This method finds the volumes of all the constituents of the TRISO
        # particle

         #self.r_Fuel = self.dr_Fuel
         #self.r_Buffer = self.r_Fuel + self.dr_Buffer
         #self.r_iPyC = self.r_Buffer + self.dr_iPyC
         #self.r_SiC = self.r_iPyC + self.dr_SiC
         #self.r_oPyC = self.r_SiC + self.dr_oPyC
         #self.r_Matrix = self.r_oPyC + self.dr_Matrix

         #self.dv_Fuel = 4./3.*math.pi*math.pow(self.r_Fuel,3.)
         #self.dv_Buffer = 4./3.*math.pi*(math.pow(self.r_Buffer,3.)
         #- math.pow(self.r_Fuel,3.))
         #self.dv_iPyC   = 4./3.*math.pi*(math.pow(self.r_iPyC,3.)
         #- math.pow(self.r_Buffer,3.))
         #self.dv_SiC    = 4./3.*math.pi*(math.pow(self.r_SiC,3.)
         #- math.pow(self.r_iPyC,3.))
         #self.dv_oPyC   = 4./3.*math.pi*(math.pow(self.r_oPyC,3.)
         #- math.pow(self.r_SiC,3.))
         #self.dv_Matrix = 4./3.*math.pi*(math.pow(self.r_Matrix,3.)
         #- math.pow(self.r_oPyC,3.))
         #self.V         = self.dv_Fuel + self.dv_Buffer
         #+ self.dv_iPyC + self.dv_SiC + self.dv_oPyC + self.dv_Matrix
         #self.hpitch    = math.pow(self.V,(1./3.))/2.


class TrisoLattice(Comp):

    def __init__(self, triso_particle, pf=0.4):
        '''pf: packing fraction
        '''
        self.triso_particle = triso_particle
        self.temp = triso_particle.temp
        self.name = 'trisoLat'+triso_particle.name
        self.pitch = (4/3.0*math.pi*max(triso_particle.r_config.values())**3/pf)**(1/3.0)
        self.mat_list = self.triso_particle.mat_list
        Comp.__init__(self, self.temp, self.name, self.mat_list,
                      TrisoLatticeGen())
