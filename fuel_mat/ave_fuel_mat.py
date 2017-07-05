'''
weighted averaged fuel mat associated with a pass number
'''
import config
from fuel_mat import FuelMat


def sum_comp(weights,
             raw_comps_folder=config.MCNP_RAW_FOLDER,
             passno=1):
    '''
    calculate weighted averaged fuel composition over the core,
    from 20 zones,
    for 8 different depletion passes
    weights: 5x4x8 matrix
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

def sum_comp_2_zones(weights,
             raw_comps_folder=config.MCNP_RAW_FOLDER,
             passno=[1, 1],
             pbnb = 1):
    '''
    calculate weighted averaged fuel composition over the core,
    from 20 zones,
    for 8 different depletion passes
    weights: 5x4x8 matrix
    '''
    new_mat = FuelMat()
    for R in range(1, 5):
      for Z in range(1, 6): 
            mat = FuelMat()
            if Z == 2 and R in range(2, 5):
              mat_loc = ''.join(
                        [raw_comps_folder, 'm%d%d%d00' % (R, Z, passno[1])])
            else:
              mat_loc = ''.join(
                        [raw_comps_folder, 'm%d%d%d00' % (R, Z, passno[0])])
            print(mat_loc)
            mat.import_comp_from_mcnp_file(mat_loc)
            new_mat = new_mat + mat * float(weights[Z-1][R-1][pbnb-1])
            print(weights[Z-1][R-1][pbnb-1])
    return new_mat
