#!/usr/bin/python
'''
This is a core class, contains a FHR core
control rods
multple radial zones in the fuel region
no shiled
# all dimensions in cm
# all temperatures in K
'''

from core_gen import CoreGen
from comp import *
import math
from centerref import CenterRef, CRCC, CRCC_Cool, CRCC_liner, CRCC_axial_segment, CRCC_gr, Control_rod
# from control_rod import Control_rod
from outerref import OuterRef, OuterRef_CoolantChannel
from vessel import Vessel
from downcomer import Downcomer
from corebarrel import Corebarrel
from blanket import Blanket
# from shield import Shield
from fuel import Fuel

class Core(Comp):

    def __init__(
            self,
            fuel_prop_w,
            fuel_prop_a1,
            fuel_prop_a2,
            fuel_prop_a3,
            fuel_prop_a4,
            temp_CR,
            temp_rod_CRCC,
            temp_cool_CRCC,
            temp_OR,
            temp_g_ORCC,
            temp_cool_ORCC,
            temp_cool_F,
            temp_blanket,
            temp_cool_B,
            temp_corebarrel,
            temp_downcomer,
            temp_vessel,
            dir_name='res/serp_input/',
            hasShield=False,
            temp_shield=None,
            hasRods=[False, False, False, False]):
      '''
      fuel_prop: (fuel_mat_temps, coating_temps, central graphtie temp, shell temp, burnup_list)
      hasRods: if the rods are inserted in the four axial segments
      '''
      self.comp_dict = {}
      self.add_CR(temp_CR, temp_rod_CRCC, temp_cool_CRCC, hasRods)
      self.add_OR(temp_OR, temp_g_ORCC, temp_cool_ORCC, hasShield)
      self.add_Fuel(
                 fuel_prop_w,
                 fuel_prop_a1,
                 fuel_prop_a2,
                 fuel_prop_a3,
                 fuel_prop_a4,
                 temp_cool_F,
                 dir_name)
      self.add_blanket(temp_blanket,
                       temp_cool_B,
                       dir_name)
      self.add_outer_layers(temp_corebarrel,
                            temp_downcomer,
                            temp_vessel,
                            hasShield,
                            temp_shield)

      self.whole_core = CylComp(900, # a placehold for temperature
                                # of the whole core component because
                                # every component needs a temperature,
                                # not used in the serpent input files
                                'whole_core',
                                self.FuelA1.act.mat_list,
                                41.6,
                                572.85,
                                175,
                                fill=self.FuelA1.act)
      # contains not only self.Fuel but other three component, but they are
      # in the same universe, only need it to get the univ id
      name = 'FullCore'
      mat_list = self.collect_mat()
      Comp.__init__(self, 900, # a placehold for temperature
                          # of the whole core component because
                          # every component needs a temperature,
                          # not used in the serpent input files
                    name, mat_list, CoreGen(dir_name))

    def add_CR(self, temp_CR, temp_rod_CRCC, temp_cool_CRCC, hasRods):
      self.CR = CenterRef(temp_CR)
      self.CRCC = CRCC(temp_rod_CRCC, temp_cool_CRCC, temp_CR, hasRods)
      self.define_CR(self.CR.temp, self.CR.name, liner=True)
      self.comp_dict['CR'] = self.CR
      self.comp_dict['CRCC'] = self.CRCC

    def add_OR(self, temp_OR, temp_g_ORCC, temp_cool_ORCC, hasShield):
      self.OR = OuterRef(temp_OR)
      self.ORCC = OuterRef_CoolantChannel(temp_g_ORCC, temp_cool_ORCC)
      if hasShield:
        or_OR = 162
      else:
        or_OR = 165
      self.define_OR(self.OR.temp, self.OR.name, or_OR)
      self.define_ORCC(self.ORCC.temp, self.ORCC.name)
      self.comp_dict['OR'] = self.OR
      self.comp_dict['ORCC'] = self.ORCC

    def add_Fuel(self,
                 fuel_prop_w,
                 fuel_prop_a1,
                 fuel_prop_a2,
                 fuel_prop_a3,
                 fuel_prop_a4,
                 temp_cool_F,
                 dir_name):
      pf = 0.6 # 0.7405 maximum attainable packing fraction in a FCC lattice
      self.FuelW = Fuel(fuel_prop_w, temp_cool_F, dir_name, name='wall',
                        packing_fraction=pf)
      self.FuelA1 = Fuel(fuel_prop_a1, temp_cool_F, dir_name, name='act1',
                         packing_fraction=pf)
      self.FuelA2 = Fuel(fuel_prop_a2, temp_cool_F, dir_name, name='act2',
                         packing_fraction=pf)
      self.FuelA3 = Fuel(fuel_prop_a3, temp_cool_F, dir_name, name='act3',
                         packing_fraction=pf)
      self.FuelA4 = Fuel(fuel_prop_a4, temp_cool_F, dir_name, name='act4',
                         packing_fraction=pf)
      self.define_FuelA1(self.FuelA1.temp, self.FuelA1.name)
      self.define_FuelA2(self.FuelA2.temp, self.FuelA2.name)
      self.define_FuelA3(self.FuelA3.temp, self.FuelA3.name)
      self.define_FuelA4(self.FuelA4.temp, self.FuelA4.name)
      self.define_FuelW(self.FuelW.temp, self.FuelW.name)
      self.comp_dict.update({
                            'FuelW': self.FuelW,
                            'FuelA1': self.FuelA1,
                            'FuelA2': self.FuelA2,
                            'FuelA3': self.FuelA3,
                            'FuelA4': self.FuelA4
                            })

    def add_blanket(self,
                    temp_blanket,
                    temp_cool_B,
                    dir_name):
      self.Blanket = Blanket(temp_blanket, temp_cool_B, dir_name)
      self.define_Blanket(self.Blanket.temp, self.Blanket.name)
      self.comp_dict['Blanket'] = self.Blanket

    def add_outer_layers(self,
                         temp_corebarrel,
                         temp_downcomer,
                         temp_vessel,
                         hasShield,
                         temp_shield=None):
      self.Corebarrel = Corebarrel(temp_corebarrel)
      self.Downcomer = Downcomer(temp_downcomer)
      self.Vessel = Vessel(temp_vessel)
      if hasShield:
        # outer radius taken from Tommy's input Mark1.txt
        or_OR = 162
        or_shield = 164.7
        or_barrel = 168
        or_downcomer = 170
        or_vessel = 175

        # shield
        self.Shield = Shield(temp_Vessel) # assume it has the same temperature as vessel, need to be separated in the future
        self.define_Shield(self.Shield.temp, self.Shield.name, or_OR, or_shield)
        self.define_Corebarrel(self.Corebarrel.temp, self.Corebarrel.name, or_shield, or_barrel)
        self.comp_dict['Shield'] = self.Shield
      else:
        or_OR = 165
        or_barrel = 167.2
        or_downcomer = 170
        or_vessel = 175
        self.define_Corebarrel(self.Corebarrel.temp, self.Corebarrel.name, or_OR, or_barrel)

      self.define_Downcomer(self.Downcomer.temp, self.Downcomer.name, or_barrel, or_downcomer)
      self.define_Vessel(self.Vessel.temp, self.Vessel.name, or_downcomer, or_vessel)
      self.comp_dict.update({
                            'Downcomer': self.Downcomer,
                            'Corebarrel': self.Corebarrel,
                            'Vessel': self.Vessel
                            })

    def define_CR(self, temp, name, liner):
        '''
        liner
        '''
        self.CR.comp_dict = {}
        # ---------------------------------------------------------
        # center reflector
        # entrance zone
        self.CR.zb_ent = 41.6  # in the design, CR starts at 15.7cm
        self.CR.zt_ent = 127.5
        self.CR.r_ent = 35+10
        self.CR.ent = CylComp(temp, name,
                              self.CR.mat_list, self.CR.zb_ent,
                              self.CR.zt_ent, self.CR.r_ent,
                              fill=self.CR.fill)
        self.CR.comp_dict['ent'] = EmbeddedComp(self.CR.ent,
                                                self.CRCC.comp_dict)

        # diverging
        self.CR.zb_div = self.CR.zt_ent
        self.CR.zt_div = 144.82
        self.CR.r_div = self.CR.r_ent
        self.CR.a_div = 60.0/180*math.pi
        self.CR.h_cone_div = self.CR.r_div * math.tan(self.CR.a_div)
        self.CR.div = TruncConeComp(
            temp, name,
            self.CR.mat_list,
            self.CR.zb_div,
            self.CR.zt_div,
            self.CR.zb_div,
            self.CR.h_cone_div,
            self.CR.r_div,
            fill=self.CR.fill)
        self.CR.comp_dict['div'] = EmbeddedComp(self.CR.div,
                                                self.CRCC.comp_dict)
        # active zone
        self.CR.zb_act = self.CR.zt_div
        self.CR.zt_act = 430.50
        self.CR.r_act = 35
        self.CR.act = CylComp(temp, name, 
                              self.CR.mat_list, self.CR.zb_act,
                              self.CR.zt_act, self.CR.r_act,
                              fill=self.CR.fill)
        self.CR.comp_dict['act'] = EmbeddedComp(self.CR.act,
                                                self.CRCC.comp_dict)

        # Converging
        self.CR.zb_conv = self.CR.zt_act
        self.CR.zt_conv = 492.85
        self.CR.r_conv = 61+10
        self.CR.a_conv = 60.0/180*math.pi
        self.CR.h_cone_conv = -self.CR.r_conv * math.tan(self.CR.a_conv)
        # negative h means direction to -z
        self.CR.conv = TruncConeComp(temp, name,
                                     self.CR.mat_list,
                                     self.CR.zb_conv,
                                     self.CR.zt_conv,
                                     self.CR.zt_conv,
                                     self.CR.h_cone_conv,
                                     self.CR.r_conv,
                                     fill=self.CR.fill)
        self.CR.comp_dict['conv'] = EmbeddedComp(self.CR.conv,
                                                 self.CRCC.comp_dict)

        # defueling
        self.CR.r_defuel = self.CR.r_conv
        self.CR.zb_defuel = self.CR.zt_conv
        self.CR.zt_defuel = self.CR.zb_defuel + 80
        self.CR.defuel = CylComp(temp, name,
                                 self.CR.mat_list,
                                 self.CR.zb_defuel,
                                 self.CR.zt_defuel,
                                 self.CR.r_defuel,
                                 fill=self.CR.fill)
        self.CR.comp_dict['defuel'] = EmbeddedComp(self.CR.defuel,
                                                   self.CRCC.comp_dict)

        # substract CRCC's from CR
        #self.comp_dict['CR'] = CenterRefWithoutCC(self.CR, self.CRCC)

#        self.CRCC.zb_act = 41.6
#        self.CRCC.zt_act = self.CR.zt_conv+80
#        self.CRCC.ri_act = self.CR.r_act
#        self.CRCC.ro_act = self.CR.r_act + 10
#
#        self.CRCC.act = AnnuCylComp(temp, name,
#                                    self.CRCC.mat_list,
#                                    self.CRCC.ri_act,
#                                    self.CRCC.ro_act,
#                                    self.CRCC.zb_act,
#                                    self.CRCC.zt_act)
#
#        self.CRCC.comp_dict['act'] = self.CRCC.act
# ---------------------------------------------------------
# center reflector
# entrance zone
# self.CRCC.zb_ent = 41.6  # in the design, CR starts at 15.7cm
#        self.CRCC.zt_ent = 127.5
#        self.CRCC.ri_ent = self.CR.r_ent
#        self.CRCC.ro_ent = 45
#
#        self.CRCC.ent = AnnuCylComp(temp, name,
#                                    self.CRCC.mat_list,
#                                    self.CRCC.ri_ent,
#                                    self.CRCC.ro_ent,
#                                    self.CRCC.zb_ent,
#                                    self.CRCC.zt_ent)
#
#        self.CRCC.comp_dict['ent'] = self.CRCC.ent
#
# diverging
#        self.CRCC.zb_div = self.CRCC.zt_ent
#        self.CRCC.zt_div = self.CR.zt_div
#        self.CRCC.ri_cone_div = self.CRCC.ri_ent
#        self.CRCC.ro_cone_div = self.CRCC.ro_ent
#        self.CRCC.ai_div = 60.0/180*math.pi
#        self.CRCC.ao_div = 60.0/180*math.pi
#        self.CRCC.hi_cone_div = self.CRCC.ri_cone_div * \
#            math.tan(self.CRCC.ai_div)
#        self.CRCC.ho_cone_div = self.CRCC.ro_cone_div * \
#            math.tan(self.CRCC.ao_div)
#
#        self.CRCC.div = AnnuConeConeComp(temp, name,
#                                         self.CRCC.mat_list,
#                                         self.CRCC.ri_cone_div,
#                                         self.CRCC.hi_cone_div,
#                                         self.CRCC.zb_div,
#                                         self.CRCC.ro_cone_div,
#                                         self.CRCC.ho_cone_div,
#                                         self.CRCC.zb_div,
#                                         self.CRCC.zb_div,
#                                         self.CRCC.zt_div)
#
#        self.CRCC.comp_dict['div'] = self.CRCC.div
#
# active zone
#        self.CRCC.zb_act = self.CRCC.zt_div
#        self.CRCC.zt_act = self.CR.zt_act
#        self.CRCC.ri_act = self.CR.r_act
#        self.CRCC.ro_act = self.CR.r_act + 10
#
#        self.CRCC.act = AnnuCylComp(temp, name,
#                                    self.CRCC.mat_list,
#                                    self.CRCC.ri_act,
#                                    self.CRCC.ro_act,
#                                    self.CRCC.zb_act,
#                                    self.CRCC.zt_act)
#
#        self.CRCC.comp_dict['act'] = self.CRCC.act
#
# Converging
#        self.CRCC.zb_conv = self.CRCC.zt_act
#        self.CRCC.zt_conv = self.CR.zt_conv
#        self.CRCC.ri_conv = self.CR.r_conv
#        self.CRCC.ro_conv = self.CR.r_conv + 10
#        self.CRCC.ai_conv = 60.0/180*math.pi
#        self.CRCC.ao_conv = 60.0/180*math.pi
#        self.CRCC.hi_cone_conv = -self.CRCC.ri_conv * \
#            math.tan(self.CRCC.ai_conv)
#        self.CRCC.ho_cone_conv = -self.CRCC.ro_conv * \
#            math.tan(self.CRCC.ao_conv)
# negative h means direction to -z
#
#        self.CRCC.conv = AnnuConeConeComp(temp, name,
#                                          self.CRCC.mat_list,
#                                          self.CRCC.ri_conv,
#                                          self.CRCC.hi_cone_conv,
#                                          self.CRCC.zt_conv,
#                                          self.CRCC.ro_conv,
#                                          self.CRCC.ho_cone_conv,
#                                          self.CRCC.zt_conv,
#                                          self.CRCC.zb_conv,
#                                          self.CRCC.zt_conv)
#
#        self.CRCC.comp_dict['conv'] = self.CRCC.conv
#
# defueling
#        self.CRCC.ri_defuel = self.CRCC.ri_conv
#        self.CRCC.ro_defuel = self.CRCC.ro_conv
#        self.CRCC.zb_defuel = self.CRCC.zt_conv
#        self.CRCC.zt_defuel = self.CRCC.zb_defuel + 80
#        self.CRCC.defuel = AnnuCylComp(temp, name,
#                                       self.CRCC.mat_list,
#                                       self.CRCC.ri_defuel,
#                                       self.CRCC.ro_defuel,
#                                       self.CRCC.zb_defuel,
#                                       self.CRCC.zt_defuel)
#        self.CRCC.comp_dict['defuel'] = self.CRCC.defuel
#
    def define_OR(self, temp, name, or_OR=165):
        # --------------------------------------------------------
        # Outer reflector
        self.OR.r_outer = or_OR   # outer radius for the whole o_ref
        self.OR.comp_dict = {}

        # entrance zone
        self.OR.zb_ent = 41.6
        self.OR.zt_ent = 112.5
        self.OR.r_ent = 85.74
        self.OR.ent = AnnuCylComp(temp, name,
                                  self.OR.mat_list,
                                  self.OR.r_ent,
                                  self.OR.r_outer,
                                  self.OR.zb_ent,
                                  self.OR.zt_ent,
                                  fill=self.OR.fill)
        self.OR.comp_dict['ent'] = self.OR.ent

        # diverging  zone
        self.OR.a_div = math.pi*60.0/180
        self.OR.zb_div = 112.5
        self.OR.zt_div = 180.5
        self.OR.r_cone_div = 125   # self.OR.r_ent + \
            # (self.OR.zt_div - self.OR.zb_div)/math.tan(self.OR.a_div)
        self.OR.h_cone_div = -self.OR.r_cone_div*math.tan(self.OR.a_div)
        #  negative sign means direction -z
        self.OR.div = AnnuCylConeComp(
                temp, name,
                self.OR.mat_list,
                self.OR.r_cone_div,
                self.OR.h_cone_div,
                self.OR.zt_div,
                self.OR.r_outer,
                self.OR.zb_div,
                self.OR.zt_div,
                fill=self.OR.fill)

        self.OR.comp_dict['div'] = self.OR.div

        # active zone
        self.OR.r_act = 125 + 10
        self.OR.zb_act = self.OR.zt_div
        self.OR.zt_act = self.CR.zt_defuel
        self.OR.act = AnnuCylComp(temp, name,
                                  self.OR.mat_list,
                                  self.OR.r_act,
                                  self.OR.r_outer,
                                  self.OR.zb_act,
                                  self.OR.zt_act,
                                  fill=self.OR.fill)

        self.OR.comp_dict['act'] = self.OR.act


    def define_ORCC(self, temp, name):
        # --------------------------------------------------------
        # Outer reflector with coolant channel
        self.ORCC.comp_dict = {}

        # entrance zone
        #self.ORCC.zb_ent = self.OR.zb_ent
        #self.ORCC.zt_ent = self.OR.zt_ent
        #self.ORCC.ri_ent = self.OR.r_ent - 10
        #self.ORCC.ro_ent = self.OR.r_ent
        #self.ORCC.ent = AnnuCylComp(temp, name,
        #                            self.ORCC.mat_list,
        #                            self.ORCC.ri_ent,
        #                            self.ORCC.ro_ent,
        #                            self.ORCC.zb_ent,
        #                            self.ORCC.zt_ent)
        #self.ORCC.comp_dict['ent'] = self.ORCC.ent

        # diverging  zone
        #self.ORCC.ai_div = math.pi*60.0/180
        #self.ORCC.ao_div = math.pi*60.0/180
        #self.ORCC.zb_div = 112.5
        #self.ORCC.zt_div = 180.5
        #self.ORCC.ri_cone_div = 125
        #self.ORCC.hi_cone_div = -self.ORCC.ri_cone_div * \
        #    math.tan(self.ORCC.ai_div)
        #self.ORCC.ro_cone_div = self.OR.r_cone_div
        #self.ORCC.ho_cone_div = -self.ORCC.ro_cone_div * \
        #    math.tan(self.ORCC.ao_div)
        ##  negative sign means direction -z

        #self.ORCC.div = AnnuConeConeComp(temp, name,
        #                                 self.ORCC.mat_list,
        #                                 self.ORCC.ri_cone_div,
        #                                 self.ORCC.hi_cone_div,
        #                                 self.ORCC.zt_div,
        #                                 self.ORCC.ro_cone_div,
        #                                 self.ORCC.ho_cone_div,
        #                                 self.ORCC.zt_div,
        #                                 self.ORCC.zb_div,
        #                                 self.ORCC.zt_div)

        #self.ORCC.comp_dict['div'] = self.ORCC.div

        # active zone
        self.ORCC.ri_act = self.OR.r_act - 10
        self.ORCC.ro_act = self.OR.r_act
        self.ORCC.zb_act = 180.5
        self.ORCC.zt_act = 430.5
        self.ORCC.act = AnnuCylComp(temp, name,
                                    self.ORCC.mat_list,
                                    self.ORCC.ri_act,
                                    self.ORCC.ro_act,
                                    self.ORCC.zb_act,
                                    self.ORCC.zt_act,
                                    fill=self.ORCC.fill)

        self.ORCC.comp_dict['act'] = self.ORCC.act

        # convergeing zone
        self.ORCC.ri_cone_conv = self.ORCC.ri_act
        self.ORCC.ro_conv = self.ORCC.ro_act
        self.ORCC.ai_conv = 60.0 * math.pi/180
        #self.ORCC.ao_conv = 60.0 * math.pi/180
        self.ORCC.hi_cone_conv = self.ORCC.ri_cone_conv *\
            math.tan(self.ORCC.ai_conv)
        #self.ORCC.ho_cone_conv = self.ORCC.ro_cone_conv *\
        #    math.tan(self.ORCC.ao_conv)
        self.ORCC.zb_conv = self.ORCC.zt_act
        self.ORCC.zt_conv = self.CR.zb_defuel

        self.ORCC.conv = AnnuCylConeComp(temp, name,
                                        self.ORCC.mat_list,
                                        self.ORCC.ri_cone_conv,
                                        self.ORCC.hi_cone_conv,
                                        self.ORCC.zb_conv,
                                        self.ORCC.ro_conv,
                                        self.ORCC.zb_conv,
                                        self.ORCC.zt_conv,
                                        fill=self.ORCC.fill)

        self.ORCC.comp_dict['conv'] = self.ORCC.conv

        # defueling zone
        self.ORCC.zb_defuel = self.ORCC.zt_conv
        self.ORCC.zt_defuel = self.CR.zt_defuel
        self.ORCC.a_conv = math.pi*60/180.0
        self.ORCC.ri_defuel = self.ORCC.ri_cone_conv -\
            (self.ORCC.zt_conv-self.ORCC.zb_conv)/math.tan(self.ORCC.a_conv)
        self.ORCC.ro_defuel = self.ORCC.ro_act

        self.ORCC.defuel = AnnuCylComp(temp, name,
                                       self.ORCC.mat_list,
                                       self.ORCC.ri_defuel,
                                       self.ORCC.ro_defuel,
                                       self.ORCC.zb_defuel,
                                       self.ORCC.zt_defuel,
                                       fill=self.ORCC.fill)

        self.ORCC.comp_dict['defuel'] = self.ORCC.defuel

    def define_FuelA1(self, temp, name):
        # ---------------------------------------------------------
        # fuel zone
        # --------------------------------------------------------
        self.FuelA1.comp_dict = {}
        self.FuelA1.zb_act = self.OR.zt_div
        self.FuelA1.zt_act = self.CR.zt_act
        self.FuelA1.ro_act = 46.1
        self.FuelA1.act = AnnuCylComp(temp, name,
                                   self.FuelA1.mat_list,
                                   self.CR.r_act,
                                   self.FuelA1.ro_act,
                                   self.FuelA1.zb_act,
                                   self.FuelA1.zt_act,
                                   fill=self.FuelA1.fill)
        self.FuelA1.comp_dict['act'] = self.FuelA1.act

    def define_FuelA2(self, temp, name):
        # ---------------------------------------------------------
        # fuel zone
        # --------------------------------------------------------
        self.FuelA2.comp_dict = {}
        # active zone
        self.FuelA2.zb_act = self.FuelA1.zb_act
        self.FuelA2.zt_act = self.FuelA1.zt_act
        self.FuelA2.ri_act = self.FuelA1.ro_act
        self.FuelA2.ro_act = 58.3
        self.FuelA2.act = AnnuCylComp(temp, name,
                                    self.FuelA2.mat_list,
                                    self.FuelA2.ri_act,
                                    self.FuelA2.ro_act,
                                    self.FuelA2.zb_act,
                                    self.FuelA2.zt_act,
                                    fill=self.FuelA2.fill)
        self.FuelA2.comp_dict['act'] = self.FuelA2.act

    def define_FuelA3(self, temp, name):
        # ---------------------------------------------------------
        # fuel zone
        # --------------------------------------------------------
        self.FuelA3.comp_dict = {}
        # active zone
        self.FuelA3.zb_act = self.FuelA1.zb_act
        self.FuelA3.zt_act = self.FuelA1.zt_act
        self.FuelA3.ri_act = self.FuelA2.ro_act
        self.FuelA3.ro_act = 96
        self.FuelA3.act = AnnuCylComp(temp, name,
                                    self.FuelA3.mat_list,
                                    self.FuelA3.ri_act,
                                    self.FuelA3.ro_act,
                                    self.FuelA3.zb_act,
                                    self.FuelA3.zt_act,
                                    fill=self.FuelA3.fill)
        self.FuelA3.comp_dict['act'] = self.FuelA3.act

    def define_FuelA4(self, temp, name):
        # ---------------------------------------------------------
        # fuel zone
        # --------------------------------------------------------
        self.FuelA4.comp_dict = {}
        # active zone
        self.FuelA4.zb_act = self.FuelA1.zb_act
        self.FuelA4.zt_act = self.FuelA1.zt_act
        self.FuelA4.ri_act = self.FuelA3.ro_act
        self.FuelA4.ro_act = 105
        self.FuelA4.act = AnnuCylComp(temp, name,
                                    self.FuelA4.mat_list,
                                    self.FuelA4.ri_act,
                                    self.FuelA4.ro_act,
                                    self.FuelA4.zb_act,
                                    self.FuelA4.zt_act,
                                    fill=self.FuelA4.fill)
        self.FuelA4.comp_dict['act'] = self.FuelA4.act

    def define_FuelW(self, temp, name):
        # ---------------------------------------------------------
        # fuel zone
        # --------------------------------------------------------
        self.FuelW.comp_dict = {}
        # entrance zone
        self.FuelW.zb_ent = 41.6  # in design report fuel pb starts at 41.6cm
        self.FuelW.zt_ent = self.OR.zt_ent
        self.FuelW.ri_ent = self.CR.r_ent
        self.FuelW.ro_ent = 75.41
        self.FuelW.ent = AnnuCylComp(temp, name,
                                    self.FuelW.mat_list,
                                    self.FuelW.ri_ent,
                                    self.FuelW.ro_ent,
                                    self.FuelW.zb_ent,
                                    self.FuelW.zt_ent,
                                    fill=self.FuelW.fill)
        self.FuelW.comp_dict['ent'] = self.FuelW.ent
        # diverging  zone 1
        self.FuelW.ro_div = 105
        self.FuelW.a_div1 = math.atan((self.OR.zt_div-self.OR.zb_div) /
                                     (self.FuelW.ro_div-self.FuelW.ro_ent))
        self.FuelW.zb_div1 = self.OR.zt_ent
        self.FuelW.zt_div1 = self.CR.zb_div
        self.FuelW.r_cone_div1 = self.FuelW.ro_div
        self.FuelW.h_cone_div1 = -self.FuelW.r_cone_div1 * \
            math.tan(self.FuelW.a_div1)
        self.FuelW.z_cone_div1 = self.OR.zt_div
        #  negative sign means direction -z
        self.FuelW.ri_div1 = self.FuelW.ri_ent
        self.FuelW.div1 = AnnuConeCylComp(temp, name,
                                         self.FuelW.mat_list,
                                         self.FuelW.r_cone_div1,
                                         self.FuelW.h_cone_div1,
                                         self.FuelW.z_cone_div1,
                                         self.FuelW.ri_div1,
                                         self.FuelW.zb_div1,
                                         self.FuelW.zt_div1,
                                         fill=self.FuelW.fill)
        self.FuelW.comp_dict['div1'] = self.FuelW.div1

        # diverging  zone 2
        self.FuelW.ao_div2 = self.FuelW.a_div1
        self.FuelW.ai_div2 = math.pi * 60.0/180.0
        self.FuelW.zb_div2 = self.FuelW.zt_div1
        self.FuelW.zt_div2 = self.CR.zt_div
        self.FuelW.ri_div2 = self.FuelW.ri_ent
        self.FuelW.h_cone_i_div2 = self.FuelW.ri_div2 * \
            math.tan(self.FuelW.ai_div2)
        self.FuelW.ro_cone_div2 = self.FuelW.r_cone_div1
        self.FuelW.ho_cone_div2 = self.FuelW.h_cone_div1
        self.FuelW.zo_cone_div2 = self.OR.zt_div
        self.FuelW.div2 = AnnuConeConeComp(temp, name,
                                          self.FuelW.mat_list,
                                          self.FuelW.ri_div2,
                                          self.FuelW.h_cone_i_div2,
                                          self.FuelW.zb_div2,
                                          self.FuelW.ro_cone_div2,
                                          self.FuelW.ho_cone_div2,
                                          self.FuelW.zo_cone_div2,
                                          self.FuelW.zb_div2,
                                          self.FuelW.zt_div2,
                                          fill=self.FuelW.fill)
        self.FuelW.comp_dict['div2'] = self.FuelW.div2

        # diverging  zone 3
        self.FuelW.a_div3 = self.FuelW.a_div1
        self.FuelW.zb_div3 = self.FuelW.zt_div2
        self.FuelW.zt_div3 = self.OR.zt_div
        self.FuelW.r_i_div3 = self.CR.r_act
        self.FuelW.r_cone_div3 = self.FuelW.ro_cone_div2
        self.FuelW.h_cone_div3 = self.FuelW.ho_cone_div2
        self.FuelW.div3 = AnnuConeCylComp(temp, name,
                                         self.FuelW.mat_list,
                                         self.FuelW.r_cone_div3,
                                         self.FuelW.h_cone_div3,
                                         self.FuelW.zt_div3,
                                         self.FuelW.r_i_div3,
                                         self.FuelW.zb_div3,
                                         self.FuelW.zt_div3,
                                         fill=self.FuelW.fill)
        self.FuelW.comp_dict['div3'] = self.FuelW.div3

        # convergeing zone
        self.FuelW.zb_conv = self.CR.zt_act
        self.FuelW.zt_conv = self.CR.zt_conv
        self.FuelW.ri_conv = self.CR.r_conv
        self.FuelW.ai_conv = 60.0 * math.pi/180
        self.FuelW.hi_conv = -1.0*self.FuelW.ri_conv*math.tan(self.FuelW.ai_conv)
        self.FuelW.ro_conv = self.FuelW.ro_div
        self.FuelW.ao_conv = math.atan((self.FuelW.zt_conv - self.FuelW.zb_conv) /
                                      (self.FuelW.ro_div - 80))
        self.FuelW.ho_conv = self.FuelW.ro_conv*math.tan(self.FuelW.ao_conv)
        self.FuelW.conv = AnnuConeConeComp(temp, name,
                                          self.FuelW.mat_list,
                                          self.FuelW.ri_conv,
                                          self.FuelW.hi_conv,
                                          self.FuelW.zt_conv,
                                          self.FuelW.ro_conv,
                                          self.FuelW.ho_conv,
                                          self.FuelW.zb_conv,
                                          self.FuelW.zb_conv,
                                          self.FuelW.zt_conv,
                                          fill=self.FuelW.fill)
        self.FuelW.comp_dict['conv'] = self.FuelW.conv

        # defueling zone
        self.FuelW.zb_defuel = self.FuelW.zt_conv
        self.FuelW.zt_defuel = self.ORCC.zt_defuel
        self.FuelW.ri_defuel = self.CR.r_defuel
        self.FuelW.ro_defuel = self.FuelW.ro_div -\
            (self.FuelW.zt_conv - self.FuelW.zb_conv)/math.tan(self.FuelW.ao_conv)
        self.FuelW.defuel = AnnuCylComp(temp, name,
                                       self.FuelW.mat_list,
                                       self.FuelW.ri_defuel,
                                       self.FuelW.ro_defuel,
                                       self.FuelW.zb_defuel,
                                       self.FuelW.zt_defuel,
                                       fill=self.FuelW.fill)
        self.FuelW.comp_dict['defuel'] = self.FuelW.defuel


    def define_Blanket(self, temp, name):
        # -------------------------------------------------------------
        # Blanket
        # ------------------------------------------------------------
        self.Blanket.comp_dict = {}
        # entrance zone
        self.Blanket.zb_ent = 41.6  # in design report 41.6
        self.Blanket.zt_ent = self.OR.zt_ent
        self.Blanket.ri_ent = self.FuelW.ro_ent
        self.Blanket.ro_ent = self.OR.r_ent
        self.Blanket.ent = AnnuCylComp(temp, name,
                                       self.Blanket.mat_list,
                                       self.Blanket.ri_ent,
                                       self.Blanket.ro_ent,
                                       self.Blanket.zb_ent,
                                       self.Blanket.zt_ent,
                                       fill=self.Blanket.fill)
        self.Blanket.comp_dict['ent'] = self.Blanket.ent

        # diverging  zone
        self.Blanket.ai_div = self.FuelW.a_div1
        self.Blanket.zb_div = self.Blanket.zt_ent
        self.Blanket.zt_div = self.OR.zt_div
        self.Blanket.ri_div = self.FuelW.div3.ro
        self.Blanket.h_cone_i_div = -1.0 * self.Blanket.ri_div * \
            math.tan(self.Blanket.ai_div)
        self.Blanket.ao_div = math.pi*60.0/180
        self.Blanket.ro_div = self.OR.div.ri
        self.Blanket.h_cone_o_div = -1.0*self.Blanket.ro_div * \
            math.tan(self.Blanket.ao_div)
        self.Blanket.div = AnnuConeConeComp(temp, name,
                                            self.Blanket.mat_list,
                                            self.Blanket.ri_div,
                                            self.Blanket.h_cone_i_div,
                                            self.Blanket.zt_div,
                                            self.Blanket.ro_div,
                                            self.Blanket.h_cone_o_div,
                                            self.Blanket.zt_div,
                                            self.Blanket.zb_div,
                                            self.Blanket.zt_div,
                                            fill=self.Blanket.fill)
        self.Blanket.comp_dict['div'] = self.Blanket.div

        # active zone
        self.Blanket.ri_act = self.FuelA4.act.ro
        self.Blanket.ro_act = self.ORCC.ri_act
        self.Blanket.zb_act = self.Blanket.zt_div
        self.Blanket.zt_act = self.CR.zt_act
        self.Blanket.act = AnnuCylComp(temp, name,
                                       self.Blanket.mat_list,
                                       self.Blanket.ri_act,
                                       self.Blanket.ro_act,
                                       self.Blanket.zb_act,
                                       self.Blanket.zt_act,
                                       fill=self.Blanket.fill)
        self.Blanket.comp_dict['act'] = self.Blanket.act

        # convergeing zone
        self.Blanket.ri_conv = self.FuelW.ro_conv
        self.Blanket.ai_conv = self.FuelW.ao_conv
        self.Blanket.hi_conv = self.Blanket.ri_conv * \
            math.tan(self.Blanket.ai_conv)
        self.Blanket.ro_conv = self.Blanket.ro_act
        self.Blanket.ao_conv = 60.0 * math.pi/180
        self.Blanket.ho_conv = self.Blanket.ro_conv * \
            math.tan(self.Blanket.ao_conv)
        self.Blanket.zb_conv = self.Blanket.zt_act
        self.Blanket.zt_conv = self.CR.zt_conv
        self.Blanket.conv = AnnuConeConeComp(temp, name,
                                             self.Blanket.mat_list,
                                             self.Blanket.ri_conv,
                                             self.Blanket.hi_conv,
                                             self.Blanket.zb_conv,
                                             self.Blanket.ro_conv,
                                             self.Blanket.ho_conv,
                                             self.Blanket.zb_conv,
                                             self.Blanket.zb_conv,
                                             self.Blanket.zt_conv,
                                             fill=self.Blanket.fill)
        self.Blanket.comp_dict['conv'] = self.Blanket.conv

        # defueling zone
        self.Blanket.ri_defuel = self.FuelW.ro_defuel
        self.Blanket.ro_defuel = self.ORCC.ri_defuel
        self.Blanket.defuel = AnnuCylComp(temp, name,
                                          self.Blanket.mat_list,
                                          self.Blanket.ri_defuel,
                                          self.Blanket.ro_defuel,
                                          self.CR.zb_defuel,
                                          self.CR.zt_defuel,
                                          fill=self.Blanket.fill)
        self.Blanket.comp_dict['defuel'] = self.Blanket.defuel

    def define_Shield(self, temp, name, ri, ro):
        self.Shield.act = AnnuCylComp(temp, name,
                                      self.Shield.mat_list,
                                      ri,
                                      ro,
                                      self.CR.zb_ent,
                                      self.CR.zt_defuel,
                                      fill=self.Shield.fill
                                      )
        self.Shield.comp_dict = {}
        self.Shield.comp_dict['act'] = self.Shield.act

    def define_Corebarrel(self, temp, name, ri, ro):
        self.Corebarrel.act = AnnuCylComp(temp, name,
                                          self.Corebarrel.mat_list,
                                          ri, 
                                          ro,
                                          self.CR.zb_ent,
                                          self.CR.zt_defuel,
                                          fill=self.Corebarrel.fill)
        self.Corebarrel.comp_dict = {}
        self.Corebarrel.comp_dict['act'] = self.Corebarrel.act

    def define_Downcomer(self, temp, name, ri, ro):
        self.Downcomer.act = AnnuCylComp(temp, name,
                                         self.Downcomer.mat_list,
                                         ri,
                                         ro,
                                         self.CR.zb_ent,
                                         self.CR.zt_defuel,
                                         fill=self.Downcomer.fill)
        self.Downcomer.comp_dict = {}
        self.Downcomer.comp_dict['act'] = self.Downcomer.act

    def define_Vessel(self, temp, name, ri, ro):
        self.Vessel.act = AnnuCylComp(temp, name,
                                      self.Vessel.mat_list,
                                      ri,
                                      ro,
                                      self.CR.zb_ent,
                                      self.CR.zt_defuel,
                                      fill=self.Vessel.fill
                                      )
        self.Vessel.comp_dict = {}
        self.Vessel.comp_dict['act'] = self.Vessel.act

    def collect_mat(self):
        mat_list = []
        for comp in self.comp_dict:
            for mat in self.comp_dict[comp].mat_list:
                if mat not in mat_list:
                    mat_list.append(mat)
        return mat_list

