#!/usr/bin/python
from gen import Gen
from serp_concept import Cell, Universe, Detector


class CoreGen(Gen):
    def generate_sbatch_file(self, dir_name):
        with open('template.sub', 'r') as rf:
            text = rf.read()
            with open(''.join([dir_name, 'sbatch.sub']), 'w') as f:
                f.write(text)

    def parse(self, a_core, type):
        if type == 's':
            self.generate_sbatch_file(self.dir_name)
            str_list = []
            # define title and library path
            str_list.append('''%%---Cross section data library path\n''')
            str_list.append('set title "FHR core"\n' +
                            'set acelib "/global/home/groups/ac_nuclear/serpent/xsdata/endfb7/sss_endfb7u.xsdata"\n')

            # define geometry, cells, universe in the core in different files
            univ = Universe()
            for key1 in a_core.comp_dict:
                filename = '%s' % key1
                comp_str = []
                comp_str.append('\n%%---%s\n' % key1)
                for key2 in a_core.comp_dict[key1].comp_dict:
                    comp_str.append('%%---%s\n' % key2)
                    a_core.comp_dict[key1].comp_dict[
                        key2].gen.set_univId(univ.id)
                    comp_str.append(
                        a_core.comp_dict[key1].comp_dict[key2].generate_output()
                    )
                comp_str.append(a_core.comp_dict[key1].generate_output())
                open(self.dir_name+filename, 'w+').write(''.join(comp_str))
                str_list.append('include "%s"\n' %filename)
            #open(dir+'Fuel', 'a').write(a_core.Fuel.unit_cell_lat2.generate_output())

            # define the whole core as universe 0, and cell 'outside'
            a_core.whole_core.gen.set_univId(0)
            str_list.append('\n%%---Core as a whole, universe 0\n' +
                            a_core.whole_core.generate_output())
            str_list.append(
                '\n%%---Outside\ncell %d 0 outside %d\n' %
                (Cell().id, a_core.whole_core.surf_list[1].id))

            # Material
            filename = 'coreMaterials'
            str_list.append('include "%s"' %filename)
            mat_str = []
            for mat in a_core.mat_list:
                if self.verbose:
                  print('create material %r' % mat)
                mat_str.append(mat.generate_output())
            open(self.dir_name+filename, 'w+').write(''.join(mat_str))

            # define neutron source and BC
            str_list.append('\n%%---Neutron source and BC\n')
            str_list.append('\n%%---set pop neutron-per-cycle cycles skip-cycles\n')
            str_list.append('set pop 200000 500 200\n')
            str_list.append('set bc 1\n')
            str_list.append('set ures 1\n')
            str_list.append('set gcu 3 6 9 12 15 18 21 24\n')
            str_list.append('set nfg 8\n')
            str_list.append('5.8e-8\n')
            str_list.append('1.9e-7\n')
            str_list.append('5e-7\n')
            str_list.append('4e-6\n')
            str_list.append('4.8e-5\n')
            str_list.append('2.5e-2\n')
            str_list.append('1.4\n')
            str_list.append('set opti 1\n')
            str_list.append('\n %% detectors\n')
            str_list.append('det 1  dm fuel1pba1 dr -8 fuel1pba1\n') 
            str_list.append('det 2  dm fuel2pba1 dr -8 fuel2pba1\n') 
            str_list.append('det 3  dm fuel3pba1 dr -8 fuel3pba1\n') 
            str_list.append('det 4  dm fuel1pba2 dr -8 fuel1pba2\n') 
            str_list.append('det 5  dm fuel2pba2 dr -8 fuel2pba2\n') 
            str_list.append('det 6  dm fuel3pba2 dr -8 fuel3pba2\n') 
            str_list.append('det 7  dm fuel1pba3 dr -8 fuel1pba3\n') 
            str_list.append('det 8  dm fuel2pba3 dr -8 fuel2pba3\n') 
            str_list.append('det 9  dm fuel3pba3 dr -8 fuel3pba3\n') 
            str_list.append('det 10 dm fuel1pba4 dr -8 fuel1pba4\n')
            str_list.append('det 11 dm fuel2pba4 dr -8 fuel2pba4\n')
            str_list.append('det 12 dm fuel1pba4 dr -8 fuel1pba4\n')
            str_list.append('\n%%---Plot the geometry\n')
            str_list.append('plot 1 700 700 0 %% yz cross plane at x=0\n')
            str_list.append('plot 2 700 700 0 %% xz cross plane at y=0\n')
            str_list.append('plot 3 700 700 100 %% xy cross plane at z=100\n')

            # define detectors
            # For cross sections
            # fission cross section
            # str_list.append(
            #     '%%---fission cross section in each kind of pebble\n')
            # for pb in a_core.comp_dict['Fuel'].unit_cell.fpb_list:
            #     str_list.append(
            #      '%%---neutron flux in fuel in pebble %s\n' %
            #     pb.triso.mat_list[0].name)
            #     text = 'dm %s\n' %pb.triso.mat_list[0].name
            #     det_flux = Detector(text)
            #     str_list.append(det_flux.generate_output())
            #     text = 'du %d dr -6 %s dt 3 %d\n' % (
            #         a_core.comp_dict['Fuel'].comp_dict['act'].gen.univ.id,
            #         pb.triso.mat_list[0].name,
            #         det_flux.id)
            #     det_fission = Detector(text)
            #     str_list.append(det_fission.generate_output())

            # # capture cross section
            # str_list.append(
            #     '%%---capture cross section in the major components\n')
            # for key in a_core.comp_dict:
            #     str_list.append(
            #         '\n%%---total flux in %s identified by its univ id\n' % key)
            #     text = 'du %d\n' % a_core.comp_dict[
            #         key].comp_dict['act'].gen.univ.id
            #     det1 = Detector(text)
            #     str_list.append(det1.generate_output())
            #     str_list.append(
            #         '%%---capture rate in %s\n' % key)
            #     str_list.append(
            #         a_core.comp_dict[key].generate_capture_detector())
           ##  For reaction rate distribution
            # str_list.append('%%---spacial mesh\n')

            #     # text = 'dx
                # det_r = Detector(text)
            return ''.join(str_list)


