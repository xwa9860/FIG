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
from more_itertools import unique_everseen


def create_the_model(gen_dir_name,
                     isOneFuel=True,
                     isOneCoating=False,
                     hasRods=[False, False, False, False],
                     hasShield=False,
                     fuelType='eq'):
  '''
  isOneFuel: boolean, if all fuel pebble unit cells have the same
             fuel compositions, otherwise multizones in the fuel region
  '''

  fuel_temp = 800 + 273.15 # nominal 800 degC
  tempcool = 650 + 273.15 #nominal 650 degC

  if isOneFuel: # all fuel pebble unit cells have the same fuel compositions
    burnups_w = np.array([1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8])
    burnups_a = np.array([1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8])
    #burnups_w = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    #burnups_a = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    burnup_nb = len(list(unique_everseen(burnups_w)))
    temps = np.ones((burnup_nb, 6))*fuel_temp
    fuel_nb = 1
    if isOneCoating:
      coating_nb = 1
    else:
      coating_nb = 5
    tempsf = temps[:, 0:fuel_nb]
    tempst = temps[:, fuel_nb:fuel_nb+coating_nb]

    fuel_comp_folder_w = config.FRESH_FOLDER
    fuel_comp_folder_a = config.FRESH_FOLDER
    #fuel_comp_folder_w = config.FLUX_ALL_AVE_FOLDER
    #fuel_comp_folder_a = config.FLUX_ALL_AVE_FOLDER
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
    temps_a = np.ones((4, 6))*fuel_temp
    temps_a_f = temps_a[:, 0:fuel_nb]
    temps_a_t = temps_a[:, fuel_nb:fuel_nb+coating_nb]
    temps_w = np.ones((8, 6))*fuel_temp
    temps_w_f = temps_w[:, 0:fuel_nb]
    temps_w_t = temps_w[:, fuel_nb:fuel_nb+coating_nb]

  # set the counters back to 0
  Cell.id = 1
  Universe.id = 1
  Surface.id = 1
  FuelPbGen.wrote_surf = False
  FCCGen.file_id = 0

  core = Core(
      (tempsf, tempst, fuel_temp, fuel_temp, 'w', burnups_w,  fuel_comp_folder_w),
      (tempsf, tempst, fuel_temp, fuel_temp, 'a1', burnups_a, fuel_comp_folder_a),
      (tempsf, tempst, fuel_temp, fuel_temp, 'a2', burnups_a, fuel_comp_folder_a),
      (tempsf, tempst, fuel_temp, fuel_temp, 'a3', burnups_a, fuel_comp_folder_a),
      (tempsf, tempst, fuel_temp, fuel_temp, 'a4', burnups_a, fuel_comp_folder_a),
      600+273.15,  # temp_CR
      600+273.15,  # temp_g_CRCC
      600+273.15,  # temp_cool_CRCC, has to be equal to temp_cool_F or temp_cool_B for now, O/W flibeMaterial will be missing
      600+273.15,  # temp_OR
      600+273.15,  # temp_g_ORCC
      600+273.15,  # temp_cool_ORCC
      tempcool,  # temp_cool_F
      650+273.15,  # temp_blanket
      tempcool,  # temp_cool_B
      600+273.15,  # temp_Corebarrel
      600+273.15,  # temp_Downcomer
      600+273.15,  # temp_vessel
      gen_dir_name,
      hasShield=hasShield,
      hasRods=hasRods)

  # write the model to the gen_dir_name
  mkdir(gen_dir_name)
  f = open(''.join([gen_dir_name, '/serp_full_core']), 'w+')
  text = core.generate_output()
  f.write(text)
  f.close
