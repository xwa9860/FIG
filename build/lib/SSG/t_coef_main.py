#!/usr/bin/python
# from core_simple import Core
from core_w_channel import Core
import shutil
import os


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


# To calculate the t_coef of coolant
for i in range(0, 5):
    dir_name = '../react_coef/fuel_v3'
    mkdir(dir_name)
    core = Core(
        650+273.15,  # temp_CR
        650+273.15,  # temp_g_CRCC
        650+273.15,  # temp_cool_CRCC
        650+273.15,  # temp_OR
        650+273.15,  # temp_g_ORCC
        650+273.15,  # temp_cool_ORCC
        [800+273.15,  # temp_fuel_list
            800+273.15-100+i*50, 800+273.15, 800+273.15, 800+273.15,
            800+273.15, 800+273.15, 
            800+273.15,
         ],
        # list of temperatures:central graphie kernel;
        # fuel, buffer, iPyC, SiC,
        # oPyC, matrix; shell
        600,  # temp_cool_F
        650+273.15,  # temp_blanket
        600)  # temp_cool_B
    f = open(dir_name+'/serp_fuel_%d' % i, 'w+')
    text = core.generate_output()
    text = text.replace('gpb_pos.inp', 'gpb_pos%d.inp' % i)
    text = text.replace('fpb_pos.inp', 'fpb_pos%d.inp' % i)
    f.write(text)
    f.close
    shutil.copy('fpb_pos.inp', '%s/fpb_pos%d.inp' % (dir_name, i))
    shutil.copy('gpb_pos.inp', '%s/gpb_pos%d.inp' % (dir_name, i))

