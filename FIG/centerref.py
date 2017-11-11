'''
changed all the flibe to graphite to see if the thermal flux in the
center reflector is larger than that in the outer reflector
'''
from comp import *
from mat import Graphite, Flibe, B4C, SS316
from infu import GrU, FlibeU, SSU
from crcc_seg_gen import CRCCSegGen
from crcc_seg_univ import CRCCSegU
from mat import B4CT
from infu import B4CU
import math

class CenterRef(Comp):

    def __init__(self, temp):
        name = 'CR'
        gru = GrU(temp)
        Comp.__init__(self, temp, name, [Graphite(temp)], fill=gru)



class CRCC(Comp):

    def __init__(self, temp_rod_CRCC, temp_cool_CRCC, temp_gr):
        name = 'CRCC'
        Comp.__init__(self, temp_rod_CRCC, name, [B4C(temp_rod_CRCC)])
        # center reflector control rod channel, 4 axial zones
        CRCC_1= CRCC_axial_segment(temp_rod_CRCC, temp_cool_CRCC, temp_gr, 572.85, 430.85, hasCR=False)
        CRCC_2 = CRCC_axial_segment(temp_rod_CRCC, temp_cool_CRCC, temp_gr, 430.85, 272, hasCR=False)
        CRCC_3 = CRCC_axial_segment(temp_rod_CRCC, temp_cool_CRCC, temp_gr, 272, 112.5, hasCR=False)
        CRCC_4 = CRCC_axial_segment(temp_rod_CRCC, temp_cool_CRCC, temp_gr, 112.5, 41.6, hasCR=False)
        self.comp_dict = {
            'CRCC1': CRCC_1,
            'CRCC2': CRCC_2,
            'CRCC3': CRCC_3,
            'CRCC4': CRCC_4,
            }


class CRCC_axial_segment(Comp):

    def __init__(self, temp_rod, temp_cool, temp_gr, zt, zb, hasCR=True, hasLiner=False):
        name = 'CRCC'
        self.zt = zt
        self.zb = zb
        self.hasCR = hasCR
        self.hasLiner = hasLiner
        self.temp_rod = temp_rod
        self.temp_cool = temp_cool
        self.temp_gr = temp_gr
        crcc_segu = CRCCSegU()
        Comp.__init__(self, 0, name, [], fill=crcc_segu, gen=CRCCSegGen())
        xandys = self.calculate_coolant_channel_locations()
        self.define_channels(xandys)
        self.define_sub_comps(xandys)

    def calculate_coolant_channel_locations(self):
        '''compute x's and y's for the 8 coolant channels in the center reflector
        and output them in a dictionary
        TODO: check the value for R
        '''
        xandy = {'x': [], 'y': []}
        R = 27.5  # the channels are situated at 27.5cm from the center
                  # and at 8 evenly distributed angles
        for i in range(8):
            angle = i*2*math.pi/8.0
            xandy['x'].append(R*math.cos(angle))
            xandy['y'].append(R*math.sin(angle))
        return xandy

    def define_channels(self, xandys):
        self.channels = {}
        for i in range(len(xandys['x'])):
              name = ''.join(['channel', str(i)])
              channel = PadComp(self.temp_cool, name,
                                self.mat_list,
                                self.zb,
                                self.zt,
                                0,
                                0,
                                20,
                                35,
                                -(i*45+15),
                                -(i*45-15),
                                fill=self.fill)
              self.channels[str(i)+'channel'] = channel


    def define_sub_comps(self, xandys):
        self.sub_comps = {}
        self.sub_comps['CRCC_cool'] = CRCC_Cool(self.temp_cool, self.zb, self.zt, xandys)
        self.sub_comps['CRCC_gr'] = CRCC_gr(self.temp_gr, self.zb, self.zt, xandys)
        self.sub_comps['CRCC_liner'] = CRCC_liner(self.temp_cool, self.zb, self.zt, self.hasLiner, xandys)
        self.sub_comps['Control_rod'] = Control_rod(self.temp_rod, self.zb, self.zt, self.hasCR, xandys)


class CRCC_Cool(Comp):

    def __init__(self, temp, zb, zt, locations):
        '''
        coolant between the control rod(cross) and the liner
        '''
        name = 'CRCC_cool'
        # flibeu = FlibeU(temp)
        gru = GrU(temp)
        Comp.__init__(self, temp, name, [Graphite(temp)], fill=gru)
        self.define_comps(zb, zt, locations)

    def define_comps(self, zb, zt, locations):
        self.comp_dict = {}
        # 8 coolant channels
        for i in range(len(locations['x'])):
            name = ''.join(['cool', str(i)])
            coolant = AnnuCrossCylComp(self.temp, name,
                                      self.mat_list,
                                      zb,
                                      zt,
                                      locations['x'][i],
                                      locations['y'][i],
                                      4,
                                      1,
                                      5-0.5,
                                      fill=self.fill)
            self.comp_dict[str(i)+'cool'] = coolant



class CRCC_liner(Comp):

    def __init__(self, temp, zb, zt, hasLiner, locations):
        ''' control rod channel liner'''
        name = 'CRCC_liner'
        if hasLiner:
          fillu = SSU(temp)
          mat = SS316(temp)
        else:
          # fillu = FlibeU(temp)
          # mat = Flibe(temp)
          fillu = GrU(temp)
          mat = Graphite(temp)
        Comp.__init__(self, temp, name, [mat], fill=fillu)
        self.define_comps(zb, zt, locations)

    def define_comps(self, zb, zt, locations):
        self.comp_dict = {}
        for i in range(len(locations['x'])):
                name = ''.join(['liner', str(i)])
                liner = AnnuCylComp(self.temp, name,
                                    self.mat_list,
                                    5-0.5,
                                    5,
                                    zb,
                                    zt,
                                    locations['x'][i],
                                    locations['y'][i],
                                    locations['x'][i],
                                    locations['y'][i],
                                    fill=self.fill)
                self.comp_dict[str(i)+'ss'] = liner


class CRCC_gr(Comp):

    def __init__(self, temp, zb, zt, locations):
        ''' graphite for super-homogenization'''
        name = 'CRCC_gr'
        gru = GrU(temp)
        Comp.__init__(self, temp, name, [Graphite(temp)], fill=gru)
        self.define_comps(zb, zt, locations)

    def define_comps(self, zb, zt, locations):
        self.comp_dict = {}
        # 8 coolant channels
        for i in range(len(locations['x'])):
              name = ''.join(['gr', str(i)])
              gr = AnnuPadCylComp(self.temp, name,
                              self.mat_list,
                              zb,
                              zt,
                              locations['x'][i],
                              locations['y'][i],
                              5,
                              0, 0, 20, 35, -(i*45+15), -(i*45 - 15),
                              fill=self.fill)
              self.comp_dict[str(i)+'gr'] = gr



class Control_rod(Comp):

    def __init__(self, temp, zb, zt, hasCR, locations):
        name = 'CRCC_rod'
        if hasCR:
          fillu = B4CU(temp)
          mat = B4C(temp)
        else:
          # fillu = FlibeU(temp)
          # mat = Flibe(temp)
          fillu = GrU(temp)
          mat = Graphite(temp)
        Comp.__init__(self, temp, name, [mat], fill=fillu)
        self.define_comps(zb, zt, locations)

    def define_comps(self, zb, zt, locations):
        self.comp_dict = {}
        # 8 coolant channels
        for i in range(len(locations['x'])):
              name = ''.join(['rod', str(i)])
              rod = CrossComp(self.temp,
                              name,
                              self.mat_list,
                              zb,
                              zt,
                              locations['x'][i],
                              locations['y'][i],
                              4,
                              1,
                              fill=self.fill)
              self.comp_dict[str(i)+'rod'] = rod

