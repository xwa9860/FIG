'''
This file is used to generate cross-sections

create core with two fuel zones

'''
#!/usr/bin/python
from FIG import triso
from FIG.core import Core
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
                    fuel_temps_a,
                    triso_temps_a,
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
    fpb_list_a = create_a_pb_unit_cell(fuel_temps_a, triso_temps_a, 900, 900, 'a', burnups_a, pb_comp_dir_a, gen_dir_name)

    core = Core(
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

    from util.sample_temperature import sample_temperature
    #temps_w_mat = sample_temperature(pb_burnups_w, 4, 10)
    sample_nb_a = 100
    fuel_nb_a = 3 
    coating_nb_a = 5 
    burnup_nb_a = len(list(unique_everseen(pb_burnups_a)))
    temps_a_mat = sample_temperature(burnup_nb_a, fuel_nb_a, coating_nb_a, sample_nb_a)
    np.save('temp', temps_a_mat)

    # generating a set of input files for serpent
    # to generat cross sections for different temperatures
    # each of the 3 fuel layers in triso particles
    # each of the 4 or 8 burnups
    for case, temps_a in enumerate(temps_a_mat):
          # reset incremental parameters for a new serpent input
          Cell.id = 1
          Universe.id = 1
          Surface.id = 1
          FuelPbGen.wrote_surf = False

          temps_a_f = temps_a[:, 0:fuel_nb_a]
          temps_a_t = temps_a[:, fuel_nb_a:fuel_nb_a+coating_nb_a]#.reshape(4,1)

          #temps_a_f = np.ones((burnup_nb_a, fuel_nb_a))*900
          #temps_a_t = np.ones((burnup_nb_a, coating_nb_a))*900
          temps_w_f = np.ones((8, 1))*900
          temps_w_t = np.ones((8, 5))*900

          output_dir_name = 'res/mk1_input/input%d/' %(case)
          fuel_comp_folder_w = config.FLUX_WALL_AVE_FOLDER
          fuel_comp_folder_a = config.FLUX_ACT_AVE_FOLDER

          create_the_core(temps_w_f, 
                          temps_w_t,
                          temps_a_f,
                          temps_a_t,
                          pb_burnups_w,
                          pb_burnups_a,
                          fuel_comp_folder_w,
                          fuel_comp_folder_a,
                          output_dir_name)
