#!/usr/bin/python
'''
get fuel composition from Mark1.txt file
and write to output folder
'''
import config
inputfilepath = config.INPUT_MCNP_FILE
outputfolder = config.OUTPUT_RAW_COMPS_FOLDER

for p in range(1, 9):
    for R in range(1, 5):
        for Z in range(1, 6):
            mat_name = 'm%d%d%d00' % (R, Z, p)
            mat_comp = []
            nb_isotope = 0
            with open(inputfilepath, 'r+') as inputfile:
                for line in inputfile:
                    if mat_name in line:
                        print(line)
                        ne = inputfile.readline()
                        print(ne)
                        while 'm' not in ne:
                            mat_comp.append(ne.split()[0]+' %.8e' % (
                                float(ne.split()[1])+float(ne.split()[3]))
                                + '\n')
                            e = inputfile.readline()
                            nb_isotope = nb_isotope + 1
            with open(''.join([outputfolder, mat_name]), 'w+') as outputf:
                outputf.write(''.join(mat_comp))
