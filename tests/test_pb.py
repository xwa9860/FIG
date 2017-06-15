#!/usr/bin/python
from pb import FPb
from triso import Triso
from mat import Fuel
from coolant import Coolant
import config
TEMP = [800.0, 900.0, 1000.0, 800.0, 800.0, 800.0, 800.0, 800.0, 770.0]


fuel_input = '%sfuel_mat%d' %(config.OUTPUT_FLUX_WALL_AVE_COMP_FOLDER,
 1)
fuel1 = Fuel(TEMP[1], 'fuel_name1', fuel_input)
fuel2 = Fuel(TEMP[1], 'fuel_name2', fuel_input)
fuel3 = Fuel(TEMP[1], 'fuel_name3', fuel_input)
tr = Triso(TEMP[2:7], [fuel1, fuel2, fuel3])

cool_temp = 800.0
cool = Coolant(800.0)
pb = FPb(tr, TEMP[0], TEMP[7])
f = open('test_pb_res', 'w+')
f.write(pb.generate_output())
for mat in pb.mat_list:
    f.write(mat.generate_output())
f.write(cool.generate_output())
f.write(cool.mat_list[0].generate_output())
