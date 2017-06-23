#!/usr/bin/python

from FIG.triso import Triso
from FIG.mat import Fuel
from FIG.pb import FPb
import config
import os

TEMP = [900, 900, 800, 900, 1000, 800, 800, 800, 800, 800, 770]


fuel_input = '%sfuel_mat%d' %(config.FLUX_WALL_AVE_FOLDER,
 1)
fuel1 = Fuel(TEMP[1], 'fuel_name1', fuel_input)
fuel2 = Fuel(TEMP[1], 'fuel_name2', fuel_input)
fuel3 = Fuel(TEMP[1], 'fuel_name3', fuel_input)
tr = Triso(TEMP[2:7], [fuel1, fuel2, fuel3])


print(tr.generate_output())
print('triso material input script\n')
for mat in tr.mat_list:
    print(mat.generate_output())
