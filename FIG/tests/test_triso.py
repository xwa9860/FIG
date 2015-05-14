#!/usr/bin/python

from triso import Triso
from mat import Fuel
from pb import FuelPebble
import os

fuel_temp_list = [800, 900, 1000, 800, 800, 800, 800, 800, 770]


i = 1
fuel_name = 'fuel%d' % i
fuel_input = 'fuel_mat/average/fuel_comp%d' % 1
fuel = Fuel(fuel_temp_list[1], fuel_name, fuel_input)
tr = Triso(fuel_temp_list[2:7], fuel)
fuelpebble = FuelPebble(tr, fuel_temp_list[0], fuel_temp_list[8])

f = open('test_triso_res', 'w+') 
f.write('triso input script\n' + tr.generate_output())
f.write('triso material input script\n')
for fil in tr.filling:
    f.write(fil.generate_output())
f.close
