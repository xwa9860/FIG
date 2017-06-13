'''
This file is used to generate cross-sections

create core with two fuel zones

'''
#!/usr/bin/python
from FIG import triso
from FIG import core_2_zones
from FIG import pbed
from FIG import pb
from FIG import mat
from FIG.pb_gen import FuelPbGen
from FIG.serp_concept import Cell, Universe, Surface
from more_itertools import unique_everseen
from util.mkdir import mkdir
import shutil
import os
import numpy as np


def create_a_fuel_pebble(temp_list, name, burnup, pb_comp_dir, gen_dir_name):
    '''
    create a fuel pebble, assuming all the triso particles in the pebble have
    same temperature configurations(can have different temp in different triso 
    layers though)
    temp_list: a list that contains temperature for each triso
    layer in the pebble
    burnup: used to choose the fuel mat composition file in pb_comp_dir
    '''
    fuel_name1 = 'fuel1in%s' % name
    fuel_name2 = 'fuel2in%s' % name
    fuel_name3 = 'fuel3in%s' % name
    fuel_input = '%s/fuel_mat%d' % (pb_comp_dir, burnup)
    fuel1 = mat.Fuel(temp_list[1], fuel_name1, fuel_input, tmp_card=None)
    fuel2 = mat.Fuel(temp_list[2], fuel_name2, fuel_input, tmp_card=None)
    fuel3 = mat.Fuel(temp_list[3], fuel_name3, fuel_input, tmp_card=None)
    tr = triso.Triso(temp_list[4:9], 
                     [fuel1, fuel2, fuel3], 
                     dr_config=None,
                     dir_name=gen_dir_name)
    return pb.FPb(tr, temp_list[0], temp_list[9], dir_name=gen_dir_name)

def create_a_pb_unit_cell(fuel_temps, uc_name, burnups, pb_comp_dir, gen_dir_name):
    '''
    fuel_temps: temperature list for pebbles in the unit cell
    a matrix of 14 pebbles x 10 layers
    '''
    fpb_list = []
    unique_fpb_list = []
    unique_burnups = list(unique_everseen(burnups))
    for i in range(len(unique_burnups)):
        pb_name = 'pb%s%d' % (uc_name, i)
        unique_fpb_list.append(
            create_a_fuel_pebble(fuel_temps[i], 
                                 pb_name,
                                 unique_burnups[i], pb_comp_dir, gen_dir_name))
    for i in range(len(burnups)):
        fpb_list.append(unique_fpb_list[burnups[i]-1])
    return fpb_list


def create_the_core(fuel_temps_w, fuel_temps_a, burnups_w, burnups_a, pb_comp_dir_w, pb_comp_dir_a, gen_dir_name):
    '''
    fuel_temps_w: a list of temperatures used to define fuel pebbles in the near-wall region
    '''

    fpb_list_w = create_a_pb_unit_cell(fuel_temps_w, 'w', burnups_w, pb_comp_dir_w, gen_dir_name)
    fpb_list_a = create_a_pb_unit_cell(fuel_temps_a, 'a', burnups_a, pb_comp_dir_a, gen_dir_name)

    core = core_2_zones.Core(
        fpb_list_w,
        fpb_list_a,
        1000,  # temp_CR
        1000,  # temp_g_CRCC
        1000,  # temp_cool_CRCC
        1000,  # temp_OR
        1000,  # temp_g_ORCC
        1000,  # temp_cool_ORCC
        950,  # temp_cool_F
        1000,  # temp_blanket
        950,  # temp_cool_B
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
    pb_burnups_w = np.array([1, 1, 1, 1, 5, 5, 5, 5, 2, 6, 3, 7, 4, 8])
    pb_burnups_a = np.array([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4])

    from util.sample_temperature import sampling_temp
    temps_a_mat = sampling_temp(4, 4, 3)
    temps_w_mat = sampling_temp(8, 4, 3)

    # generating a set of input files for serpent
    # to generat cross sections for different temperatures
    # each of the 3 fuel layers in triso particles
    # each of the 4 or 8 burnups
    for case, temps_a in enumerate(temps_a_mat):
          # parse temeprature list from a 12x1 or 24x1 vector to a matrix to be used in function create_the_core
          temps_w = temps_w_mat[case] 
          # reset incremental parameters for a new serpent input
          Cell.id = 1
          Universe.id = 1
          Surface.id = 1
          FuelPbGen.wrote_surf = False

          #pb_idxs = np.where(pb_burnups_w == j)[0]
          #print(pb_idxs)
          #for pb_idx in pb_idxs:
              #fuel_temp_list[pb_idx] = temp*np.ones(8)
              # list of temperatures:central graphie kernel;
              # fuel, buffer, iPyC, SiC,
              # oPyC, matrix;
              # shell
          output_dir_name = 'mk1_input/input%d/' %(case)
          fuel_comp_folder_w = 'fuel_mat/fuel_comp/flux_wall_ave_serp/'
          fuel_comp_folder_a = 'fuel_mat/fuel_comp/flux_act_ave_serp/'

          create_the_core(temps_w,
                          temps_a,
                          pb_burnups_w,
                          pb_burnups_a,
                          fuel_comp_folder_w,
                          fuel_comp_folder_a,
                          output_dir_name)
