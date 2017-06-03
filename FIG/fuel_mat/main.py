import volume
import config
import pandas as pd
from ave_fuel_mat import sum_comp
import numpy as np

# the weight(volume or flux) matrices have dimension 5x4x8
volmat = np.array(volume.get_volume()).reshape((4, 5, 1))
volmat = np.swapaxes(volmat, 0, 1)

fluxdf = pd.read_csv(config.FLUX_CSV_PATH, header=None)
fluxmat = fluxdf.values.reshape((5, 4, 8))
print(fluxmat)

fluxmat_act = np.zeros((5, 4, 8))
for passno in range(1, 9):
  for R in range(2, 5):
    print(fluxmat[2][R-1][passno-1])
    fluxmat_act[2][R-1][passno-1] = fluxmat[2][R-1][passno-1]
print(fluxmat_act)

fluxmat_wall = fluxmat
for passno in range(1, 9):
  for R in range(2, 5):
    fluxmat_wall[2][R-1][passno-1] = 0
print('fluxmat')
print(fluxmat)
print('one element')
print(fluxmat[2,3,2])


#weightmat = np.multiply(fluxmat, weightmat)


for i in range(1, 9):
    flux_ave_fuel1 = sum_comp(fluxmat_wall, passno=i)
    outputfile1 = config.OUTPUT_FLUX_WALL_AVE_COMP_FOLDER + 'fuel_mat%d' % i
    flux_ave_fuel1.write_mat_to_file(comp_path=outputfile1)

print('compute for zone2')
for i in range(1, 9):
    flux_ave_fuel2 = sum_comp(fluxmat_act, passno=i)
    outputfile2 = config.OUTPUT_FLUX_ACT_AVE_COMP_FOLDER + 'fuel_mat%d' % i
    flux_ave_fuel2.write_mat_to_file(comp_path=outputfile2)
