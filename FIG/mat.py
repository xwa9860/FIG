'''
 Units used in this file
 density in g/cm3 (in serpent g/cm3 if negative, in 10^24/cm3 if positive)
 composition fraction in atomic fraction (in serpent atomic if positive, mass
 if negative)
 temperatures in K
#
#
#TODO: add coolant and solid reflector mix class and make graphite_coolant, B2C
#mix and  Yh2 mix subclasses
#'''
##!/usr/bin/python
from mat_gen import MatGen
from comparable_object import CmpObj
import math

class Mat(CmpObj):

    def __init__(
            self,
            name,
            density,
            temp,
            mat_comp=[],
            isotopes=[],
            ratio_list=[],
            tmp_card=True,
            flag=''):
        '''
        ratio_list: list of atomic ratios of the isotopes, in the same order as
        in isotopes list
        '''
        self.name = name
        self.density = density   # density is mass density in g/cm3
        # string containing mat_composition and fraction
        self.mat_comp = mat_comp
        self.gen = MatGen()
        self.flag = flag
        self.temp = temp
        self.tmp_card = tmp_card
        self.isotopes = isotopes
        self.ratio_list = ratio_list
        if self.isotopes:
            self.mat_comp = []
            lib_id = self.calc_lib_id(temp)
            #TODO self.mat_comp.append(comments)
            print('defined isotopes%s' %self.name)
            self.calc_atomic_ratio(self.ratio_list)
            for isotope in self.isotopes:
                self.mat_comp.append(
                    '%s.%s %f\n' %
                    (isotope, lib_id, self.atomic_ratio[isotope]))
            self.mat_comp = ''.join(self.mat_comp)
        CmpObj.__init__(self, temp, name)

    def generate_output(self):
        return self.gen.parse(self, 's', self.tmp_card)

    def calc_lib_id(self, temp):
        if temp//300*3 < 10:
            lib_id = '0'+str(int(temp//300*3))+'c'
        else:
            lib_id = str(int(temp//300*3))+'c'
        return lib_id

    def calc_atomic_ratio(self, ratio_list):
        self.atomic_ratio = {}
        for i, isotope in enumerate(self.isotopes):
            self.atomic_ratio[isotope] = ratio_list[i]


class Isotope:

    def __init__(self, name, Z, A, T):
        self.name = name
        self.Z = Z
        self.A = A
        self.T = T


class Fuel(Mat):

    def __init__(self, temp, name, input_file, tmp_card=True):
        '''
        the input_file only contains isotope name and fractions, this init
        funct will calculate lib_id according to the temperature
        and include it in the file
        '''
        lib_id = self.calc_lib_id(temp)
        text_comp = []
        with open(input_file, 'r') as inpf:
            for line in inpf:
                text_comp.append(
                    line.split(' ')[0].split('.')[0] +
                    '.%s ' %
                    lib_id +
                    line.split(' ')[1])
        Mat.__init__(self, name, 10, temp, mat_comp=''.join(text_comp),
                     tmp_card=tmp_card)


class Flibe(Mat):

    def __init__(self, temp, tmp_card=True):
        density = (2279.92 - 0.488*(temp-273.15))/1000
        self.temp = temp
        # FLiBe chemical formular is Li2BeF4
        isotopes = ['3006', '3007', '4009', '9019']
        ratio_list = [2*0.0001, 2*0.9999, 1.0, 4.0]
        name = 'Flibe%d' % math.ceil(temp)
        Mat.__init__(self, name, density, temp, tmp_card=tmp_card,
                     isotopes=isotopes, ratio_list=ratio_list)


class Buffer(Mat):

    def __init__(self, temp, tmp_card=True):
        mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        mat_comp.append(
            '%Buffer layer in triso particle\n' +
            '6000.%s 5.26449E-02\n' %
            lib_id)
        mat_comp = ''.join(mat_comp)
        Mat.__init__(self, 'Buffer', 1.05, temp, mat_comp=mat_comp,
                     tmp_card=tmp_card, flag='moder')


class iPyC(Mat):

    def __init__(self, temp, tmp_card=True):
        mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        mat_comp.append(
            '%inner pyrocarbon layer in triso particle\n' +
            '6000.%s 9.52621E-02\n' %
            lib_id)
        mat_comp = ''.join(mat_comp)
        Mat.__init__(self, 'iPyC', 1.90, temp, mat_comp=mat_comp,
                     tmp_card=tmp_card, flag='moder')


class oPyC(Mat):

    def __init__(self, temp, tmp_card=True):
        mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        mat_comp.append(
            '%outer pyrocarbon layer in triso particle\n' +
            '6000.%s 9.52621E-02\n' %
            lib_id)
        mat_comp = ''.join(mat_comp)
        Mat.__init__(self, 'oPyC', 1.90, temp, mat_comp=mat_comp,
                    tmp_card=tmp_card, flag='moder')


class SiC(Mat):

    def __init__(self, temp, tmp_card=True):
        mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        mat_comp.append(
            '%silicon carbon layer in triso particle\n' +
            '6000.%s 4.7724E-02\n14028.%s 4.77240E-02\n' %
            (lib_id,
             lib_id))
        mat_comp = ''.join(mat_comp)
        Mat.__init__(self, 'SiC', 3.18, temp, mat_comp=mat_comp,
                     tmp_card=tmp_card)


class Matrix(Mat):

    def __init__(self, temp, tmp_card=True):
        mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        mat_comp.append('%matrix in triso particle\n' +
                        '6000.%s 8.77414E-02\n' % lib_id +
                        '5010.%s 9.64977E-09\n' % lib_id +
                        '5011.%s 3.90864E-08\n' % lib_id)
        mat_comp = ''.join(mat_comp)
        Mat.__init__(self, 'Matrix', 1.75, temp, mat_comp=mat_comp,
                     tmp_card=tmp_card, flag='moder')


class Graphite(Mat):

    def __init__(self, temp, tmp_card=True):
        self.temp = temp
        self.density = 2.26
        isotopes = ['6000']
        ratio_list = [1]
        #self.mat_comp = []
        #lib_id = self.calc_lib_id(temp)
        #self.mat_comp.append(
        #    '%graphite in reflectors\n' +
        #    '6000.%s 1.0\n' %
        #    lib_id)
        #self.mat_comp = ''.join(self.mat_comp)
        self.name = 'Graphite%d' % (math.ceil(temp))
        Mat.__init__(
            self,
            self.name,
            self.density,
            temp,
            tmp_card=tmp_card,
            isotopes=isotopes,
            ratio_list=ratio_list,
            flag='moder')

class GraphiteSSMix(Mat):
    '''Graphite and SS316 mix to represent inner reflector with a ss316
    control rod channel liner
    stainless steel composition and density from:
        http://www.espimetals.com/index.php/192-technical-data/stainless-steel-316-alloy-composition/202-stainless-steel-316-alloy-composition
    '''

    def __init__(self, temp, tmp_card=True):
        self.temp = temp
        # the density is an average between 2.26 for graphite
        # and 8.03 for SS316: 2.26*0.9+8.03*0.1
        self.density = 2.837
        # carbon, Ni, Cr, Mo, Fe, Si, Mn, P, S
        # carbon fraction includes both carbon in graphite and carbon in ss316
        isotopes = ['6000', '28000', '24000', '42000', '26000', '14000', '25000', '15000', '16000']
        # the SS316 atomic ratio to carbon in graphtie in 1:10
        ratio_list = [1+0.008, 1.2, 1.7, 0.25, 6.5345, 0.1, 0.2, 0.0045, 0.003]
        #self.mat_comp = []
        #lib_id = self.calc_lib_id(temp)
        #self.mat_comp.append(
        #    '%graphite in reflectors\n' +
        #    '6000.%s 1.0\n' %
        #    lib_id)
        #self.mat_comp = ''.join(self.mat_comp)
        self.name = 'GraphiteAndSS316%d' % (math.ceil(temp))
        Mat.__init__(
            self,
            self.name,
            self.density,
            temp,
            tmp_card=tmp_card,
            isotopes=isotopes,
            ratio_list=ratio_list,
            flag='moder')

class Shell(Mat):
    # graphite shell in the pebbles

    def __init__(self, temp, tmp_card=True):
        self.density = 1.75
        isotopes = ['6000']
        ratio_list = [1]
        #self.mat_comp = []
        #self.temp = temp
        #lib_id = self.calc_lib_id(temp)
        #self.mat_comp.append(
        #    '%Graphite shell(outermost layer of fuel pebble)\n' +
        #    '6000.%s 1.0\n' %
        #    lib_id)
        #self.mat_comp = ''.join(self.mat_comp)
        Mat.__init__(
            self,
            'Shell',
            self.density,
            temp,
            isotopes=isotopes,
            ratio_list=ratio_list,
            tmp_card=tmp_card,
            flag='moder')


class CentralGraphite(Mat):
    # graphite core in the pebbles

    def __init__(self, temp, tmp_card=True):
        self.density = 1.74
        isotopes = ['6000']
        ratio_list = [1]
        #self.mat_comp = []
        #self.temp = temp
        #lib_id = self.calc_lib_id(temp)
        #self.mat_comp.append(
        #    '%graphite core in fuel pebble(also called moderator\n' +
        #    '6000.%s 1.0\n' %
        #    lib_id)
        #self.mat_comp = ''.join(self.mat_comp)
        Mat.__init__(
            self,
            'CentralGraphite',
            self.density,
            temp,
            isotopes=isotopes,
            ratio_list=ratio_list,
            tmp_card=tmp_card,
            flag='moder')


class B4C(Mat):
    # natural boron carbide in control rods

    def __init__(self, temp, tmp_card=True):
        self.density = 2.52  # g/cm3
        self.mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        self.mat_comp.append('6000.%s 1.0\n5010.%s 0.8\n5011.%s 3.2' %
                             (lib_id, lib_id, lib_id))
        self.mat_comp = ''.join(self.mat_comp)
        Mat.__init__(
            self,
            'B4C',
            self.density,
            temp,
            mat_comp=self.mat_comp,
            tmp_card=tmp_card)


class Be2C(Mat):
    # berrylium carbide in reflectors

    def __init__(self, temp, tmp_card=True):
        self.density = 1.85  # g/cm3
        self.mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        self.mat_comp.append('6000.%s 1.0\n4009.%s 2.0\n' %
                             (lib_id, lib_id))
        self.mat_comp = ''.join(self.mat_comp)
        Mat.__init__(
            self,
            'Be2C',
            self.density,
            temp,
            mat_comp=self.mat_comp,
            tmp_card=tmp_card)

class Be(Mat):
    # berrylium metal in reflectors

    def __init__(self, temp, tmp_card=True):
        self.density = 1.85  # g/cm3
        self.mat_comp = []
        self.temp = temp
        lib_id = self.calc_lib_id(temp)
        self.mat_comp.append('4009.%s 1.0\n' %
                             (lib_id))
        self.mat_comp = ''.join(self.mat_comp)
        Mat.__init__(
            self,
            'Be',
            self.density,
            temp,
            mat_comp=self.mat_comp,
            tmp_card=tmp_card)

class YH2(Mat):
    # Yttrium hydride in the outer reflector

    def __init__(self, temp, tmp_card=True):
        self.density = 3.958  # g/cm3
        isotopes = ['39089', '1001']
        ratio_list = [1, 2]
        Mat.__init__(
            self,
            'YH2',
            self.density,
            temp,
            isotopes=isotopes,
            ratio_list=ratio_list,
            tmp_card=tmp_card)


class ZrH2(Mat):
    # Yttrium hydride in the outer reflector

    def __init__(self, temp, tmp_card=True):
        self.density = 5.56  # g/cm3
        isotopes = ['40090', '40091', '40092', '40094', '40096', '1001']
        ratio_list = [0.5145, 0.1122, 0.1715, 0.1738, 0.0280, 2]
        Mat.__init__(
            self,
            'ZrH2',
            self.density,
            temp,
            isotopes=isotopes,
            ratio_list=ratio_list,
            tmp_card=tmp_card)
class Outside(Mat):
    # outside the defined domain

    def __init__(self, temp):
        mat_comp = ''
        Mat.__init__(self, 'Outside', self.density, temp, mat_comp=mat_comp)


class mixMat(Mat):
    # this is a 'virtual' material defined as a mix of solid and FliBe coolant
    # to represent the inner part of the reflectors with coolant channel in it
    # volumetric fraction of coolant is 40%

    def __init__(self, temp, solid_mat, solid_atomic_mass,
                 coolant_v_ratio=0.4, tmp_card=True, flag=''):
        '''
        solid_mat and coolant_mat: material objects
        solid_atomic_mass: average atomic(sum of all elements if compound)
                        mass of the solid material
        '''
        self.v_ratio = coolant_v_ratio
        self.solid = solid_mat
        self.temp = temp
        self.coolant = Flibe(temp)
        isotopes = self.coolant.isotopes + self.solid.isotopes
        ratio_list = self.coolant.ratio_list + self.solid.ratio_list
        self.calculate_density()
        self.name = '%sCoolantMix%d' % (self.solid.name, math.ceil(temp))
        Mat.__init__(
            self,
            self.name,
            self.density,
            temp,
            tmp_card=tmp_card,
            isotopes=isotopes,
            ratio_list=ratio_list,
            flag=flag)
        self.calculate_atomic_comp(solid_atomic_mass)
        #self.mat_comp = []
        #lib_id = self.calc_lib_id(temp)
        #self.mat_comp.append(
        #    '%reflector and flibe mix(fictitious material' +
        #    ' for coolant channel regions in reflectors\n')
        #for isotope in self.isotopes:
        #    self.mat_comp.append(
        #        '%s.%s %f\n' %
        #        (isotope, lib_id, self.atomic_ratio[isotope]))
        #self.mat_comp = ''.join(self.mat_comp)

    def calculate_atomic_comp(self, solid_atomic_mass):
        self.coolant_mass_ratio = (self.v_ratio*self.coolant.density) /\
            (self.v_ratio * self.coolant.density +
             (1-self.v_ratio) * self.solid.density)
        self.coolant_atomic_ratio = (self.coolant_mass_ratio/2.349321E-23) /\
            (self.coolant_mass_ratio/2.349321E-23 +
             (1-self.coolant_mass_ratio)/(solid_atomic_mass/6.022/10E23))
        self.solid_atomic_ratio = (1-self.coolant_atomic_ratio)
        for isotope in self.solid.isotopes:
            self.atomic_ratio[isotope] = self.solid.atomic_ratio[isotope] \
                * self.solid_atomic_ratio
        for isotope in self.coolant.isotopes:
            self.atomic_ratio[isotope] = self.coolant.atomic_ratio[isotope] \
                * self.coolant_atomic_ratio
        #sum = self.r89000 + self.r3006 + self.r3007 + self.r4009 + self.r9019
        #assert sum == 1, 'atomic fraction does not sum to 1, but %f' %sum

    def calculate_density(self):
        # calculate the equavalent density for the mixed material of graphite
        # and coolant

        self.coolant = Flibe(self.temp)
        self.density = self.coolant.density * self.v_ratio + self.solid.density *\
            (1 - self.v_ratio)


class GraphiteCoolMix(mixMat):
    # this is a 'virtual' material defined as a mix of graphite and FliBe
    # to represent the inner part of the reflectors with coolant channel in it
    # volumetric fraction of coolant is 40%

    def __init__(self, temp, tmp_card=True):
        self.temp = temp
        flag='moder'
        mixMat.__init__(
            self,
            temp,
            Graphite(temp),
            12.0,
            tmp_card=tmp_card,
            flag=flag)

class GraphiteSSCoolMix(mixMat):
    # this is a 'virtual' material defined as a mix of graphite and FliBe and
    # a little SS316 as control rod channel liner
    # to represent the inner part of the reflectors with coolant channel in it
    # volumetric fraction of coolant is 40%

    def __init__(self, temp, tmp_card=True):
        # average graphtie and SS316 atomic mass(not very precise about the
        # atomic numbers of each isotope)
        solid_atomic_mass = (12*100.008+56*1.2+48*1.7+84*0.5+52*6.5345*2
                             +28*0.2+50*0.4+30*0.009+32*0.006)/110.0
        self.temp = temp
        flag='moder'
        mixMat.__init__(
            self,
            temp,
            GraphiteSSMix(temp),
            solid_atomic_mass,
            tmp_card=tmp_card,
            flag=flag)

class Be2CCoolMix(mixMat):
    # this is a 'virtual' material defined as a mix of Be2C and FliBe
    # to represent the inner part of the reflectors with coolant channel in it
    # volumetric fraction of coolant is 40%

    def __init__(self, temp, tmp_card=True):
        self.v_ratio = 0.4   # volumic ratio of coolant
        mixMat.__init__(
            self,
            temp,
            Be2C(temp),
            30,
            tmp_card)


class BeCoolMix(mixMat):
    # this is a 'virtual' material defined as a mix of Be and FliBe
    # to represent the inner part of the reflectors with coolant channel in it
    # volumetric fraction of coolant is 40%

    def __init__(self, temp, tmp_card=True):
        self.v_ratio = 0.4   # volumic ratio of coolant
        mixMat.__init__(
            self,
            temp,
            Be(temp),
            30,
            tmp_card)

class YH2CoolMix(mixMat):
    # this is a 'virtual' material defined as a mix of YH2 and FliBe
    # to represent the inner part of the reflectors with coolant channel in it
    # volumetric fraction of coolant is 40%

    def __init__(self, temp, tmp_card=True):
        self.v_ratio = 0.4   # volumic ratio of coolant
        mixMat.__init__(
            self,
            temp,
            YH2(temp),
            91.0,
            tmp_card=tmp_card)

class ZrH2CoolMix(mixMat):
    # this is a 'virtual' material defined as a mix of Be2C and FliBe
    # to represent the inner part of the reflectors with coolant channel in it
    # volumetric fraction of coolant is 40%

    def __init__(self, temp, tmp_card=True):
        self.v_ratio = 0.4   # volumic ratio of coolant
        mixMat.__init__(
            self,
            temp,
            ZrH2(temp),
            93.224,
            tmp_card)

