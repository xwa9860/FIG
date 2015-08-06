'''
generate bu.eq type file from Tommy's MCNP input file
'''
#!/usr/bin/python
import mocup
import re
import os
import csv

#input file name that is used to get volume of each region
input_file_volume = 'mk1.txt'
output_fuel_comp_loc='vol_ave_mcnp'

def get_volume(inputf):
    '''
    search for volume of 20 zones from MCNP input file and make a list of volume vol
    '''
    with open(inputf, 'r+') as f:
        lines = f.readlines()
        vol = [[None for _ in range(5)] for _ in range(4)]
        for i in range(1, 5):
            for j in range(1, 6):
                linenb = 0
                string_to_find = 'c Depletion Zones %d%d' % (i, j)
                for k in range(linenb, len(lines)):
                    linenb = linenb + 1
                    if string_to_find in lines[k]:
                        vol[i-1][j-1] = float(lines[k+3].split('=')[1])
    return vol


def write_vol(vol, outf):
    '''
    write a list of volume into a csv file
    '''
    with open(outf, 'w+') as csvfile:
        fieldnames = ['zone', 'volume']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for R in range(1, 5):
            for Z in range(1, 6):
                writer.writerow({'zone': '%d%d' %
                                 (R, Z), 'volume': '%f' %
                                 vol[R-1][Z-1]})
    csvfile.close()


def import_mcnpcomp(mat, comp_loc):
    '''
    read isotope name and fraction from comp_loc
    generate mat.comp as a dictionary
    '''
    mat.comp = {}
    pairs = open(comp_loc).readlines()
    for line in pairs:
        mat.comp[line.split()[0]] = float(line.split()[1])
    # print mat.comp
    return mat


def add_mat():
    '''
    calculate volume averaged fuel composition over the core, for 8 different depletion passes
    '''
    for B in range(1, 9):
        for R in range(1, 5):
            for Z in range(1, 6):
                node_mat = mocup.material()
                # mat_loc = 'moi_files/moi.%d%d%d00.eq.pch' % (R,Z,B)
                mat_loc = 'comp_from_mk1/m%d%d%d00' % (R, Z, B)
                mat = mocup.material()
                mat = import_mcnpcomp(mat, mat_loc)
                node_mat = node_mat + mat * float(volume[R-1][Z-1])
        mat_loc = output_fuel_comp_loc+'/bu%d.eq' % (B)
        mat_comp = []
        for pair in node_mat.comp:
            mat_comp.append('%s %e\n' % (pair, node_mat.comp[pair]))
        open(mat_loc, 'w+').write(''.join(mat_comp))


def write_mat(isotope, outf):

    with open(outf, 'w+') as csvfile:
        fieldnames = ['zones']
        for B in range(1,9):
            fieldnames.append('mat_pass%d'%i)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for B in range(1, 9):
            mat_dict ={}
            for R in range(1, 5):
                for Z in range(1, 6):
                    mat_loc = 'comp_from_mk1/m%d%d%d00' % (R, Z, B)
                    mat = mocup.material()
                    mat = import_mcnpcomp(mat, mat_loc)
            writer.writerow({'zone': '%d%d' %
                                 (R, Z), 'volume': '%f' %
                                 vol[R-1][Z-1]})
    csvfile.close()

volume = get_volume(input_file_volume)
write_vol(volume, 'volume.csv')
add_mat()
