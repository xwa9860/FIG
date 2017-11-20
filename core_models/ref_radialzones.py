'''
This file is used to assemble the core from input file that contains model specifications
in main.py

'''
#!/usr/bin/python
from FIG.core import Core
from FIG.pb_gen import FuelPbGen
from FIG.pbed_gen import FCCGen
from FIG.serp_concept import Cell, Universe, Detector, Surface
from util.mkdir import mkdir
import config
import shutil
import numpy as np


def create_the_model(gen_dir_name,
                     isOneFuel=True,
                     isOneCoating=False,
                     hasRods=[False, False, False, False],
                     hasShield=False):

    if isOneFuel: # all fuel pebble unit cells have the same fuel compositions
      burnups_w = np.array([1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8])
      burnups_a = np.array([1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8])

      temps = np.ones((8, 6))*1000
      fuel_nb = 1
      if isOneCoating:
        coating_nb = 1
      else:
        coating_nb = 5
      tempsf = temps[:, 0:fuel_nb]
      tempst = temps[:, fuel_nb:fuel_nb+coating_nb]
      tempcool = 950# 950 nominal

      fuel_comp_folder_w = config.FLUX_ALL_AVE_FOLDER
      fuel_comp_folder_a = config.FLUX_ALL_AVE_FOLDER
    else:  # fuel pebble unit cells are different between the center zones and the peripheral zones
      pb_burnups_w = np.array([1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8])
      pb_burnups_a = np.array([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4])
      fuel_comp_folder_w = config.FLUX_WALL_AVE_FOLDER
      fuel_comp_folder_a = config.FLUX_ACT_AVE_FOLDER

      fuel_nb = 1
      if isOneCoating:
        coating_nb = 1
      else:
        coating_nb = 5
      temps_a = np.ones((4, 6))*1000
      temps_a_f = temps_a[:, 0:fuel_nb]
      temps_a_t = temps_a[:, fuel_nb:fuel_nb+coating_nb]
      temps_w = np.ones((8, 6))*1000
      temps_w_f = temps_w[:, 0:fuel_nb]
      temps_w_t = temps_w[:, fuel_nb:fuel_nb+coating_nb]
      tempcool = 950# 950 nominal

    # set the counters back to 0
    Cell.id = 1
    Universe.id = 1
    Surface.id = 1
    FuelPbGen.wrote_surf = False
    FCCGen.file_id = 0

    core = Core(
        (tempsf, tempst, 900, 900, 'w', burnups_w,  fuel_comp_folder_w),
        (tempsf, tempst, 900, 900, 'a1', burnups_a, fuel_comp_folder_a),
        (tempsf, tempst, 900, 900, 'a2', burnups_a, fuel_comp_folder_a),
        (tempsf, tempst, 900, 900, 'a3', burnups_a, fuel_comp_folder_a),
        (tempsf, tempst, 900, 900, 'a4', burnups_a, fuel_comp_folder_a),
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
        gen_dir_name,
        hasShield=hasShield,
        hasRods=hasRods)

    # write the model to the gen_dir_name
    mkdir(gen_dir_name)
    f = open(''.join([gen_dir_name, '/serp_full_core']), 'w+')
    text = core.generate_output()
    f.write(text)
    f.close
