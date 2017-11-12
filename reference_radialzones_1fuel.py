'''
This file is used to generate cross-sections

create core with two fuel zones
and control rods

'''
#!/usr/bin/python
from FIG import triso
from FIG.core_rods_multiR import Core
from FIG import pbed
from FIG import pb
from FIG import mat
from FIG.pb_gen import FuelPbGen
from FIG.serp_concept import Cell, Universe, Surface
from more_itertools import unique_everseen
from util.mkdir import mkdir
import config
import shutil
import numpy as np


def create_a_fuel_pebble(fuel_temps, coating_temps, cgt, sht, pbname, burnup, pb_comp_dir, gen_dir_name):
    '''
    create a fuel pebble, assuming all the triso particles in the pebble have the
    same temperature configurations(can have different temp in different triso
    layers though)
    fuel_temps: a list that contains temperature for each fuel
    layer in the triso, 1d array of length 1 or 3
    coating_temps: a list that contains temp for each of the non-fuel layers in triso
    cgt: central graphite temperature
    sht: shell temperature
    burnup: used to choose the fuel mat composition file in pb_comp_dir
    '''
    assert fuel_temps.shape == (1,) or fuel_temps.shape == (3,), 'wrong fuel temp shape:%r' %(fuel_temps.shape)
    assert coating_temps.shape == (1,) or coating_temps.shape == (5,), 'wrong coating temp shape:%r' %(fuel_temps.shape)

    # create fuel materials
    fuels = []
    for i, temp in enumerate(fuel_temps):
        fuel_name = 'fuel%d%s' % (i+1, pbname)
        fuel_input = '%s/fuel_mat%d' % (pb_comp_dir, burnup)
        fuels.append(mat.Fuel(temp, fuel_name, fuel_input))
    
    # create triso particle
    if coating_temps.shape == (1,):
        tr = triso.Triso(coating_temps,
                         fuels, 
                         dr_config='homogenized',
                         dir_name=gen_dir_name)
    else:
        tr = triso.Triso(coating_temps,
                         fuels, 
                         dr_config=None,
                         dir_name=gen_dir_name)
    return pb.FPb(tr, cgt, sht, dir_name=gen_dir_name)


def create_a_pb_unit_cell(fuel_temps, coating_temps, cgt, sht, uc_name, burnups, pb_comp_dir, gen_dir_name):
    '''
    fuel_temps: temperature list for unique pebbles in the unit cell
    a matrix of unique pebbles x n layers of fuel in a triso
    coating_temps: a list that contains temp for each of the non-fuel layers in triso, e.g. 4x5
    cgt: central graphite temperature
    sht: shell temperature
    '''
    fpb_list = []
    unique_fpb_list = {}
    unique_burnups = list(unique_everseen(burnups))

    unique_burnup_nb = len(unique_burnups)
    assert fuel_temps.shape[0] == unique_burnup_nb, 'wrong dimension %s' %str(fuel_temps.shape)
    assert coating_temps.shape[0] == unique_burnup_nb, 'wrong dimension' 
    # create a list of unique pebbles
    for i, bu in enumerate(unique_burnups):
        pb_name = 'pb%s%d' % (uc_name, bu)
        unique_fpb_list[bu] = create_a_fuel_pebble(fuel_temps[bu-1, :], 
                                                   coating_temps[unique_burnups[i]-1, :],
                                                   cgt, sht,
                                                   pb_name,
                                                   unique_burnups[i], 
                                                   pb_comp_dir, 
                                                   gen_dir_name)
    # create a list of all the 14 fuel pebbles, some of them are exactly the same
    for bu in burnups:
        fpb_list.append(unique_fpb_list[bu])
    return fpb_list


def create_the_core(fuel_temps_w,
                    triso_temps_w,
                    fuel_temps_a1,
                    triso_temps_a1,
                    fuel_temps_a2,
                    triso_temps_a2,
                    fuel_temps_a3,
                    triso_temps_a3,
                    fuel_temps_a4,
                    triso_temps_a4,
                    burnups_w,
                    burnups_a,
                    pb_comp_dir_w,
                    pb_comp_dir_a,
                    gen_dir_name):
    '''
    fuel_temps_w: a list of temperatures used to define fuel layers in the near-wall region
    triso_temps_w: a list of temperatures used to define  layers in the near-wall region
    '''

    fpb_list_w = create_a_pb_unit_cell(fuel_temps_w, triso_temps_w, 900, 900, 'w', burnups_w, pb_comp_dir_w, gen_dir_name)
    fpb_list_a1 = create_a_pb_unit_cell(fuel_temps_a1, triso_temps_a1, 900, 900, 'a1', burnups_a, pb_comp_dir_a, gen_dir_name)
    fpb_list_a2 = create_a_pb_unit_cell(fuel_temps_a2, triso_temps_a2, 900, 900, 'a2', burnups_a, pb_comp_dir_a, gen_dir_name)
    fpb_list_a3 = create_a_pb_unit_cell(fuel_temps_a3, triso_temps_a3, 900, 900, 'a3', burnups_a, pb_comp_dir_a, gen_dir_name)
    fpb_list_a4 = create_a_pb_unit_cell(fuel_temps_a4, triso_temps_a4, 900, 900, 'a4', burnups_a, pb_comp_dir_a, gen_dir_name)

    core = Core(
        fpb_list_w,
        fpb_list_a1,
        fpb_list_a2,
        fpb_list_a3,
        fpb_list_a4,
        1000,  # temp_CR
        1000,  # temp_g_CRCC
        1000,  # temp_cool_CRCC, has to be equal to temp_cool_F or temp_cool_B for now, O/W flibeMaterial will be missing
        1000,  # temp_OR
        1000,  # temp_g_ORCC
        1000,  # temp_cool_ORCC
        1000,  # temp_cool_F
        1000,  # temp_blanket
        1000,  # temp_cool_B
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
    output_folder = 'res/multi_zone_ref/'
    pb_burnups_w = np.array([1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8])
    pb_burnups_a = np.array([1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8])

    temps = np.ones((8, 6))*1000
    fuel_nb = 1
    coating_nb = 5
    tempsf = temps[:, 0:fuel_nb]
    tempst = temps[:, fuel_nb:fuel_nb+coating_nb]
    tempcool = 950# 950 nominal

    output_dir_name = output_folder + 'cr_all_up/gr_rods/'
    fuel_comp_folder_w = config.FLUX_ALL_AVE_FOLDER
    fuel_comp_folder_a = config.FLUX_ALL_AVE_FOLDER

    # assuming all the layers have the same temperature
    create_the_core(tempsf, 
                    tempst,
                    tempsf,
                    tempst,
                    tempsf,
                    tempst,
                    tempsf,
                    tempst,
                    tempsf,
                    tempst,
                    pb_burnups_w,
                    pb_burnups_a,
                    fuel_comp_folder_w,
                    fuel_comp_folder_a,
                    output_dir_name)
