'''
get volumes of each of the 4x5 zones and write it to volume.csv
'''
import csv
import config


def get_volume(inputf=config.INPUT_MCNP_FILE):
    '''
    search for volume of 20 zones from a MCNP input file
    and make a list of volume vol
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
