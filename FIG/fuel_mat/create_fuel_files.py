'''
create fuel material composition file for serpent input
from mcnp fuel format to serpent fuel format
'''
#!/usr/bin/python
from mat_parser import mat_parser

INPDIR = 'vol_ave_mcnp/'
OUTPDIR = 'vol_ave_mcnp/'


for i in range(1, 9):
    inputfile = INPDIR + 'bu%d.eq' % i
    outputfile = OUTPDIR + 'fuel_mat%d' % i
    parser = mat_parser(inputfile, outputfile)
    parser.mcnp_2_serp()
