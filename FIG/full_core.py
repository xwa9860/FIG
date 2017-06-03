#!/usr/bin/python
import triso
import core_2_zones
import pbed
import pb
import mat
from pb_gen import FuelPbGen
import shutil
import os
import numpy as np
from serp_concept import Cell, Universe, Surface
from more_itertools import unique_everseen


def mkdir(path):
    '''create a new directory and check  if not exsit,
    so it will not overwrite existing folders'''
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


def create_a_fuel_pebble(temp_list, name, burnup, pb_comp_dir, gen_dir_name):
    '''
    temp_list: a list that contains temperature for each triso
    layer in the pebble
    burnup: used to choose the fuel mat composition
    '''
    fuel_name = 'fuel%d' % burnup
    fuel_input = '%s/fuel_mat%d' % (pb_comp_dir, burnup)
    fuel = mat.Fuel(temp_list[1], fuel_name, fuel_input, tmp_card=None)
    tr = triso.Triso(temp_list[2:7], fuel, dr_config=None,
                     dir_name=gen_dir_name)
    return pb.FPb(tr, temp_list[0], temp_list[7], dir_name=gen_dir_name)

def create_a_pb_unit_cell(fuel_temps, burnups, pb_comp_dir, gen_dir_name):
    fpb_list = []
    unique_fpb_list = []
    unique_burnups = list(unique_everseen(burnups))
    for i in range(len(unique_burnups)):
        name = 'fuelpb%d' % i
        unique_fpb_list.append(
            create_a_fuel_pebble(fuel_temps[i], name,
                                 unique_burnups[i], pb_comp_dir, gen_dir_name))
    for i in range(len(burnups)):
        fpb_list.append(unique_fpb_list[burnups[i]-1])
    return fpb_list


def create_the_core(fuel_temps, burnups1, burnups2, pb_comp_dir1, pb_comp_dir2, gen_dir_name):

    fpb_list1 = create_a_pb_unit_cell(fuel_temps, burnups1, pb_comp_dir1, gen_dir_name)
    fpb_list2 = create_a_pb_unit_cell(fuel_temps, burnups2, pb_comp_dir2, gen_dir_name)

    core = core_2_zones.Core(
        fpb_list1,
        fpb_list2,
        900,  # temp_CR
        900,  # temp_g_CRCC
        900,  # temp_cool_CRCC
        900,  # temp_OR
        900,  # temp_g_ORCC
        900,  # temp_cool_ORCC
        900,  # temp_cool_F
        900,  # temp_blanket
        900,  # temp_cool_B
        900,  # temp_Corebarrel
        900,  # temp_Downcomer
        900,  # temp_vessel
        gen_dir_name)
    mkdir(gen_dir_name)
    f = open(''.join([gen_dir_name, '/serp_full_core']), 'w+')
    text = core.generate_output()
    f.write(text)
    f.close

if __name__ == "__main__":
    pb_burnups1 = np.array([1, 1, 1, 1, 5, 5, 5, 5, 2, 6, 3, 7, 4, 8])
    pb_burnups2 = np.array([1, 1, 1, 1, 5, 5, 5, 5, 2, 6, 3, 7, 4, 8])

    fuel_temp_list = [900*np.ones(8) for i in range(14)]

    case_nb = 1
    for temp in np.array([300, 600, 900]):
        for j in range(1, 9):
            # reset
            Cell.id = 1
            Universe.id = 1
            Surface.id = 1
            FuelPbGen.wrote_surf = False
            pb_idxs = np.where(pb_burnups1 == j)[0]
            #for pb_idx in pb_idxs:
                #fuel_temp_list[pb_idx] = temp*np.ones(8)
                # list of temperatures:central graphie kernel;
                # fuel, buffer, iPyC, SiC,
                # oPyC, matrix;
                # shell
            output_dir_name = 'mk1_input/%d_%d/' %(j, temp)
            fuel_comp_folder1 = 'fuel_mat/fuel_comp/flux_ave_serp/'
            fuel_comp_folder2 = 'fuel_mat/fuel_comp/flux_ave_serp/'
            create_the_core(fuel_temp_list, pb_burnups1, pb_burnups2,
                fuel_comp_folder1,
                fuel_comp_folder2,
                output_dir_name)
            case_nb += 1
