#!/usr/bin/python
from pb import FPb
from triso import Triso
from mat import Fuel, Flibe
from pbed import FuelUnitCell, PBedLat


TEMP = [800.0, 900.0, 1000.0, 800.0, 800.0, 800.0, 800.0, 800.0, 770.0]
cool_temp = 800.0

pb_list = []
f = open('test_pb_res', 'w+')
for i in range(0, 14):
    fuel_name = 'fuel%d' % i
    fuel_input = 'fuel_mat/average/fuel_comp%d' % 1
    fuel = Fuel(TEMP[1], fuel_name, fuel_input)
    tr = Triso(TEMP[2:7], fuel)
    pb = FPb(tr, TEMP[0], TEMP[7])
    pb_list.append(pb)
fuelbed = FuelUnitCell(pb_list, cool_temp)
fuelfccLattice = PBedLat(fuelbed, 2.568)
f.write(fuelfccLattice.generate_output())
for mat in fuelfccLattice.mat_list:
    f.write(mat.generate_output())
