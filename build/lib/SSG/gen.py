#!/usr/bin/python
from serp_concept import Cell, Universe, Detector
from mat import Mat
import math


class Gen:

    def __init__(self):
        self.cell = Cell()
        self.univ = Universe()

    def set_univId(self, id):
        self.univ.setId(id)

    def parse(self, a_comp, type):
        pass

    def parse_capture_det(self, a_comp, type):
        if type == 's':
            str_list = []
            for mat in a_comp.matSet:
                text = 'du %d dr -2 %s\n' % (
                    a_comp.gen.univ.id,
                    mat.name)
                det_capture = Detector(text)
                str_list.append(det_capture.generate_output())
            return ''.join(str_list)


class AnnularCompGen(Gen):

    def parse(self, a_anComp, type):
        if type == 's':
            i = 0
            if len(a_anComp.filling) > 1:
                print '%s.filling is more than one' %a_anComp.name
            else:
                for fil in a_anComp.filling:
                    fill_card = ''
                    if isinstance(fil, Mat):
                        fill_card += fil.name
                    else:
                        fill_card += 'fill %d ' % fil.gen.univ.id
                    cell_text = (
                        'cell %d %d %s ' %
                        (a_anComp.gen.cell.id,
                        a_anComp.gen.univ.id,
                        fill_card))
                text = ''
                for s in a_anComp.surf_list:
                    if s:
                        text += s.text
                        cell_text += ('%d ' % (math.pow(-1, i)*s.id))
                    i=i+1
                text += cell_text + '\n'
                return text
