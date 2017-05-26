#!/usr/bin/python
'''
parse material composition files 
from mcnp to serpent
from beau to serpent
'''
import config


class mat_parser:

    '''
    convert material composition files from one format to another
    '''

    # isotopes not defined in serpent library
    not_in_serpent_lib = config.NOT_IN_SERPENT_LIB
            # above are isotopes from origen results but not in serpent library

    def __init__(self, inp, outp):
        self.inp = inp
        self.outp = outp

    def beau2serp(self):
        '''
        convert fuel material composition files from
        BEAU depletion calculation results to serpent syntax
        '''
        with open(self.outp, 'w+') as f:
            with open(self.inp, 'r+') as input:
                lines = input.readlines()
                for line in lines:
                    if len(line) < 20:
                        pass
                    elif line[7] != str(0) and line[7] != str(1):
                        if not line[8:18] == '0.0000E+00' \
                                and line[2:6] not in mat_parser.not_in_serpent_lib:
                            f.write(line[2: 6])
                            f.write(' ')
                            f.write(line[8: 18])
                            f.write('\n')
                        else:
                            print('isotope %s fraction =0 or not in serp lib')
                    else:
                        if not line[9:19] == '0.0000E+00' and\
                                line[2:7] not in mat_parser.not_in_serpent_lib:
                            f.write(line[2: 7])
                            f.write(' ')
                            f.write(line[9: 19])
                            f.write('\n')
                        else:
                            print('isotope %s fraction =0 or not in serp lib'
                                  %line[2:7])
        f.close
        input.close


    def mcnp_2_serp(self):
        mat_dict = {}
        text = []
        with open(self.inp, 'r+') as f:
            for line in f:
                isotope = line.split()[0].split('.')[0]
                fraction = line.split()[1]
                if isotope not in mat_parser.not_in_serpent_lib:
                    mat_dict[isotope] = fraction
                    text.append(isotope + ' '+fraction+'\n')
                else:
                    print('isotope %s fraction =0 or not in serp lib' %isotope)
            with open(self.outp, 'w+') as of:
                of.write(''.join(text))
        of.close()
        f.close()
