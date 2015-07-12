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
    fpb_list = [] #list of different pebbles, 8 in this design
    fpb_list_all=[] #list of 14 pebbles
    for i in xrange(0, 8):
        fuel_name = 'fuel%d' %i
        fuel_input = '../fuel_mat/vol_ave_mcnp/fuel_mat%d' %pb_burnup_list[i]
        fuel = mat.Fuel(fuel_temp_list[1], fuel_name, fuel_input, tmp_card=None)
        # range in python: list[2:7] means list[2,3,4,5,6]
        tr = triso.Triso(fuel_temp_list[2:7], fuel)
        fpb_list.append(pb.FPb(tr, fuel_temp_list[0], fuel_temp_list[7]))
    for i in xrange(0, 14):
        fpb_list_all.append(fpb_list[pb_burnup_list[i]-1])
    return fpb_list_all


# list of temperatures:central graphie kernel;
# fuel, buffer, iPyC, SiC,
# oPyC, matrix; shell
fuel_temp_list= [900,  # temp_fuel_list
        1200, 1200, 1200, 1200,
        1200, 1200,
        1200]
fpb_list = create_fuel_pebbles(fuel_temp_list)

core = core_w_channel.Core(
    fpb_list,
    1200,  # temp_CR
    1200,  # temp_g_CRCC
    1200,  # temp_cool_CRCC
    1200,  # temp_OR
    1200,  # temp_g_ORCC
    1200,  # temp_cool_ORCC
    1200,  # temp_cool_F
    1200,  # temp_blanket
    1200)  # temp_cool_B
f = open('serp_input/test_full_core_res', 'w+')
text = core.generate_output()
f.write(text)
f.close
