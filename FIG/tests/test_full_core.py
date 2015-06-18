#!/usr/bin/python
import core_w_channel, triso, pbed, pb, mat
import shutil
import os

def mkdir(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


def create_fuel_pebbles(fuel_temp_list):
    pb_burnup_list = [1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8]
    #pb_burnup_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1 ,1]
    fpb_list = []
    for i in xrange(0, 14):
        fuel_name = 'fuel%d' % i
        fuel_input = '../fuel_mat/vol_ave_mcnp/fuel_mat%d' %pb_burnup_list[i]
        fuel = mat.Fuel(fuel_temp_list[1], fuel_name, fuel_input)
        # range in python: list[2:7] means list[2,3,4,5,6]
        tr = triso.Triso(fuel_temp_list[2:7], fuel)
        fpb_list.append(pb.FPb(tr, fuel_temp_list[0], fuel_temp_list[7]))
    return fpb_list


# list of temperatures:central graphie kernel;
# fuel, buffer, iPyC, SiC,
# oPyC, matrix; shell
fuel_temp_list= [800+273.15,  # temp_fuel_list
        800+273.15, 800+273.15, 800+273.15, 800+273.15,
        800+273.15, 800+273.15,
        800+273.15]
fpb_list = create_fuel_pebbles(fuel_temp_list)
core = core_w_channel.Core(
    fpb_list,
    650+273.15,  # temp_CR
    650+273.15,  # temp_g_CRCC
    650+273.15,  # temp_cool_CRCC
    650+273.15,  # temp_OR
    650+273.15,  # temp_g_ORCC
    650+273.15,  # temp_cool_ORCC
    650+273.15,  # temp_cool_F
    650+273.15,  # temp_blanket
    650+273.15)  # temp_cool_B
f = open('test_full_core_res', 'w+')
text = core.generate_output()
f.write(text)
f.close
