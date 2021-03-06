#!/usr/bin/python
from gen import Gen
from serp_concept import Cell, Universe, Detector, Surface
from FIG.pb_gen import FuelPbGen
from FIG.pbed_gen import FCCGen


class CoreGen(Gen):

    def parse(self, a_core, type):
        if type == 's':
            self.generate_sbatch_file(self.dir_name)

            str_list = []
            # define title and library path
            str_list.append('''%%---Cross section data library path\n''')
            str_list.append('set title "FHR core"\n' +
                            'set acelib "/global/home/groups/co_nuclear/serpent/xsdata/endfb7/sss_endfb7u.xsdata"\n')
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
            str_list.append('set power 2.36E8\n')
            
            if a_core.purpose == 'XS_gen':
              # generate group constants for comsol
              str_list.append('% OR, ORCC, CR, CRCC1, CRCC2, CRCC3, CRCC4, Barrel, Dcmer, Vessel, Blanket, FuelW, FuelA1, FuelA2, FuelA3, FuelA4\n')
              # str_list.append('% OR 196, ORCC 197, CR 1, CRCC1, CRCC2, CRCC3, CRCC4, Barrel 377, Dcmer 378, Vessel 379, Blanket 370, FuelW 230, FuelA1 258, FuelA2 286, FuelA3 314, FuelA4 342\n')
              str_list.append('set gcu 196 197 1 2 48 94 140 377 378 379 370 230 258 286 314 342\n')
              # str_list.append('set gcu 196 197 1 2 48 94 140 272 273 274 265 209 216 223 230 237\n')
              str_list.append('set nfg 8\n')
              str_list.append('5.8e-8\n')
              str_list.append('1.9e-7\n')
              str_list.append('5e-7\n')
              str_list.append('4e-6\n')
              str_list.append('4.8e-5\n')
              str_list.append('2.5e-2\n')
              str_list.append('1.4\n')
              str_list.append('set opti 1\n')

            # str_list.append('\n %% detectors\n')
            # detnb = 1 
	    #str_list.append('\n %% detector for power fraction in different burnups\n')
            #for i in range(8):
            #  str_list.append('det %d  dm fuel1pbw%d dr -8 fuel1pbw%d\n' %(detnb, i+1, i+1))
              # str_list.append('det %d  dm fuel2pbw%d dr -8 fuel2pbw%d\n' %(detnb+1, i+1, i+1))
              # str_list.append('det %d  dm fuel3pbw%d dr -8 fuel3pbw%d\n' %(detnb+2, i+1, i+1))
            #  detnb = detnb + 1

            #for i in range(8):
            #  str_list.append('det %d  dm fuel1pba1%d dr -8 fuel1pba1%d\n' %(detnb, i+1, i+1))
              # str_list.append('det %d  dm fuel2pba1%d dr -8 fuel2pba1%d\n' %(detnb+1, i+1, i+1))
              # str_list.append('det %d  dm fuel3pba1%d dr -8 fuel3pba1%d\n' %(detnb+2, i+1, i+1))
            #  detnb = detnb + 1

            #str_list.append('%% detector for power\n')
            #str_list.append('%det <name> dn 1 <rmin> <rmax> <nr>  <amin> <amax> <na> <zmin> <zmax> <nz>\n')
            #str_list.append('det %d dr -8 void dn 1 0  175 35 0 360 1 41 573 38\n' %detnb)
            #detnb = detnb + 1

            #str_list.append('%% detector for thermal neutron flux\n')
            #str_list.append('ene 1 1 1E-11 0.625E-6\n')
            #str_list.append('det %d de 1 dn 1 0  175 35 0 360 1 41 573 38\n' %detnb)
            #detnb = detnb + 1

            #str_list.append('%% detector for fast neutron flux\n')
            #str_list.append('ene 2 1 0.625E-6 200\n')
            #str_list.append('det %d de 2 dn 1 0  175 35 0 360 1 41 573 38\n' %detnb)
            #detnb = detnb + 1

            #str_list.append('%% detector for fast neutron flux in matrix for thermal conductivity correlation\n')
            # str_list.append('ene 2 1 0.1 200\n')
            # str_list.append('det %d de 2 dm matrix\n' %detnb)
            # detnb = detnb + 1

            #str_list.append('\n%%---Plot the geometry\n')
            #str_list.append('plot 1 700 700 0 %% yz cross plane at x=0\n')
            #str_list.append('plot 2 700 700 0 %% xz cross plane at y=0\n')
            #str_list.append('plot 3 700 700 300 %% xy cross plane at z=300\n')

            return ''.join(str_list)

    def generate_sbatch_file(self, dir_name):
        with open('template.sub', 'r') as rf:
            text = rf.read()
            with open(''.join([dir_name, 'sbatch.sub']), 'w') as f:
                f.write(text)


