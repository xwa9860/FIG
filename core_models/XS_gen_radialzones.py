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
    output_folder = 'res/multi_zones_short/'
    pb_burnups_w = np.array([1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8])
    pb_burnups_a = np.array([1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8])

    # sample fuel temperatures for each layer
    from util.sample_temperature import sample_temperature
    sample_nb = 50
    fuel_nb = 3 
    coating_nb = 5
    burnup_nb = len(list(unique_everseen(pb_burnups_w)))
    temps_mat = sample_temperature(burnup_nb, fuel_nb, coating_nb, sample_nb)
    np.save(output_folder+'temp_multiR_cr', temps_mat)


    # generating a set of input files for serpent
    # to generat cross sections for different temperatures
    # each of the 3 fuel layers in triso particles
    # each of the 4 or 8 burnups
    for case, temps in enumerate(temps_mat['sol']):
      # reset incremental parameters for a new serpent input
      Cell.id = 1
      Universe.id = 1
      Surface.id = 1
      FuelPbGen.wrote_surf = False

      tempsf = temps[:, 0:fuel_nb]
      tempst = temps[:, fuel_nb:fuel_nb+coating_nb]
      tempcool = temps_mat['liq'][case]

      output_dir_name = output_folder + 'input%d/' % case
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
