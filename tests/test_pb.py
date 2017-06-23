#!/usr/bin/python
from FIG.pb import FPb
from FIG.triso import Triso
from FIG.mat import Fuel
from FIG.coolant import Coolant
import config
TEMP = [800.0, 900.0, 1000.0, 800.0, 800.0, 800.0, 800.0, 800.0, 770.0]


fuel_input = config.FRESH_FILE
fuel1 = Fuel(TEMP[1], 'fuel_name1', fuel_input)
fuel2 = Fuel(TEMP[1], 'fuel_name2', fuel_input)
fuel3 = Fuel(TEMP[1], 'fuel_name3', fuel_input)
tr = Triso(TEMP[2:7], [fuel1, fuel2, fuel3])

pb = FPb(tr, TEMP[0], TEMP[7])
f = open('tests/test_pb_res', 'w+')
f.write(pb.generate_output())
for mat in pb.mat_list:
    f.write(mat.generate_output())
cool = Coolant(800.0)
f.write(cool.generate_output())
f.write(cool.mat_list[0].generate_output())

fuel_input = config.FRESH_FILE
fuel = Fuel(900, 'fuel_name1', fuel_input)
TEMP = [800.0, 900.0, 1000.0, 800.0, 800.0]
tr = Triso(TEMP, [fuel])
pb = FPb(tr, 900.0, 870.0)
cool = Coolant(800.0)

# write output to file
f = open('pb', 'w+')
f.write(pb.generate_output())
for mat in pb.mat_list:
    f.write(mat.generate_output())
f.write(cool.generate_output())
f.write(cool.mat_list[0].generate_output())
