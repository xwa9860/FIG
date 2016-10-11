#!/usr/bin/python
import triso
import core_w_channel
import pbed
import pb
import mat
import shutil
import os


def mkdir(path):
    '''create a new directory and check  if not exsit,
    so it will not overwrite existing folders'''
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


def create_fuel_pebbles(fuel_temp_list):
    pb_burnup_list = [1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8]
    # pb_burnup_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1 ,1]
    fpb_list = []  # list of different pebbles, 8 in this design
    fpb_list_all = []  # list of 14 pebbles
    for i in range(0, 8):
        fuel_name = 'fuel%d' % i
        fuel_input = 'fuel_mat/vol_ave/fuel_mat%d' % (i+1)
        fuel = mat.Fuel(fuel_temp_list[1], fuel_name, fuel_input, tmp_card=None)
        # range in python: list[2:7] means list[2,3,4,5,6]
        tr = triso.Triso(fuel_temp_list[2:7], fuel)
        fpb_list.append(pb.FPb(tr, fuel_temp_list[0], fuel_temp_list[7]))
    for i in range(0, 14):
        fpb_list_all.append(fpb_list[pb_burnup_list[i]-1])
    return fpb_list_all


# list of temperatures:central graphie kernel;
# fuel, buffer, iPyC, SiC,
# oPyC, matrix; shell
fuel_temp_list = [900,  # temp_fuel_list
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
mkdir('serp_input')
f = open('serp_input/serp_full_core', 'w+')
text = core.generate_output()
f.write(text)
f.close
