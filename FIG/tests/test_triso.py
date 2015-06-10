#!/usr/bin/python

from triso import Triso
from mat import Fuel
from pb import FPb
import os

TEMP = [800, 900, 1000, 800, 800, 800, 800, 800, 770]


i = 1
fuel_name = 'fuel%d' % i
fuel_input = 'fuel_mat/average/fuel_comp%d' % 1
fuel = Fuel(TEMP[1], fuel_name, fuel_input)
tr = Triso(TEMP[2:7], fuel)
#fuelpebble = FuelPebble(tr, TEMP[0], TEMP[8])

f = open('test_triso_res', 'w+')
f.write('triso input script\n' + tr.generate_output())
f.write('triso material input script\n')
for mat in tr.mat_list:
    f.write(mat.generate_output())
f.close
