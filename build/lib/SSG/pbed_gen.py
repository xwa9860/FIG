#!/usr/bin/python
from gen import Gen
from serp_concept import Universe, Cell, Surface

class PBedGen(Gen):

    def parse(self, a_pbed, type):
        if type == 's':
            str_list = []
            str_list.append(
                '%%---Pebble bed(here means unit cell) from input file\n' +
                'pbed %d %d "%s"\n' %
                (self.univ.id, a_pbed.surrounding.gen.univ.id,
                 a_pbed.input_file))
            str_list.append('%%---Pebbles in the unit cell(pbed)\n')
            for pb in a_pbed.pb_list:
                str_list.append(pb.generate_output())
            return ''.join(str_list)


class FCCGen(PBedGen):

    def generate_pos_file(self, a_fcc):
        pb_pos_input = (
            '%f  %f  %f 1.5 %d\n' % (a_fcc.p,  a_fcc.p,  a_fcc.p, 0) +
            '-%f  %f  %f 1.5 %d\n' % (a_fcc.p, a_fcc.p, a_fcc.p, 0) +
            '-%f -%f  %f 1.5 %d\n' % (a_fcc.p, a_fcc.p, a_fcc.p, 0) +
            ' %f -%f  %f 1.5 %d\n' % (a_fcc.p, a_fcc.p, a_fcc.p, 0) +
            ' %f  %f -%f 1.5 %d\n' % (a_fcc.p, a_fcc.p, a_fcc.p, 0) +
            '-%f  %f -%f 1.5 %d\n' % (a_fcc.p, a_fcc.p, a_fcc.p, 0) +
            '-%f -%f -%f 1.5 %d\n' % (a_fcc.p, a_fcc.p, a_fcc.p, 0) +
            ' %f -%f -%f 1.5 %d\n' % (a_fcc.p, a_fcc.p, a_fcc.p, 0) +
            ' %f  0. 0.  1.5 %d\n' % (a_fcc.p, 0) +
            '-%f  0. 0.  1.5 %d\n' % (a_fcc.p, 0) +
            ' 0.  %f  0. 1.5 %d\n' % (a_fcc.p, 0) +
            ' 0.  -%f 0. 1.5 %d\n' % (a_fcc.p, 0) +
            ' 0.  0. %f  1.5 %d\n' % (a_fcc.p, 0) +
            ' 0.  0. -%f 1.5 %d\n' % (a_fcc.p, 0))

        f = open(a_fcc.input_file, 'w+')
        i = 0
        for line in pb_pos_input.splitlines(True):
            line = line.replace(
                '1.5 0', '1.5 %d' % (a_fcc.pb_list[i].gen.univ.id))
            i = i+1
            f.write(line)
        f.close()

    def parse(self, a_fcc, type):
        self.generate_pos_file(a_fcc)
        return PBedGen.parse(self, a_fcc, 's')

class GFCCGen(PBedGen):

    def generate_pos_file(self, a_g_fcc):
        pb_pos_input = (  # template, pb univ id to be replaced
            '%f  %f  %f 1.5 %d\n' % (a_g_fcc.p,  a_g_fcc.p,  a_g_fcc.p, 0) +
            '-%f  %f  %f 1.5 %d\n' % (a_g_fcc.p, a_g_fcc.p, a_g_fcc.p, 0) +
            '-%f -%f  %f 1.5 %d\n' % (a_g_fcc.p, a_g_fcc.p, a_g_fcc.p, 0) +
            ' %f -%f  %f 1.5 %d\n' % (a_g_fcc.p, a_g_fcc.p, a_g_fcc.p, 0) +
            ' %f  %f -%f 1.5 %d\n' % (a_g_fcc.p, a_g_fcc.p, a_g_fcc.p, 0) +
            '-%f  %f -%f 1.5 %d\n' % (a_g_fcc.p, a_g_fcc.p, a_g_fcc.p, 0) +
            '-%f -%f -%f 1.5 %d\n' % (a_g_fcc.p, a_g_fcc.p, a_g_fcc.p, 0) +
            ' %f -%f -%f 1.5 %d\n' % (a_g_fcc.p, a_g_fcc.p, a_g_fcc.p, 0) +
            ' %f  0. 0.  1.5 %d\n' % (a_g_fcc.p, 0) +
            '-%f  0. 0.  1.5 %d\n' % (a_g_fcc.p, 0) +
            ' 0.  %f  0. 1.5 %d\n' % (a_g_fcc.p, 0) +
            ' 0.  -%f 0. 1.5 %d\n' % (a_g_fcc.p, 0) +
            ' 0.  0. %f  1.5 %d\n' % (a_g_fcc.p, 0) +
            ' 0.  0. -%f 1.5 %d\n' % (a_g_fcc.p, 0))

        f = open(a_g_fcc.input_file, 'w+')
        for line in pb_pos_input.splitlines(True):
            line = line.replace(
                '1.5 0', '1.5 %d' % a_g_fcc.gpb.gen.univ.id)
            f.write(line)
        f.close()

    def parse(self, a_g_pbed, type):
        if type == 's':
            str_list = []
            str_list.append(
                '\n%%---Graphite pebble bed(or unit cell) from input file\n' +
                'pbed %d %d "%s"\n' %
                (self.univ.id, a_g_pbed.surrounding.gen.univ.id,
                 a_g_pbed.input_file))
            str_list.append('%%---Graphite pebbles in a unit pebble bed\n')
            str_list.append(a_g_pbed.gpb.generate_output())
            self.generate_pos_file(a_g_pbed)
            return ''.join(str_list)


class PBedLatGen(Gen):

    def __init__(self):
        self.univ = Universe()

    def parse(self, a_pbed_lat, type):
        if type == 's':
            str_list = []
            cell = Cell()
            s = Surface()
            univ = Universe()
            str_list.append(
                '%%---FCC unit cell lattice\n' +
                'surf %d cube 0. 0. 0. %f\n' %
                (s.id, a_pbed_lat.pitch*2) +
                'cell %d  %d fill %d -%d\n' %
                (cell.id, univ.id, a_pbed_lat.pbed.gen.univ.id, s.id) +
                'lat %d 6 0. 0. %.8f %d\n' %
                (self.univ.id, a_pbed_lat.pitch*2,
                 univ.id))
            return '\n'.join(str_list)


