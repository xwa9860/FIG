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
	if a_comp.fill is not None:
            return a_comp.fill.generate_output()    
	else:
            return ''
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
            # generate cell cid uid fill uid/ mat nb
            if not a_anComp.fill == None:
                print '%s has a filling universe(id=%d)' %(
                a_anComp.name, a_anComp.fill.gen.univ.id) 
                fill_card = 'fill %d ' % a_anComp.fill.gen.univ.id
            else:
                assert len(a_anComp.mat_list) == 1, \
                    '''%s has more than one material: %s, should be
                    separated into multiple component.''' %(
                        a_anComp.name, a_anComp.mat_list)
                fill_card = a_anComp.mat_list[0].name
            cell_text = (
                'cell %d %d %s ' % (
                    a_anComp.gen.cell.id,
                    a_anComp.gen.univ.id,
                    fill_card))
            # generate surfaces
            text = ''
            i = 0
            for surf in a_anComp.surf_list:
                if surf:
                    text += surf.text
                    cell_text += ('%d ' % (math.pow(-1, i)*surf.id))
                i = i+1
            text += cell_text + '\n'
            # generate higher level universes that fills this component
            #if not a_anComp.fill == None:
            #    text += a_anComp.fill.generate_output()
            return text
