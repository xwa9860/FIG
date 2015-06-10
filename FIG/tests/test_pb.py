#!/usr/bin/python
from pb import FPb
from triso import Triso
from mat import Fuel
from coolant import Coolant
TEMP = [800.0, 900.0, 1000.0, 800.0, 800.0, 800.0, 800.0, 800.0, 770.0]


i = 1
fuel_name = 'fuel%d' % i
fuel_input = 'fuel_mat/average/fuel_comp%d' % 1
fuel = Fuel(TEMP[1], fuel_name, fuel_input)
tr = Triso(TEMP[2:7], fuel)

cool_temp = 800.0
cool = Coolant(800.0)
pb = FPb(tr, TEMP[0], TEMP[7])
f = open('test_pb_res', 'w+')
f.write(pb.generate_output())
for mat in pb.mat_list:
    f.write(mat.generate_output())
f.write(cool.generate_output())
f.write(cool.mat_list[0].generate_output())
