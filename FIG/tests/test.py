#/usr/bin/python

from ../core_w_channel import Core
import shutil
import os


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

#for i in range(0, 5):
i=0    
dir_name = 'test_res'
mkdir(dir_name)
core = Core(
650+273.15,  # temp_CR
650+273.15,  # temp_g_CRCC
650+273.15,  # temp_cool_CRCC
650+273.15,  # temp_OR
650+273.15,  # temp_g_ORCC
650+273.15,  # temp_cool_ORCC
[800+273.15,  # temp_fuel_list
    800+273.15, 800+273.15, 800+273.15, 800+273.15,
    800+273.15, 800+273.15, 800+273.15,
 ],
# list of temperatures:central graphie kernel;
# fuel, buffer, iPyC, SiC,
# oPyC, matrix; shell
600+100*i,  # temp_cool_F
650+273.15,  # temp_blanket
600+100*i)  # temp_cool_B
f = open(dir_name+'/Fuel_unit_cell%d' % i, 'w+')
text = core.Fuel.unit_cell.generate_output()
print text
#    text = text.replace('gpb_pos.inp', 'gpb_pos%d.inp' % i)
#    text = text.replace('fpb_pos.inp', 'fpb_pos%d.inp' % i)
for fil in core.Fuel.filling:
	print fil.generate_output()
	text = text + fil.generate_output()
print list(core.Fuel.filling)[0] 
f.write(text)
f.close
#    shutil.copy('fpb_pos.inp', '%s/fpb_pos%d.inp' % (dir_name, i))
#    shutil.copy('gpb_pos.inp', '%s/gpb_pos%d.inp' % (dir_name, i))
f = open(dir_name+'/Fuel_lattice%d' % i, 'w+')
#    text = text.replace('gpb_pos.inp', 'gpb_pos%d.inp' % i)
#    text = text.replace('fpb_pos.inp', 'fpb_pos%d.inp' % i)
for fil in list(core.Fuel.filling)[0].filling:
	print fil.generate_output()
	text = text + fil.generate_output()
print list(core.Fuel.filling)[0].filling 

print core.Fuel.filling
f.write(text)
f.close
