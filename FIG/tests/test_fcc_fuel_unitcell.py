#!/usr/bin/python
from triso import Triso
from pbed import FuelFCC, PBedLat

fuel_temp_list=[800, 800, 800, 800, 800, 800, 800, 650]
cool_temp = 800
unit_cell = FuelFCC(fuel_temp_list, cool_temp, 'fpb_pos.inp')
unit_cell_lattice = PBedLat(unit_cell, unit_cell.p)
f = open('test_fcc_fuel_unitcell_res', 'w+')
f.write(unit_cell.generate_output())
f.write(unit_cell_lattice.generate_output())

for fil in unit_cell.filling:
    f.write(fil.name + '\n')
    f.write(fil.generate_output())

