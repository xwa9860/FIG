#!/usr/bin/python
from serp_concept import Universe
from gen import Gen


class TrisoGen(Gen):
    first_time = True

    def __init__(self, dir_name='serp_input'):
        self.particle = Universe()
        self.dir_name = dir_name

    def parse(self, a_triso, type):
        if type == 's':
            str_list = []
            str_list.append('''%%---Triso particle \nparticle %d''' %
                            self.particle.id)
            for mat in a_triso.mat_list:
                if 'Matrix' in mat.name:
                    str_list.append(mat.name + '\n')
                    continue
                str_list.append('%s %.4f' %
                                (mat.name, a_triso.r_config[mat.name]))
            # if TrisoGen.first_time:
            #    for mat in a_triso.mat_list:
            #         str_list.append(mat.generate_output())
            #         TrisoGen.first_time = False
            # else:
            #     # str_list.append(a_triso.mat_list[0].generate_output())
            return '\n'.join(str_list)


class TrisoLatticeGen(Gen):

    def __init__(self, dir_name='serp_input'):
        self.univ = Universe()
        self.dir_name = dir_name

    def parse(self, a_triso_lattice, type):
        if type == 's':
            str_list = []
            str_list.append(
                '%%---Triso  lattice\n'+
                'lat %d 6 0. 0. %.8f %d\n' %
                (self.univ.id,
                 a_triso_lattice.pitch,
                 a_triso_lattice.triso_particle.gen.particle.id))
            return '\n'.join(str_list)
