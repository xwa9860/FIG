#!/usr/bin/python
from core_simple_gen import CoreSimpleGen
from mat import Graphite
from comp import (Comp, CylComp, TruncConeComp,
                  AnnuCylComp, AnnuConeCylComp,
                  AnnuCylConeComp, AnnuConeConeComp)
from pbed import FuelFCC, GFCC, PBedLat
import math
from sets import Set
# all dimensions in cm
# all temperatures in K


class CenterRef(Comp):

    def __init__(self, temp):
        name = 'CR'
        Comp.__init__(self, temp, name, Set([Graphite(temp)]))


class OuterRef(Comp):

    def __init__(self, temp):
        name = 'OR'
        Comp.__init__(self, temp, name, Set([Graphite(temp)]))


class Fuel(Comp):

    def __init__(self, fuel_temp, cool_temp):
        name = 'FuelZone'
        self.unit_cell = FuelFCC(cool_temp, fuel_temp, 'fpb_pos.inp')
        self.unit_cell_lattice = PBedLat(self.unit_cell, self.unit_cell.p)
        self.filling = Set([self.unit_cell_lattice])
        Comp.__init__(self, fuel_temp, name, self.filling)


class Blanket(Comp):

    def __init__(self, cool_temp, pb_temp):
        self.cool_temp = cool_temp
        self.pb_temp = pb_temp
        name = 'Blanket'
        self.unit_cell = GFCC(self.cool_temp, self.pb_temp, 'gpb_pos.inp')
        self.unit_cell_lattice = PBedLat(self.unit_cell, self.unit_cell.p)
        self.filling = Set([self.unit_cell_lattice])
        Comp.__init__(self, pb_temp, name,
                      self.filling)


class Core(Comp):

    def __init__(
            self,
            temp_CR,
            temp_OR,
            temp_Fuel,
            temp_cool_F,
            temp_Blanket,
            temp_cool):
        self.comp_dict = {
            'CR': CenterRef(temp_CR),
            'OR': OuterRef(temp_OR),
            'Fuel': Fuel(temp_Fuel, temp_cool_F),
            'Blanket': Blanket(temp_Blanket, temp_cool)
        }
        self.CR = self.comp_dict['CR']
        self.OR = self.comp_dict['OR']
        self.Fuel = self.comp_dict['Fuel']
        self.Blanket = self.comp_dict['Blanket']
        self.define_CR(self.CR.temp, self.CR.name)
        self.define_OR(self.OR.temp, self.OR.name)
        self.define_Fuel(self.Fuel.temp, self.Fuel.name)
        self.define_Blanket(self.Blanket.temp, self.Blanket.name)

        self.core = CylComp(temp_Fuel,
                            'core',
                            Set([self.Fuel.act]),
                            0,
                            572.85,
                            165)
        # contains not only self.Fuel but other three component, but they are in
        # the same universe, so only need one to get the univ id
        name = 'FullCore'
        self.collect_fillings()
        Comp.__init__(self, temp_Fuel, name, self.filling, CoreSimpleGen())

    def define_CR(self, temp, name):
        self.CR.comp_dict = {}
        # ---------------------------------------------------------
        # center reflector
        # entrance zone
        self.CR.zb_ent = 0  # in the design, CR starts at 15.7cm
        self.CR.zt_ent = 127.5
        self.CR.r_ent = 45
        self.CR.ent = CylComp(temp, name, self.CR.filling, self.CR.zb_ent,
                              self.CR.zt_ent, self.CR.r_ent)
        self.CR.comp_dict['ent'] = self.CR.ent
        # diverging
        self.CR.zb_div = self.CR.zt_ent
        self.CR.zt_div = 144.82
        self.CR.r_div = self.CR.r_ent
        self.CR.a_div = 60.0/180*math.pi
        self.CR.h_cone_div = self.CR.r_div * math.tan(self.CR.a_div)
        self.CR.div = TruncConeComp(
            temp, name,
            self.CR.filling,
            self.CR.zb_div,
            self.CR.zt_div,
            self.CR.zb_div,
            self.CR.h_cone_div,
            self.CR.r_div)
        self.CR.comp_dict['div'] = self.CR.div
        # active zone
        self.CR.zb_act = self.CR.zt_div
        self.CR.zt_act = 430.50
        self.CR.r_act = 35
        self.CR.act = CylComp(temp, name, self.CR.filling, self.CR.zb_act,
                              self.CR.zt_act, self.CR.r_act)
        self.CR.comp_dict['act'] = self.CR.act
        # Converging
        self.CR.zb_conv = self.CR.zt_act
        self.CR.zt_conv = 492.85
        self.CR.r_conv = 71
        self.CR.a_conv = 60.0/180*math.pi
        self.CR.h_cone_conv = -self.CR.r_conv * math.tan(self.CR.a_conv)
        # negative h means direction to -z
        self.CR.conv = TruncConeComp(temp, name,
                                     self.CR.filling,
                                     self.CR.zb_conv,
                                     self.CR.zt_conv,
                                     self.CR.zt_conv,
                                     self.CR.h_cone_conv,
                                     self.CR.r_conv)
        self.CR.comp_dict['conv'] = self.CR.conv
        # top
        self.CR.r_defuel = self.CR.r_conv
        self.CR.zb_defuel = self.CR.zt_conv
        self.CR.zt_defuel = self.CR.zb_defuel + 80
        self.CR.defuel = CylComp(temp, name,
                                 self.CR.filling,
                                 self.CR.zb_defuel,
                                 self.CR.zt_defuel,
                                 self.CR.r_defuel)
        self.CR.comp_dict['defuel'] = self.CR.defuel

    def define_OR(self, temp, name):
        # --------------------------------------------------------
        # Outer reflector
        self.OR.r_outer = 165   # outer radius for the whole o_ref
        self.OR.comp_dict = {}
        # entrance zone
        self.OR.zb_ent = 0
        self.OR.zt_ent = 112.5
        self.OR.r_ent = 85.74
        self.OR.ent = AnnuCylComp(temp, name,
                                  self.OR.filling,
                                  self.OR.r_ent,
                                  self.OR.r_outer,
                                  self.OR.zb_ent,
                                  self.OR.zt_ent)
        self.OR.comp_dict['ent'] = self.OR.ent
        # diverging  zone
        self.OR.a_div = math.pi*60.0/180
        self.OR.zb_div = 112.5
        self.OR.zt_div = 180.5
        self.OR.r_cone_div = 125  # self.OR.r_ent + \
            #(self.OR.zt_div - self.OR.zb_div)/math.tan(self.OR.a_div)
        self.OR.h_cone_div = -self.OR.r_cone_div*math.tan(self.OR.a_div)
        #  negative sign means direction -z
        self.OR.div = AnnuCylConeComp(
            name,
            temp,
            self.OR.filling,
            self.OR.r_cone_div,
            self.OR.h_cone_div,
            self.OR.zt_div,
            self.OR.r_outer,
            self.OR.zb_div,
            self.OR.zt_div)

        self.OR.comp_dict['div'] = self.OR.div
        # active zone
        self.OR.r_act = 125
        self.OR.zb_act = 180.5
        self.OR.zt_act = 430.5
        self.OR.act = AnnuCylComp(temp, name,
                                  self.OR.filling,
                                  self.OR.r_act,
                                  self.OR.r_outer,
                                  self.OR.zb_act,
                                  self.OR.zt_act)

        self.OR.comp_dict['act'] = self.OR.act
        # convergeing zone
        self.OR.r_cone_conv = self.OR.r_act
        self.OR.a_conv = 60.0 * math.pi/180
        self.OR.h_cone_conv = self.OR.r_cone_conv*math.tan(self.OR.a_conv)
        self.OR.z_cone_conv = self.OR.zt_act
        self.OR.zb_conv = self.OR.zt_act
        self.OR.zt_conv = 492.85
        self.OR.conv = AnnuCylConeComp(
            name,
            temp,
            self.OR.filling,
            self.OR.r_cone_conv,
            self.OR.h_cone_conv,
            self.OR.z_cone_conv,
            self.OR.r_outer,
            self.OR.zb_conv,
            self.OR.zt_conv)

        self.OR.comp_dict['conv'] = self.OR.conv
        # defueling zone
        self.OR.zb_defuel = self.OR.zt_conv
        self.OR.zt_defuel = self.CR.zt_defuel
        self.OR.ri_defuel = self.OR.r_cone_conv -\
            (self.OR.zt_conv-self.OR.zb_conv)/math.tan(self.OR.a_conv)
        self.OR.defuel = AnnuCylComp(temp, name,
                                     self.OR.filling,
                                     self.OR.ri_defuel,
                                     self.OR.r_outer,
                                     self.OR.zb_defuel,
                                     self.OR.zt_defuel)
        self.OR.comp_dict['defuel'] = self.OR.defuel

    def define_Fuel(self, temp, name):
        # ---------------------------------------------------------
        # fuel zone
        # --------------------------------------------------------
        self.Fuel.comp_dict = {}
        # entrance zone
        self.Fuel.zb_ent = 0.0  # in design report fuel pb starts at 41.6cm
        self.Fuel.zt_ent = self.OR.zt_ent
        self.Fuel.ri_ent = self.CR.r_ent
        self.Fuel.ro_ent = self.Fuel.ri_ent + 20
        self.Fuel.ent = AnnuCylComp(temp, name,
                                    self.Fuel.filling,
                                    self.Fuel.ri_ent,
                                    self.Fuel.ro_ent,
                                    self.Fuel.zb_ent,
                                    self.Fuel.zt_ent)
        self.Fuel.comp_dict['ent'] = self.Fuel.ent
        # diverging  zone 1
        self.Fuel.ro_act = 105
        self.Fuel.a_div1 = math.atan((self.OR.zt_div-self.OR.zb_div)/\
                                     (self.Fuel.ro_act-self.Fuel.ro_ent))
        self.Fuel.zb_div1 = self.OR.zt_ent
        self.Fuel.zt_div1 = self.CR.zb_div
        self.Fuel.r_cone_div1 = self.Fuel.ro_act
        self.Fuel.h_cone_div1 = -self.Fuel.r_cone_div1 * \
            math.tan(self.Fuel.a_div1)
        self.Fuel.z_cone_div1 = self.OR.zt_div
        #  negative sign means direction -z
        self.Fuel.ri_div1 = self.Fuel.ri_ent
        self.Fuel.div1 = AnnuConeCylComp(temp, name,
                                         self.Fuel.filling,
                                         self.Fuel.r_cone_div1,
                                         self.Fuel.h_cone_div1,
                                         self.Fuel.z_cone_div1,
                                         self.Fuel.ri_div1,
                                         self.Fuel.zb_div1,
                                         self.Fuel.zt_div1)
        self.Fuel.comp_dict['div1'] = self.Fuel.div1

        # diverging  zone 2
        self.Fuel.ao_div2 = self.Fuel.a_div1
        self.Fuel.ai_div2 = math.pi * 60.0/180.0
        self.Fuel.zb_div2 = self.Fuel.zt_div1
        self.Fuel.zt_div2 = self.CR.zt_div
        self.Fuel.ri_div2 = self.Fuel.ri_ent
        self.Fuel.h_cone_i_div2 = self.Fuel.ri_div2 * \
            math.tan(self.Fuel.ai_div2)
        self.Fuel.ro_cone_div2 = self.Fuel.r_cone_div1
        self.Fuel.ho_cone_div2 = self.Fuel.h_cone_div1
        self.Fuel.zo_cone_div2 = self.OR.zt_div
        self.Fuel.div2 = AnnuConeConeComp(temp, name,
                                          self.Fuel.filling,
                                          self.Fuel.ri_div2,
                                          self.Fuel.h_cone_i_div2,
                                          self.Fuel.zb_div2,
                                          self.Fuel.ro_cone_div2,
                                          self.Fuel.ho_cone_div2,
                                          self.Fuel.zo_cone_div2,
                                          self.Fuel.zb_div2,
                                          self.Fuel.zt_div2)
        self.Fuel.comp_dict['div2'] = self.Fuel.div2

        # diverging  zone 3
        self.Fuel.a_div3 = self.Fuel.a_div1
        self.Fuel.zb_div3 = self.Fuel.zt_div2
        self.Fuel.zt_div3 = self.OR.zt_div
        self.Fuel.r_i_div3 = self.CR.r_act
        self.Fuel.r_cone_div3 = self.Fuel.ro_cone_div2
        self.Fuel.h_cone_div3 = self.Fuel.ho_cone_div2
        self.Fuel.div3 = AnnuConeCylComp(temp, name,
                                         self.Fuel.filling,
                                         self.Fuel.r_cone_div3,
                                         self.Fuel.h_cone_div3,
                                         self.Fuel.zt_div3,
                                         self.Fuel.r_i_div3,
                                         self.Fuel.zb_div3,
                                         self.Fuel.zt_div3)
        self.Fuel.comp_dict['div3'] = self.Fuel.div3

        # active zone
        self.Fuel.zb_act = self.Fuel.zt_div3
        self.Fuel.zt_act = self.CR.zt_act
        self.Fuel.act = AnnuCylComp(temp, name,
                                    self.Fuel.filling,
                                    self.CR.r_act,
                                    self.Fuel.ro_act,
                                    self.Fuel.zb_act,
                                    self.Fuel.zt_act)
        self.Fuel.comp_dict['act'] = self.Fuel.act

        # convergeing zone
        self.Fuel.zb_conv = self.Fuel.zt_act
        self.Fuel.zt_conv = self.CR.zt_conv
        self.Fuel.ri_conv = self.CR.r_conv
        self.Fuel.ai_conv = 60.0 * math.pi/180
        self.Fuel.hi_conv = -1.0*self.Fuel.ri_conv*math.tan(self.Fuel.ai_conv)
        self.Fuel.ro_conv = self.Fuel.ro_act
        self.Fuel.ao_conv = math.atan((self.Fuel.zt_conv - self.Fuel.zb_conv)/\
                (self.Fuel.ro_act - 80))
        self.Fuel.ho_conv = self.Fuel.ro_conv*math.tan(self.Fuel.ao_conv)
        self.Fuel.conv = AnnuConeConeComp(temp, name,
                                          self.Fuel.filling,
                                          self.Fuel.ri_conv,
                                          self.Fuel.hi_conv,
                                          self.Fuel.zt_conv,
                                          self.Fuel.ro_conv,
                                          self.Fuel.ho_conv,
                                          self.Fuel.zb_conv,
                                          self.Fuel.zb_conv,
                                          self.Fuel.zt_conv)
        self.Fuel.comp_dict['conv'] = self.Fuel.conv

        # defueling zone
        self.Fuel.zb_defuel = self.Fuel.zt_conv
        self.Fuel.zt_defuel = self.OR.zt_defuel
        self.Fuel.ri_defuel = self.CR.r_defuel
        self.Fuel.ro_defuel = self.Fuel.ro_act -\
            (self.Fuel.zt_conv - self.Fuel.zb_conv)/math.tan(self.Fuel.ao_conv)
        self.Fuel.defuel = AnnuCylComp(temp, name,
                                       self.Fuel.filling,
                                       self.Fuel.ri_defuel,
                                       self.Fuel.ro_defuel,
                                       self.Fuel.zb_defuel,
                                       self.Fuel.zt_defuel)
        self.Fuel.comp_dict['defuel'] = self.Fuel.defuel

    def define_Blanket(self, temp, name):
        # -------------------------------------------------------------
        # Blanket
        # ------------------------------------------------------------
        self.Blanket.comp_dict = {}
        # entrance zone
        self.Blanket.zb_ent = 0  # in design report 41.6
        self.Blanket.zt_ent = self.OR.zt_ent
        self.Blanket.ri_ent = self.Fuel.ro_ent
        self.Blanket.ro_ent = self.OR.r_ent
        self.Blanket.ent = AnnuCylComp(temp, name,
                                       self.Blanket.filling,
                                       self.Blanket.ri_ent,
                                       self.Blanket.ro_ent,
                                       self.Blanket.zb_ent,
                                       self.Blanket.zt_ent)
        self.Blanket.comp_dict['ent'] = self.Blanket.ent

        # diverging  zone
        self.Blanket.ai_div = self.Fuel.a_div1
        self.Blanket.zb_div = self.Blanket.zt_ent
        self.Blanket.zt_div = self.OR.zt_div
        self.Blanket.ri_div = self.Fuel.div3.ro
        self.Blanket.h_cone_i_div = -1.0 * self.Blanket.ri_div * \
            math.tan(self.Blanket.ai_div)
        self.Blanket.ao_div = math.pi*60.0/180
        self.Blanket.ro_div = self.OR.div.ri
        self.Blanket.h_cone_o_div = -1.0*self.Blanket.ro_div * \
            math.tan(self.Blanket.ao_div)
        self.Blanket.div = AnnuConeConeComp(temp, name,
                                            self.Blanket.filling,
                                            self.Blanket.ri_div,
                                            self.Blanket.h_cone_i_div,
                                            self.Blanket.zt_div,
                                            self.Blanket.ro_div,
                                            self.Blanket.h_cone_o_div,
                                            self.Blanket.zt_div,
                                            self.Blanket.zb_div,
                                            self.Blanket.zt_div)
        self.Blanket.comp_dict['div'] = self.Blanket.div

        # active zone
        self.Blanket.ri_act = self.Fuel.act.ro
        self.Blanket.ro_act = self.OR.r_act
        self.Blanket.zb_act = self.Blanket.zt_div
        self.Blanket.zt_act = self.CR.zt_act
        self.Blanket.act = AnnuCylComp(temp, name,
                                       self.Blanket.filling,
                                       self.Blanket.ri_act,
                                       self.Blanket.ro_act,
                                       self.Blanket.zb_act,
                                       self.Blanket.zt_act)
        self.Blanket.comp_dict['act'] = self.Blanket.act

        # convergeing zone
        self.Blanket.ri_conv = self.Fuel.ro_conv
        self.Blanket.ai_conv = self.Fuel.ao_conv
        self.Blanket.hi_conv = self.Blanket.ri_conv * \
            math.tan(self.Blanket.ai_conv)
        self.Blanket.ro_conv = self.Blanket.ro_act
        self.Blanket.ao_conv = 60.0 * math.pi/180
        self.Blanket.ho_conv = self.Blanket.ro_conv * \
            math.tan(self.Blanket.ao_conv)
        self.Blanket.zb_conv = self.Blanket.zt_act
        self.Blanket.zt_conv = self.CR.zt_conv
        self.Blanket.conv = AnnuConeConeComp(temp, name,
                                             self.Blanket.filling,
                                             self.Blanket.ri_conv,
                                             self.Blanket.hi_conv,
                                             self.Blanket.zb_conv,
                                             self.Blanket.ro_conv,
                                             self.Blanket.ho_conv,
                                             self.Blanket.zb_conv,
                                             self.Blanket.zb_conv,
                                             self.Blanket.zt_conv)
        self.Blanket.comp_dict['conv'] = self.Blanket.conv

        # defueling zone
        self.Blanket.ri_defuel = self.Fuel.ro_defuel
        self.Blanket.ro_defuel = self.OR.ri_defuel
        self.Blanket.defuel = AnnuCylComp(temp, name,
                                          self.Blanket.filling,
                                          self.Blanket.ri_defuel,
                                          self.Blanket.ro_defuel,
                                          self.CR.zb_defuel,
                                          self.CR.zt_defuel)
        self.Blanket.comp_dict['defuel'] = self.Blanket.defuel

    def collect_fillings(self):
        # self.filling = self.CR.filling.update(
        #     self.OR.filling).update(
        #         self.Fuel.filling).update(
        #     self.Blanket.filling)
        self.filling = self.CR.filling | self.OR.filling | self.Fuel.filling | \
            self.Blanket.filling | list(self.Fuel.filling)[0].filling | \
            list(self.Blanket.filling)[0].filling
