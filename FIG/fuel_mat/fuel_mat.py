#!/usr/bin/python
import config


class FuelMat():

    def __init__(self):
        '''
        self.comp : in this dictionary the keys are a string of the nuclide ID 
        and the values are the compositions in moles
        '''
        self.comp = {}
        self.lib = 'pwru50'
        self.tmp = 0
        self.scat = ''

    def __add__(self, other):
        # this method adds to materials together

        new = FuelMat()
        for nuclide in self.comp.keys():
            if nuclide in other.comp:
                new.comp[nuclide] = self.comp[nuclide] + other.comp[nuclide]
            else:
                new.comp[nuclide] = self.comp[nuclide]
        for nuclide in other.comp.keys():
            if nuclide in self.comp:
                # do nothing these nuclides have already been summed
                pass
            else:
                new.comp[nuclide] = other.comp[nuclide]

        #new.tmp = self.tmp*self.moles() + other.tmp*other.moles()

        return new

    def __mul__(self, other):
        new = FuelMat()
        new.tmp = self.tmp
        for nuclide in self.comp.keys():
            new.comp[nuclide] = other*self.comp[nuclide]
        return new

    def import_comp_from_file(self, inputpath):
        '''
        read isotope name and fraction from an input file
        that has 2 columns:
            isotope and fraction
        update self.material.comp
        '''
        pairs = open(inputpath).readlines()
        for line in pairs:
            self.comp[line.split()[0]] = float(line.split()[1])

    def import_comp_from_mcnp_file(self, inputpath):
        '''
        read isotope name and fraction from an mcnp input file
        update self.material.comp
        '''
        with open(inputpath, 'r+') as f:
            for line in f:
                isotope = line.split()[0].split('.')[0]
                fraction = line.split()[1]
                if isotope not in config.NOT_IN_SERPENT_LIB:
                    self.comp[isotope] = float(fraction)
                else:
                    print('isotope %s fraction =0 or not in serp lib'
                          % isotope)

    def write_mat_to_file(self, comp_path=None):
        '''
        write mateiral composition to output file
        with 2 columns:
            isotope and fraction
        '''
        mat_comp_text = []
        for pair in self.comp:
            mat_comp_text.append('%s %e\n' % (pair, self.comp[pair]))
        if comp_path:
            with open(comp_path, 'w+') as csvfile:
                csvfile.write(''.join(mat_comp_text))
        return mat_comp_text

    def write_mat_to_mcnp_file(self,
                               mat_name,
                               temp='1.00588E+03K',
                               comp_path=None):
        fuel_comp = []
        for iso in self.comp:
            fuel_comp.append('%s%s.%2f %e' % ('        ',
                                              iso, 72, self.comp[iso]))
            fuel_comp = ''.join(fuel_comp)
        mat_name = [mat_name, '$ tmp=%s\n' % (temp)]
        mat_comp = ''.join([mat_name, fuel_comp])
        if comp_path:
            with open(comp_path, 'w+') as outputf:
                outputf.write(mat_comp)
        return mat_comp
