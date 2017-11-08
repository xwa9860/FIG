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
                #univ = Universe()
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
            str_list.append('set pop 10000 2000 500\n')
            str_list.append('set bc 1\n')
            str_list.append('set ures 1\n')
            # str_list.append('%OR, ORCC, CR, CRCC, Vsl, Dcmer, barrel, Blanket, Fuel\n')
            #str_list.append('%OR, ORCC, CR, CRCC1, CRCC2, CRCC3, CRCC4, Vsl, Dcmer, barrel, Blanket, FuelW, FuelA1, FuelA2, FuelA3, FuelA4\n')
            # str_list.append('set gcu 28 29 27 25 52 53 54 50 32\n')
            #str_list.append('set gcu 306 307 121 122 168 214 260 346 347 348 344 326 310 314 318 322\n')
            #str_list.append('set nfg 8\n')
            #str_list.append('5.8e-8\n')
            #str_list.append('1.9e-7\n')
            #str_list.append('5e-7\n')
            #str_list.append('4e-6\n')
            #str_list.append('4.8e-5\n')
            #str_list.append('2.5e-2\n')
            #str_list.append('1.4\n')
            #str_list.append('set opti 1\n')

            #str_list.append('\n %% detectors\n')
            #detnb = 1 
            #for i in range(8):
            #  str_list.append('det %d  dm fuel1pb%d dr -8 fuel1pb%d\n' %(i*3, i+1, i+1))
            #  str_list.append('det %d  dm fuel2pb%d dr -8 fuel2pb%d\n' %(i*3+1, i+1, i+1))
            #  str_list.append('det %d  dm fuel3pb%d dr -8 fuel3pb%d\n' %(i*3+2, i+1, i+1))

            str_list.append('%% detector for power\n')
            str_list.append('%det <name> dn 1 <rmin> <rmax> <nr>  <amin> <amax> <na> <zmin> <zmax> <nz>\n')
            str_list.append('det 1 dr -8 void dn 1 0  178 90 0 360 1 41 573 267\n')

            str_list.append('%% detector for thermal neutron flux\n')
            str_list.append('ene 1 1 1E-11 0.625E-6\n')
            str_list.append('det 2 de 1 dn 1 0  178 90 0 360 1 41 573 267\n')
            str_list.append('%% detector for fast neutron flux\n')
            str_list.append('ene 2 1 0.625E-6 200\n')
            str_list.append('det 3 de 2 dn 1 0  178 90 0 360 1 41 573 267\n')
            str_list.append('\n%%---Plot the geometry\n')
            str_list.append('plot 1 700 700 0 %% yz cross plane at x=0\n')
            str_list.append('plot 2 700 700 0 %% xz cross plane at y=0\n')
            str_list.append('plot 3 700 700 300 %% xy cross plane at z=300\n')

            return ''.join(str_list)


