#!/usr/bin/python
from triso_gen import TrisoGen
from triso_gen import TrisoLatticeGen
from comp import Comp
from mat import Buffer, iPyC, SiC, oPyC, Matrix, CMatrix
import math


class Triso(Comp):

    def __init__(self,
                 coating_t_list, 
                 fuel_list, 
                 dr_config=None, 
                 dir_name='serp_input'):
        '''
        coating_t_list: non_fuel coating layers temperatures in a list
        fuel_list: fuel material in a list
        dr_config: thickness of the layers
        '''
        if dr_config == None:
            assert len(coating_t_list) == 5, 'wrong temperature number %d' %(len(coating_t_list))
        elif dr_config =='homogenized':
            assert len(coating_t_list) == 1, 'wrong temperature number %d' %len(coating_t_list)
        else:
            raise ValueError, 'triso dr_config not implemented'

        # materials
        self.mat_list = []
        if not dr_config:
            for fuel in fuel_list:
                self.mat_list.append(fuel)
            self.mat_list.extend([Buffer(coating_t_list[0]),
                                  iPyC(coating_t_list[1]),
                                  SiC(coating_t_list[2]),
                                  oPyC(coating_t_list[3]),
                                  Matrix(coating_t_list[4])])
        elif dr_config == 'homogenized':
            for fuel in fuel_list:
                self.mat_list.append(fuel)
            self.mat_list.append(CMatrix(coating_t_list[0]))

        dr_list = []
        self.dr_config = {}
        # fuel layers radius
        for i, fuel in enumerate(fuel_list):
            tot_nb = len(fuel_list)
            tot_r = 0.02
            dr_list.append(((tot_r**3.0)/float(tot_nb)*(i+1))**(1/3.0))
        if not dr_config:
            dr_list.extend([0.01, 0.0035, 0.0035, 0.0035])
        elif dr_config == 'homogenized':
            assert len(self.mat_list) == len(fuel_list) + 1, 'wrong length of mat_list'
        for i, dr in enumerate(dr_list):
            self.dr_config[self.mat_list[i].name] = dr

        assert len(coating_t_list) + len(fuel_list) == 1 + len(self.dr_config), '''
        coating_t_list and fuel_list for triso particle needs %d
        temperature values, got %d and %d''' % (len(self.dr_config),
                                                len(coating_t_list),
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
