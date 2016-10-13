'''
This is a core_w_channel class, contains a FHR core with coolant
channels inside the center and outer reflectors
# all dimensions in cm
# all temperatures in K
'''
#!/usr/bin/python
from core_gen import CoreGen
from mat import Be, YH2, ZrH2, Graphite
from mat import BeCoolMix, YH2CoolMix, GraphiteCoolMix, ZrH2CoolMix, GraphiteSSCoolMix
from comp import *
from pbed import FuelUnitCell, GraphiteUnitCell, PBedLat
import math


class CenterRef(Comp):

    def __init__(self, temp):
        name = 'CR'
        Comp.__init__(self, temp, name, [Graphite(temp)])


class OuterRef(Comp):

    def __init__(self, temp):
        name = 'OR'
        Comp.__init__(self, temp, name, [Be(temp)])


class CenterRef_CoolantChannel(Comp):

    def __init__(self, temp, cool_temp):
        name = 'CRCC'
        Comp.__init__(self, temp, name, [GraphiteCoolMix(cool_temp)])


class OuterRef_CoolantChannel(Comp):

    def __init__(self, temp, cool_temp):
        name = 'ORCC'
        Comp.__init__(self, temp, name, [BeCoolMix(cool_temp)])


class Fuel(Comp):

    def __init__(self, fpb_list, cool_temp):
        name = 'FuelZone'
        self.unit_cell = FuelUnitCell(fpb_list, cool_temp)
        self.unit_cell_lat = PBedLat(self.unit_cell, self.unit_cell.pitch)
        Comp.__init__(self, fpb_list[0].temp, name, self.unit_cell_lat.mat_list,
                      fill=self.unit_cell_lat)


class Blanket(Comp):

    def __init__(self, pb_temp, cool_temp):
        self.pb_temp = pb_temp
        self.cool_temp = cool_temp
        name = 'Blanket'
        self.unit_cell = GraphiteUnitCell(self.pb_temp, self.cool_temp)
        self.unit_cell_lat = PBedLat(self.unit_cell, self.unit_cell.pitch)
        Comp.__init__(self, pb_temp, name, self.unit_cell_lat.mat_list,
                      fill=self.unit_cell_lat)


class Core(Comp):

    def __init__(
            self,
            fpb_list,
            temp_CR,
            temp_g_CRCC,
            temp_cool_CRCC,
            temp_OR,
            temp_g_ORCC,
            temp_cool_ORCC,
            temp_cool_F,
            temp_Blanket,
            temp_cool_B):
        assert(len(fpb_list) == 14), 'pb_list length is wrong, expected 14 pbs, got %d' % len(
            fpb_list)
        self.comp_dict = {
            'CR': CenterRef(temp_CR),
            #'CRCC': CenterRef_CoolantChannel(temp_g_CRCC, temp_cool_CRCC),
            'OR': OuterRef(temp_OR),
            'ORCC': OuterRef_CoolantChannel(temp_g_ORCC, temp_cool_ORCC),
            'Fuel': Fuel(fpb_list, temp_cool_F),
            'Blanket': Blanket(temp_Blanket, temp_cool_B)
        }
        self.CR = self.comp_dict['CR']
        #self.CRCC = self.comp_dict['CRCC']
        self.OR = self.comp_dict['OR']
        self.ORCC = self.comp_dict['ORCC']
        self.Fuel = self.comp_dict['Fuel']
        self.Blanket = self.comp_dict['Blanket']
        self.define_CR(self.CR.temp, self.CR.name)
        #self.define_CRCC(self.CRCC.temp, self.CRCC.name)
        self.define_OR(self.OR.temp, self.OR.name)
        self.define_ORCC(self.ORCC.temp, self.ORCC.name)
        self.define_Fuel(self.Fuel.temp, self.Fuel.name)
        self.define_Blanket(self.Blanket.temp, self.Blanket.name)

        self.whole_core = CylComp(fpb_list[0].temp,
                                  'whole_core',
                                  self.Fuel.act.mat_list,
                                  41.6,
                                  572.85,
                                  165,
                                  fill=self.Fuel.act)
        # contains not only self.Fuel but other three component, but they are in
        # the same universe, only need it to get the univ id
        name = 'FullCore'
        mat_list = self.collect_mat()
        Comp.__init__(self, fpb_list[0].temp, name, mat_list, CoreGen())

    def define_CR(self, temp, name):
        self.CR.comp_dict = {}
        # ---------------------------------------------------------
        # center reflector
        # entrance zone
        self.CR.zb_ent = 41.6  # in the design, CR starts at 15.7cm
        self.CR.zt_ent = 127.5
        self.CR.r_ent = 35+10
        self.CR.ent = CylComp(temp, name, self.CR.mat_list, self.CR.zb_ent,
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
            self.CR.mat_list,
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
        self.CR.act = CylComp(temp, name, self.CR.mat_list, self.CR.zb_act,
                              self.CR.zt_act, self.CR.r_act)
        self.CR.comp_dict['act'] = self.CR.act
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
                                     self.CR.r_conv)
        self.CR.comp_dict['conv'] = self.CR.conv
        # defueling
        self.CR.r_defuel = self.CR.r_conv
        self.CR.zb_defuel = self.CR.zt_conv
        self.CR.zt_defuel = self.CR.zb_defuel + 80
        self.CR.defuel = CylComp(temp, name,
                                 self.CR.mat_list,
                                 self.CR.zb_defuel,
                                 self.CR.zt_defuel,
                                 self.CR.r_defuel)
        self.CR.comp_dict['defuel'] = self.CR.defuel
        # 8 coolant channels
        xandys = self.calculate_coolant_channel_locations()
        for i in range(len(xandys['x'])):
            self.CR.channel = CylComp(temp, name,
                                      self.CRCC.mat_list,
                                      self.CR.zb_ent,
                                      self.CR.zt_defuel,
                                      10,
                                      xandys['x'][i],
                                      xandys['y'][i])



#    def define_CRCC(self, temp, name):
#        '''
#        CRCC is a 10 cm bande at the outer layer of the center reflector
#        that is a mix of graphite and flibe, to represent the coolant channel
#        in the reflector
#        '''
#        self.CRCC.comp_dict = {}
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
#        # ---------------------------------------------------------
#        # center reflector
#        # entrance zone
#        self.CRCC.zb_ent = 41.6  # in the design, CR starts at 15.7cm
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
#        # diverging
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
#        # active zone
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
#        # Converging
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
#        # negative h means direction to -z
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
#        # defueling
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
    def define_OR(self, temp, name):
        # --------------------------------------------------------
        # Outer reflector
        self.OR.r_outer = 165   # outer radius for the whole o_ref
        self.OR.comp_dict = {}

        # entrance zone
        self.OR.zb_ent = 41.6
        self.OR.zt_ent = 112.5
        self.OR.r_ent = 95.74
        self.OR.ent = AnnuCylComp(temp, name,
                                  self.OR.mat_list,
                                  self.OR.r_ent,
                                  self.OR.r_outer,
                                  self.OR.zb_ent,
                                  self.OR.zt_ent)
        self.OR.comp_dict['ent'] = self.OR.ent

        # diverging  zone
        self.OR.a_div = math.pi*60.0/180
        self.OR.zb_div = 112.5
        self.OR.zt_div = 180.5
        self.OR.r_cone_div = 135   # self.OR.r_ent + \
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
            self.OR.zt_div)

        self.OR.comp_dict['div'] = self.OR.div

        # active zone
        self.OR.r_act = 125 + 10
        self.OR.zb_act = self.OR.zt_div
        self.OR.zt_act = 430.5
        self.OR.act = AnnuCylComp(temp, name,
                                  self.OR.mat_list,
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
            temp, name,
            self.OR.mat_list,
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
                                     self.OR.mat_list,
                                     self.OR.ri_defuel,
                                     self.OR.r_outer,
                                     self.OR.zb_defuel,
                                     self.OR.zt_defuel)
        self.OR.comp_dict['defuel'] = self.OR.defuel

    def define_ORCC(self, temp, name):
        # --------------------------------------------------------
        # Outer reflector with coolant channel
        self.ORCC.comp_dict = {}

        # entrance zone
        self.ORCC.zb_ent = self.OR.zb_ent
        self.ORCC.zt_ent = self.OR.zt_ent
        self.ORCC.ri_ent = self.OR.r_ent - 10
        self.ORCC.ro_ent = self.OR.r_ent
        self.ORCC.ent = AnnuCylComp(temp, name,
                                    self.ORCC.mat_list,
                                    self.ORCC.ri_ent,
                                    self.ORCC.ro_ent,
                                    self.ORCC.zb_ent,
                                    self.ORCC.zt_ent)
        self.ORCC.comp_dict['ent'] = self.ORCC.ent

        # diverging  zone
        self.ORCC.ai_div = math.pi*60.0/180
        self.ORCC.ao_div = math.pi*60.0/180
        self.ORCC.zb_div = 112.5
        self.ORCC.zt_div = 180.5
        self.ORCC.ri_cone_div = 125
        self.ORCC.hi_cone_div = -self.ORCC.ri_cone_div * \
            math.tan(self.ORCC.ai_div)
        self.ORCC.ro_cone_div = self.OR.r_cone_div
        self.ORCC.ho_cone_div = -self.ORCC.ro_cone_div * \
            math.tan(self.ORCC.ao_div)
        #  negative sign means direction -z

        self.ORCC.div = AnnuConeConeComp(temp, name,
                                         self.ORCC.mat_list,
                                         self.ORCC.ri_cone_div,
                                         self.ORCC.hi_cone_div,
                                         self.ORCC.zt_div,
                                         self.ORCC.ro_cone_div,
                                         self.ORCC.ho_cone_div,
                                         self.ORCC.zt_div,
                                         self.ORCC.zb_div,
                                         self.ORCC.zt_div)

        self.ORCC.comp_dict['div'] = self.ORCC.div

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
                                    self.ORCC.zt_act)

        self.ORCC.comp_dict['act'] = self.ORCC.act

        # convergeing zone
        self.ORCC.ri_cone_conv = self.ORCC.ri_act
        self.ORCC.ro_cone_conv = self.ORCC.ro_act
        self.ORCC.ai_conv = 60.0 * math.pi/180
        self.ORCC.ao_conv = 60.0 * math.pi/180
        self.ORCC.hi_cone_conv = self.ORCC.ri_cone_conv *\
            math.tan(self.ORCC.ai_conv)
        self.ORCC.ho_cone_conv = self.ORCC.ro_cone_conv *\
            math.tan(self.ORCC.ao_conv)
        self.ORCC.zb_conv = self.ORCC.zt_act
        self.ORCC.zt_conv = self.OR.zt_conv

        self.ORCC.conv = AnnuConeConeComp(temp, name,
                                          self.ORCC.mat_list,
                                          self.ORCC.ri_cone_conv,
                                          self.ORCC.hi_cone_conv,
                                          self.ORCC.zb_conv,
                                          self.ORCC.ro_cone_conv,
                                          self.ORCC.ho_cone_conv,
                                          self.ORCC.zb_conv,
                                          self.ORCC.zb_conv,
                                          self.ORCC.zt_conv)

        self.ORCC.comp_dict['conv'] = self.ORCC.conv

        # defueling zone
        self.ORCC.zb_defuel = self.ORCC.zt_conv
        self.ORCC.zt_defuel = self.CR.zt_defuel
        self.ORCC.ri_defuel = self.OR.ri_defuel - 10
        self.ORCC.ro_defuel = self.OR.ri_defuel

        self.ORCC.defuel = AnnuCylComp(temp, name,
                                       self.ORCC.mat_list,
                                       self.ORCC.ri_defuel,
                                       self.ORCC.ro_defuel,
                                       self.ORCC.zb_defuel,
                                       self.ORCC.zt_defuel)

        self.ORCC.comp_dict['defuel'] = self.ORCC.defuel

    def define_Fuel(self, temp, name):
        # ---------------------------------------------------------
        # fuel zone
        # --------------------------------------------------------
        self.Fuel.comp_dict = {}
        # entrance zone
        self.Fuel.zb_ent = 41.6  # in design report fuel pb starts at 41.6cm
        self.Fuel.zt_ent = self.OR.zt_ent
        self.Fuel.ri_ent = self.CR.r_ent
        self.Fuel.ro_ent = 75.41
        self.Fuel.ent = AnnuCylComp(temp, name,
                                    self.Fuel.mat_list,
                                    self.Fuel.ri_ent,
                                    self.Fuel.ro_ent,
                                    self.Fuel.zb_ent,
                                    self.Fuel.zt_ent,
                                    fill=self.Fuel.fill)
        self.Fuel.comp_dict['ent'] = self.Fuel.ent
        # diverging  zone 1
        self.Fuel.ro_act = 105
        self.Fuel.a_div1 = math.atan((self.OR.zt_div-self.OR.zb_div) /
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
                                         self.Fuel.mat_list,
                                         self.Fuel.r_cone_div1,
                                         self.Fuel.h_cone_div1,
                                         self.Fuel.z_cone_div1,
                                         self.Fuel.ri_div1,
                                         self.Fuel.zb_div1,
                                         self.Fuel.zt_div1,
                                         fill=self.Fuel.fill)
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
                                          self.Fuel.mat_list,
                                          self.Fuel.ri_div2,
                                          self.Fuel.h_cone_i_div2,
                                          self.Fuel.zb_div2,
                                          self.Fuel.ro_cone_div2,
                                          self.Fuel.ho_cone_div2,
                                          self.Fuel.zo_cone_div2,
                                          self.Fuel.zb_div2,
                                          self.Fuel.zt_div2,
                                          fill=self.Fuel.fill)
        self.Fuel.comp_dict['div2'] = self.Fuel.div2

        # diverging  zone 3
        self.Fuel.a_div3 = self.Fuel.a_div1
        self.Fuel.zb_div3 = self.Fuel.zt_div2
        self.Fuel.zt_div3 = self.OR.zt_div
        self.Fuel.r_i_div3 = self.CR.r_act
        self.Fuel.r_cone_div3 = self.Fuel.ro_cone_div2
        self.Fuel.h_cone_div3 = self.Fuel.ho_cone_div2
        self.Fuel.div3 = AnnuConeCylComp(temp, name,
                                         self.Fuel.mat_list,
                                         self.Fuel.r_cone_div3,
                                         self.Fuel.h_cone_div3,
                                         self.Fuel.zt_div3,
                                         self.Fuel.r_i_div3,
                                         self.Fuel.zb_div3,
                                         self.Fuel.zt_div3,
                                         fill=self.Fuel.fill)
        self.Fuel.comp_dict['div3'] = self.Fuel.div3

        # active zone
        self.Fuel.zb_act = self.Fuel.zt_div3
        self.Fuel.zt_act = self.CR.zt_act
        self.Fuel.act = AnnuCylComp(temp, name,
                                    self.Fuel.mat_list,
                                    self.CR.r_act,
                                    self.Fuel.ro_act,
                                    self.Fuel.zb_act,
                                    self.Fuel.zt_act,
                                    fill=self.Fuel.fill)
        self.Fuel.comp_dict['act'] = self.Fuel.act
        # convergeing zone
        self.Fuel.zb_conv = self.Fuel.zt_act
        self.Fuel.zt_conv = self.CR.zt_conv
        self.Fuel.ri_conv = self.CR.r_conv
        self.Fuel.ai_conv = 60.0 * math.pi/180
        self.Fuel.hi_conv = -1.0*self.Fuel.ri_conv*math.tan(self.Fuel.ai_conv)
        self.Fuel.ro_conv = self.Fuel.ro_act
        self.Fuel.ao_conv = math.atan((self.Fuel.zt_conv - self.Fuel.zb_conv) /
                                      (self.Fuel.ro_act - 80))
        self.Fuel.ho_conv = self.Fuel.ro_conv*math.tan(self.Fuel.ao_conv)
        self.Fuel.conv = AnnuConeConeComp(temp, name,
                                          self.Fuel.mat_list,
                                          self.Fuel.ri_conv,
                                          self.Fuel.hi_conv,
                                          self.Fuel.zt_conv,
                                          self.Fuel.ro_conv,
                                          self.Fuel.ho_conv,
                                          self.Fuel.zb_conv,
                                          self.Fuel.zb_conv,
                                          self.Fuel.zt_conv,
                                          fill=self.Fuel.fill)
        self.Fuel.comp_dict['conv'] = self.Fuel.conv

        # defueling zone
        self.Fuel.zb_defuel = self.Fuel.zt_conv
        self.Fuel.zt_defuel = self.OR.zt_defuel
        self.Fuel.ri_defuel = self.CR.r_defuel
        self.Fuel.ro_defuel = self.Fuel.ro_act -\
            (self.Fuel.zt_conv - self.Fuel.zb_conv)/math.tan(self.Fuel.ao_conv)
        self.Fuel.defuel = AnnuCylComp(temp, name,
                                       self.Fuel.mat_list,
                                       self.Fuel.ri_defuel,
                                       self.Fuel.ro_defuel,
                                       self.Fuel.zb_defuel,
                                       self.Fuel.zt_defuel,
                                       fill=self.Fuel.fill)
        self.Fuel.comp_dict['defuel'] = self.Fuel.defuel

    def define_Blanket(self, temp, name):
        # -------------------------------------------------------------
        # Blanket
        # ------------------------------------------------------------
        self.Blanket.comp_dict = {}
        # entrance zone
        self.Blanket.zb_ent = 41.6  # in design report 41.6
        self.Blanket.zt_ent = self.OR.zt_ent
        self.Blanket.ri_ent = self.Fuel.ro_ent
        self.Blanket.ro_ent = self.ORCC.ri_ent
        self.Blanket.ent = AnnuCylComp(temp, name,
                                       self.Blanket.mat_list,
                                       self.Blanket.ri_ent,
                                       self.Blanket.ro_ent,
                                       self.Blanket.zb_ent,
                                       self.Blanket.zt_ent,
                                       fill=self.Blanket.fill)
        self.Blanket.comp_dict['ent'] = self.Blanket.ent

        # diverging  zone
        self.Blanket.ai_div = self.Fuel.a_div1
        self.Blanket.zb_div = self.Blanket.zt_ent
        self.Blanket.zt_div = self.OR.zt_div
        self.Blanket.ri_div = self.Fuel.div3.ro
        self.Blanket.h_cone_i_div = -1.0 * self.Blanket.ri_div * \
            math.tan(self.Blanket.ai_div)
        self.Blanket.ao_div = math.pi*60.0/180
        self.Blanket.ro_div = self.ORCC.div.ri
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
        self.Blanket.ri_act = self.Fuel.act.ro
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
        self.Blanket.ri_defuel = self.Fuel.ro_defuel
        self.Blanket.ro_defuel = self.ORCC.ri_defuel
        self.Blanket.defuel = AnnuCylComp(temp, name,
                                          self.Blanket.mat_list,
                                          self.Blanket.ri_defuel,
                                          self.Blanket.ro_defuel,
                                          self.CR.zb_defuel,
                                          self.CR.zt_defuel,
                                          fill=self.Blanket.fill)
        self.Blanket.comp_dict['defuel'] = self.Blanket.defuel

    def collect_mat(self):
        mat_list = []
        for comp in self.comp_dict:
            for mat in self.comp_dict[comp].mat_list:
                if mat not in mat_list:
                    mat_list.append(mat)
        return mat_list

    def calculate_coolant_channel_locations():
        '''compute x's and y's for the 8 coolant channels in the center reflector
        and output them in a dictionary
        TODO: check the value for R
        '''
        xandy = {}
        R = 27.5  # the channels are situated at 27.5cm from the center
                  # and at 8 evenly distributed angles
        for i in range(8):
            angle = i*math.pi/8.0
            xandy['x'][i] = R*math.cos(angle)
            xandy['y'][i] = R*math.sin(angle)
        return xandy
