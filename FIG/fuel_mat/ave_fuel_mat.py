'''
weighted averaged fuel mat associated with a pass number
'''
import config
from fuel_mat import FuelMat


def sum_comp(weights,
             raw_comps_folder=config.RAW_COMPS_FOLDER,
             passno=1):
    '''
    calculate weighted averaged fuel composition over the core,
    from 20 zones,
    for 8 different depletion passes
    weights: 4x5x8 matrix
    '''
    new_mat = FuelMat()
    for R in range(1, 5):
        for Z in range(1, 6):
            mat = FuelMat()
            mat_loc = ''.join(
                      [raw_comps_folder, 'm%d%d%d00' % (R, Z, passno)])
            print(mat_loc)
            mat.import_comp_from_mcnp_file(mat_loc)
            new_mat = new_mat + mat * float(weights[Z-1][R-1][passno-1])
            print(weights[Z-1][R-1][passno-1])
    return new_mat
