#!/usr/bin/python
from gen import Gen
from serp_concept import Universe, Cell, Surface
from more_itertools import unique_everseen
#  "List unique elements, preserving order. Remember all elements ever seen."


class PBedGen(Gen):

    def __init__(self, dir_name='serp_input/'):
        Gen.__init__(self, dir_name)

    def parse(self, a_pbed, input_file, type):
        if type == 's':
            str_list = []
            str_list.append(
                '%%---Pebble unit cell with position from input file\n' +
                'pbed %d %d "%s"\n' %
                (self.univ.id, a_pbed.coolant.gen.univ.id,
                 input_file))
            str_list.append(
                '%%---Coolant in the unit cell\n' +
                a_pbed.coolant.generate_output())
            str_list.append(
                '%%---Pebbles in the unit cell(pbed)\n')
            for pb in list(unique_everseen(a_pbed.pb_list)):
                str_list.append(pb.generate_output())
            return ''.join(str_list)


class FCCGen(Gen):
    file_id = 0 # increment the name by 1 for multiple fuel unit cells

    def __init__(self, dir_name='serp_input/',  verbose=False, pbed_file_prefix = 'fpb_pos'):
        FCCGen.file_id += 1
        Gen.__init__(self, dir_name, verbose)
        self.pbed_file_prefix_and_id = pbed_file_prefix+str(FCCGen.file_id)

    def generate_pos_file(self, a_fcc, dir_loc, pbed_file_prefix):
        ''' generate pebble position file for Serpent from packing fraction'''
        pb_pos_input = (
            '%f  %f  %f 1.5 %d\n' % (a_fcc.pitch,  a_fcc.pitch,  a_fcc.pitch, 0) +
            '-%f  %f  %f 1.5 %d\n' % (a_fcc.pitch, a_fcc.pitch, a_fcc.pitch, 0) +
            '-%f -%f  %f 1.5 %d\n' % (a_fcc.pitch, a_fcc.pitch, a_fcc.pitch, 0) +
            ' %f -%f  %f 1.5 %d\n' % (a_fcc.pitch, a_fcc.pitch, a_fcc.pitch, 0) +
            ' %f  %f -%f 1.5 %d\n' % (a_fcc.pitch, a_fcc.pitch, a_fcc.pitch, 0) +
            '-%f  %f -%f 1.5 %d\n' % (a_fcc.pitch, a_fcc.pitch, a_fcc.pitch, 0) +
            '-%f -%f -%f 1.5 %d\n' % (a_fcc.pitch, a_fcc.pitch, a_fcc.pitch, 0) +
            ' %f -%f -%f 1.5 %d\n' % (a_fcc.pitch, a_fcc.pitch, a_fcc.pitch, 0) +
            ' %f  0. 0.  1.5 %d\n' % (a_fcc.pitch, 0) +
            '-%f  0. 0.  1.5 %d\n' % (a_fcc.pitch, 0) +
            ' 0.  %f  0. 1.5 %d\n' % (a_fcc.pitch, 0) +
            ' 0.  -%f 0. 1.5 %d\n' % (a_fcc.pitch, 0) +
            ' 0.  0. %f  1.5 %d\n' % (a_fcc.pitch, 0) +
            ' 0.  0. -%f 1.5 %d\n' % (a_fcc.pitch, 0))
        file_name = pbed_file_prefix+'_%d' % (a_fcc.packing_fraction * 100)
        f = open(dir_loc+file_name, 'w+')
        i = 0
        for line in pb_pos_input.splitlines(True):
            line = line.replace(
                '1.5 0', '1.5 %d' % (a_fcc.pb_list[i].gen.univ.id))
            i = i+1
            f.write(line)
        f.close()
        return file_name

    def parse(self, a_fcc, type):
        # dir_loc is the folder path for the generated position file
        dir_loc = self.dir_name
        file_name = self.generate_pos_file(a_fcc, dir_loc, self.pbed_file_prefix_and_id)
        return self.parse1(a_fcc, file_name, 's')

    def parse1(self, a_pbed, input_file, type):
        if type == 's':
            str_list = []
            str_list.append(
                '%%---Pebble unit cell with position from input file\n' +
                'pbed %d %d "%s"\n' %
                (self.univ.id, a_pbed.coolant.gen.univ.id,
                 input_file))
            str_list.append(
                '%%---Coolant in the unit cell\n' +
                a_pbed.coolant.generate_output())
            str_list.append(
                '%%---Pebbles in the unit cell(pbed)\n')
            for pb in list(unique_everseen(a_pbed.pb_list)):
                str_list.append(pb.generate_output())
            return ''.join(str_list)


class GFCCGen(Gen):

    def generate_pos_file(self, a_g_fcc, dir_loc):
        pb_pos_input = (  # template, pb univ id to be replaced
            '%f  %f  %f 1.5 %d\n' % (a_g_fcc.pitch,  a_g_fcc.pitch,  a_g_fcc.pitch, 0) +
            '-%f  %f  %f 1.5 %d\n' % (a_g_fcc.pitch, a_g_fcc.pitch, a_g_fcc.pitch, 0) +
            '-%f -%f  %f 1.5 %d\n' % (a_g_fcc.pitch, a_g_fcc.pitch, a_g_fcc.pitch, 0) +
            ' %f -%f  %f 1.5 %d\n' % (a_g_fcc.pitch, a_g_fcc.pitch, a_g_fcc.pitch, 0) +
            ' %f  %f -%f 1.5 %d\n' % (a_g_fcc.pitch, a_g_fcc.pitch, a_g_fcc.pitch, 0) +
            '-%f  %f -%f 1.5 %d\n' % (a_g_fcc.pitch, a_g_fcc.pitch, a_g_fcc.pitch, 0) +
            '-%f -%f -%f 1.5 %d\n' % (a_g_fcc.pitch, a_g_fcc.pitch, a_g_fcc.pitch, 0) +
            ' %f -%f -%f 1.5 %d\n' % (a_g_fcc.pitch, a_g_fcc.pitch, a_g_fcc.pitch, 0) +
            ' %f  0. 0.  1.5 %d\n' % (a_g_fcc.pitch, 0) +
            '-%f  0. 0.  1.5 %d\n' % (a_g_fcc.pitch, 0) +
            ' 0.  %f  0. 1.5 %d\n' % (a_g_fcc.pitch, 0) +
            ' 0.  -%f 0. 1.5 %d\n' % (a_g_fcc.pitch, 0) +
            ' 0.  0. %f  1.5 %d\n' % (a_g_fcc.pitch, 0) +
            ' 0.  0. -%f 1.5 %d\n' % (a_g_fcc.pitch, 0))
        file_name = 'gpb_pos_%d' %(a_g_fcc.packing_fraction*100)
        f = open(dir_loc+file_name, 'w+')
        for line in pb_pos_input.splitlines(True):
            line = line.replace(
                '1.5 0', '1.5 %d' % a_g_fcc.pb_list[0].gen.univ.id)
            f.write(line)
        f.close()
        return file_name

    def parse(self, a_g_pbed, type):
      # dir_loc is the folder path for the generated position file
        if type == 's':
            dir_loc = self.dir_name
            input_file = self.generate_pos_file(a_g_pbed, dir_loc)
            str_list = []
            str_list.append(
                '\n%%---Graphite pebble bed(or unit cell) from input file\n' +
                'pbed %d %d "%s"\n' %
                (self.univ.id, a_g_pbed.coolant.gen.univ.id,
                 input_file))
            str_list.append(
                '%%---coolant in the graphite pb unit cell\n')
            str_list.append(a_g_pbed.coolant.generate_output())
            str_list.append(
                '%%---Graphite pebbles in a unit pebble bed(assuming all graphite pbs are the same)\n')
            str_list.append(a_g_pbed.pb_list[0].generate_output())
            return ''.join(str_list)


class PBedLatGen(Gen):

    def __init__(self, dir_name='serp_input/'):
        self.univ = Universe()   # univ of pbed lattice
        self.dir_name = dir_name

    def parse(self, a_pbed_lat, type):
        if type == 's':
            str_list = []
            cell = Cell()
            s = Surface()
            univ = Universe()  # univ of the cubic cell containing the unit cell
            str_list.append(
                '%%---FCC unit cell lattice\n' +
                'surf %d cube 0. 0. 0. %f\n' %
                (s.id, a_pbed_lat.pitch*2) +
                'cell %d  %d fill %d -%d\n' %
                (cell.id, univ.id, a_pbed_lat.pbed.gen.univ.id, s.id) +
                'lat %d 6 0. 0. %f %d\n' %
                (self.univ.id, a_pbed_lat.pitch*2,
                 univ.id))
            str_list.append(a_pbed_lat.pbed.generate_output())
            return '\n'.join(str_list)
