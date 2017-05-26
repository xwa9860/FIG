import volume
import config
import pandas as pd
from ave_fuel_mat import sum_comp
import numpy as np

volmat = np.array(volume.get_volume()).reshape((4, 5, 1))
volmat = np.swapaxes(volmat, 0, 1)

fluxdf = pd.read_csv(config.FLUX_CSV_PATH, header=None)
fluxmat = fluxdf.values.reshape((5, 4, 8))

weightmat = np.multiply(fluxmat, volmat)
weightmat = np.multiply(fluxmat, weightmat)


for i in range(1, 9):
    flux_ave_fuel = sum_comp(weightmat)
    outputfile = config.OUTPUT_FLUX_AVE_COMP_FOLDER + 'fuel_mat%d' % i
    flux_ave_fuel.write_mat_to_file(comp_path=outputfile)
