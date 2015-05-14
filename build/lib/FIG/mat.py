#!/usr/bin/python
from mat_gen import MatGen
from comparable_object import CmpObj
import math
from sets import Set
# Units used in this file
# density in g/cm3 (in serpent g/cm3 if negative, in 10^24/cm3 if positive)
# composition fraction in atomic fraction (in serpent atomic if positive, mass
# if negative)
# temperatures in K

class Mat(CmpObj):

    def __init__(
            self,
            name,
            density,
            mat_comp,
            temp,
            flag=''):
        self.density = density   # density is mass density in g/cm3
        self.mat_comp = mat_comp  # string containing mat_composition and fraction
        self.gen = MatGen()
        self.flag = flag
        self.temp = temp
        CmpObj.__init__(self, temp, name)

    def generate_output(self):
        return self.gen.parse(self, 's')

    def calc_lib_id(self, temp):
        if temp//300*3<10:
            lib_id = '0'+str(int(temp//300*3))+'c'
        else:
            lib_id = str(int(temp//300*3))+'c'
        return lib_id

class Isotope:

    def __init__(self, name, Z, A, T):
        self.name = name
        self.Z = Z
        self.A = A
        self.T = T


class Fuel(Mat):

    def __init__(self, temp, name, input_file):
        #''' the input_file only contains isotope name and fractions, this init funct will calculate lib_id according to the temperature and include it in the file'''

        lib_id = self.calc_lib_id(temp)
        text_comp = []
        with open(input_file, 'r') as f:
            for line in f:
                text_comp.append(line.split(' ')[0]+'.%s ' %lib_id +line.split(' ')[1])
        Mat.__init__(self, name, 10, ''.join(text_comp), temp)


class Flibe(Mat):

    def __init__(self, temp):
        density = (2279.92 - 0.488*(temp-273.15))/1000
        self.temp = temp
        # FLiBe chemical formular is Li2BeF4
        self.r3006 = 2*0.0001#2.42E-5 # 2 * 0.0001
        self.r3007 = 2*0.9999 #2 # 2*0.9999
        self.r4009 = 1.0
        self.r9019 = 4.0
        mat_comp = []
        lib_id = self.calc_lib_id(temp)
        mat_comp.append('3006.%s %.8f\n3007.%s %f\n' %
                        (lib_id, self.r3006, lib_id, self.r3007) +
                        '4009.%s %f\n 9019.%s %f\n' %
                        (lib_id, self.r4009, lib_id, self.r9019))
        mat_comp = ''.join(mat_comp)
        name = 'Flibe%d' % math.ceil(temp)
        Mat.__init__(self, name, density, mat_comp, temp)


class Buffer(Mat):

    def __init__(self, temp):
        mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        mat_comp.append('6000.%s 5.26449E-02\n' % lib_id)
        mat_comp = ''.join(mat_comp)
        Mat.__init__(self, 'Buffer', 1.05, mat_comp, temp, 'moder')


class iPyC(Mat):

    def __init__(self, temp):
        mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        mat_comp.append('6000.%s 9.52621E-02\n' % lib_id)
        mat_comp = ''.join(mat_comp)
        Mat.__init__(self, 'iPyC', 1.90, mat_comp, temp, 'moder')


class oPyC(Mat):

    def __init__(self, temp):
        mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        mat_comp.append('6000.%s 9.52621E-02\n' % lib_id)
        mat_comp = ''.join(mat_comp)
        Mat.__init__(self, 'oPyC', 1.90, mat_comp, temp, 'moder')


class SiC(Mat):

    def __init__(self, temp):
        mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        mat_comp.append('6000.%s 4.7724E-02\n14000.%s 4.77240E-02\n' %
                        (lib_id, lib_id))
        mat_comp = ''.join(mat_comp)
        Mat.__init__(self, 'SiC', 3.18, mat_comp, temp)


class Matrix(Mat):

    def __init__(self, temp):
        mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        mat_comp.append('6000.%s 8.77414E-02\n' % lib_id +
                        '5010.%s 9.64977E-09\n' % lib_id +
                        '5011.%s 3.90864E-08\n' % lib_id)
        mat_comp = ''.join(mat_comp)
        Mat.__init__(self, 'Matrix', 1.75, mat_comp, temp, 'moder')


class Graphite(Mat):

    def __init__(self, temp):
        self.temp = temp
        self. density = 2.26
        self.mat_comp = []
        lib_id = self.calc_lib_id(temp)
        self.mat_comp.append('6000.%s 1.0\n' % lib_id)
        self.mat_comp = ''.join(self.mat_comp)
        self.name = 'Graphite%d' % (math.ceil(temp))
        Mat.__init__(
            self,
            self.name,
            self.density,
            self.mat_comp,
            temp,
            'moder')


class GraphiteCoolantMix(Mat):
    # this is a 'virtual' material defined as a mix of graphite and FliBe
    # to represent the inner part of the reflectors with coolant channel in it
    # volumetric fraction of coolant is 40%

    def __init__(self, temp):
        self.v_ratio = 0.4   # volumic ratio of coolant
        self.g = Graphite(temp)
        self.c = Flibe(temp)
        self.calculate_density()
        self.calculate_atomic_comp()
        self.mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        self.mat_comp.append(
            '6000.%s %f\n' %
            (lib_id, self.r6000) +
            '3006.%s %f\n3007.%s %f\n' %
            (lib_id, self.r3006, lib_id, self.r3007) +
            '4009.%s %f\n 9019.%s %f\n' %
            (lib_id, self.r4009, lib_id, self.r9019))
        self.mat_comp = ''.join(self.mat_comp)
        self.name = 'GraphiteCoolantMix%d' % (math.ceil(temp))
        Mat.__init__(
            self,
            self.name,
            self.density,
            self.mat_comp,
            temp,
            'moder')

    def calculate_atomic_comp(self):
        self.m_ratio = (self.v_ratio*self.c.density) /\
            (self.v_ratio * self.c.density + (1-self.v_ratio) * self.g.density)
        self.a_ratio = (self.m_ratio/2.349321E-23) /\
            (self.m_ratio/2.349321E-23 + (1-self.m_ratio)/(12/6.022/10E23))
        self.r3006 = self.c.r3006 * self.a_ratio
        self.r3007 = self.c.r3007 * self.a_ratio
        self.r4009 = self.c.r4009 * self.a_ratio
        self.r9019 = self.c.r9019 * self.a_ratio
        self.r6000 = (1-self.a_ratio)
        # print self.r3006 + self.r3007 + self.r4009 + self.r9019 + self.r6000

    def calculate_density(self):
        # calculate the equavalent density for the mixed material of graphite and coolant
        self.density = self.c.density * self.v_ratio + self.g.density *\
            (1 - self.v_ratio)


class Shell(Mat):
    # graphite shell in the pebbles

    def __init__(self, temp):
        self.density = 1.75
        self.mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        self.mat_comp.append('6000.%s 1.0\n' % lib_id)
        self.mat_comp = ''.join(self.mat_comp)
        Mat.__init__(self, 'Shell', self.density, self.mat_comp, temp, 'moder')


class CentralGraphite(Mat):
    # graphite core in the pebbles

    def __init__(self, temp):
        self.density = 1.74
        self.mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        self.mat_comp.append('6000.%s 1.0\n' % lib_id)
        self.mat_comp = ''.join(self.mat_comp)
        Mat.__init__(
            self,
            'CentralGraphite',
            self.density,
            self.mat_comp,
            temp,
            'moder')


class B4C(Mat):
    # natural boron carbide in control rods

    def __init__(self, temp):
        self.density = 2.52   #g/cm3
        self.mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        self.mat_comp.append('6000.%s 1.0\n5010.%s 0.8\n5011.%s 3.2' %\
                             (lib_id, lib_id, lib_id))
        self.mat_comp = ''.join(self.mat_comp)
        Mat.__init__(
            self,
            'B4C',
            self.density,
            self.mat_comp,
            temp)

class Outside(Mat):
    # outside the defined domain

    def __init__(self, temp):
        self.mat_comp = ''
        self.temp = temp
        Mat.__init__(self, 'Outside', self.density, self.mat_comp, temp)
