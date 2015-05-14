#!/usr/bin/python
from serp_concept import Cell
from serp_concept import Universe
from serp_concept import Surface
from gen import Gen


class CoolantGen(Gen):

    def __init__(self):
        self.cell = Cell()
        self.univ = Universe()

    def parse(self, a_cool, type):
        surf = Surface()
        if type == 's':
            str_list = []
            str_list.append(
                '%%---Coolant\n' +
                'surf %d inf\ncell %d %d %s -%d\n' %
                (surf.id, self.cell.id, self.univ.id,
                 list(a_cool.filling)[0].name, surf.id))
            return ''.join(str_list)
