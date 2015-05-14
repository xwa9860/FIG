#!/usr/bin/python
from serp_concept import Universe, Cell, SphSurf
from mat import Mat
from gen import Gen


class GPbGen(Gen):
    # wrote_surf = False

    def __init__(self):
        self.univ = Universe()
        self.surf1 = SphSurf()

    def parse(self, a_g_pb, type):
        if type == 's':
            str_list = []
            self.surf1.set_r(a_g_pb.r)
            str_list.append('%%---surf for graphite pebble\n')
            str_list.append(self.surf1.text)
            cell = Cell()
            filling_card = []
            for fil in a_g_pb.filling:
                if isinstance(fil, Mat):
                    filling_card += fil.name
                else:
                    filling_card += 'fill %d ' % fil.gen.univ.id
            str_list.append(
                '%%---Graphite pebble\n' +
                'cell %d %d %s -%d\n' %
                (cell.id, self.univ.id, ''.join(filling_card), self.surf1.id))
            return ''.join(str_list)


class FuelPbGen(Gen):
    # wrote_surf = False

    def __init__(self):
        self.univ = Universe()
        self.surf1 = SphSurf()
        self.surf2 = SphSurf()

    def parse(self, a_f_pb, type):
        if type == 's':
            str_list = []
            # if not FuelPbGen.wrote_surf:
            self.surf1.set_r(a_f_pb.r_config['CentralGraphite'])
            str_list.append('%%---surf for fuel  pebbles\n')
            str_list.append(self.surf1.text)
            self.surf2.set_r(a_f_pb.r_config['TrLat'])
            str_list.append(self.surf2.text)
            # FuelPbGen.wrote_surf = True
            cell1 = Cell()
            cell2 = Cell()
            cell3 = Cell()
            str_list.append(
                '%%---Fuel pebble\n' +
                'cell %d %d CentralGraphite -%d\n' %
                (cell1.id, self.univ.id, self.surf1.id) +
                'cell %d %d fill %d %d -%d\n' %
                (cell2.id, self.univ.id, a_f_pb.tr_lat.gen.univ.id,
                 self.surf1.id, self.surf2.id)  # +
                # a_f_pb.triso.generate_output() +
                # a_f_pb.tr_lat.generate_output()
                + 'cell %d %d Shell %d\n' %
                (cell3.id, self.univ.id, self.surf2.id))
            return ''.join(str_list)
