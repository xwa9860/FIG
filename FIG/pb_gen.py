#!/usr/bin/python
from serp_concept import Universe, Cell, SphSurf
from mat import Mat
from gen import Gen


class GPbGen(Gen):

    def __init__(self):
        self.univ = Universe()

    def parse(self, a_g_pb, type):
        if type == 's':
            str_list = []
            str_list.append('%%---surf for graphite pebble\n')
            surf1 = SphSurf()
            surf1.set_r(a_g_pb.r)
            str_list.append(surf1.text)
            cell = Cell()
            str_list.append(
                '%%---Graphite pebble\n' +
                'cell %d %d %s -%d\n' %
                (cell.id, self.univ.id, a_g_pb.mat_list[0].name, surf1.id))
            return ''.join(str_list)


class FuelPbGen(Gen):
    # wrote_surf = False

    def __init__(self):
        self.univ = Universe()

    def parse(self, a_f_pb, type):
        if type == 's':
            str_list = []
            # if not FuelPbGen.wrote_surf:
            surf1 = SphSurf()
            surf2 = SphSurf()
            surf1.set_r(a_f_pb.r_config['CentralGraphite'])
            str_list.append('%%---surf for fuel pebbles\n')
            str_list.append(surf1.text)
            surf2.set_r(a_f_pb.r_config['TrLat'])
            str_list.append(surf2.text)
            # FuelPbGen.wrote_surf = True
            cell1 = Cell()
            cell2 = Cell()
            cell3 = Cell()
            str_list.append(
                '%%---Fuel pebble\n' +
                'cell %d %d CentralGraphite -%d\n' %
                (cell1.id, self.univ.id, surf1.id) +
                'cell %d %d fill %d %d -%d\n' %
                (cell2.id, self.univ.id, a_f_pb.tr_lat.gen.univ.id,
                 surf1.id, surf2.id)   +
                 a_f_pb.triso.generate_output() +
                 a_f_pb.tr_lat.generate_output()
                + 'cell %d %d Shell %d\n' %
                (cell3.id, self.univ.id, surf2.id))
            return ''.join(str_list)
