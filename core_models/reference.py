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
                     fuel_type='fresh',
                     temp_cool = 923.15,
                     temp_fuel = 1073.15,
                     packing_fraction=0.6):
  '''
  isOneFuel: boolean, if all fuel pebble unit cells have the same
             fuel compositions, otherwise multizones in the fuel region
  '''

  if isOneFuel: # all fuel pebble unit cells have the same fuel compositions
    if fuel_type == 'eq':
        burnups_w = np.array([1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8])
        burnups_a = np.array([1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8])
    else:
        burnups_w = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        burnups_a = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    burnup_nb = len(list(unique_everseen(burnups_w)))
    temps = np.ones((burnup_nb, 6))*temp_fuel
    fuel_nb = 1
    if isOneCoating:
      coating_nb = 1
    else:
      coating_nb = 5
    tempsf = temps[:, 0:fuel_nb]
    tempst = temps[:, fuel_nb:fuel_nb+coating_nb]

    if fuel_type == 'eq':
        fuel_comp_folder_w = config.FLUX_ALL_AVE_FOLDER
        fuel_comp_folder_a = config.FLUX_ALL_AVE_FOLDER
    else:
        fuel_comp_folder_w = config.FRESH_FOLDER
        fuel_comp_folder_a = config.FRESH_FOLDER
  else:  # fuel pebble unit cells are different between the center zones and the peripheral zones
    pb_burnups_w = np.array([1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8])
    pb_burnups_a = np.array([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4])
    fuel_comp_folder_w = config.FLUX_WALL_AVE_FOLDER
    fuel_comp_folder_a = config.FLUX_ACT_AVE_FOLDER

    fuel_nb = 1
    if isOneCoating:
      coating_nb = 1
    else:
      csoating_nb = 5
    temps_a = np.ones((4, 6))*temp_fuel
    temps_a_f = temps_a[:, 0:fuel_nb]
    temps_a_t = temps_a[:, fuel_nb:fuel_nb+coating_nb]
    temps_w = np.ones((8, 6))*temp_fuel
    temps_w_f = temps_w[:, 0:fuel_nb]
    temps_w_t = temps_w[:, fuel_nb:fuel_nb+coating_nb]

  # set the counters back to 0
  Cell.id = 1
  Universe.id = 1
  Surface.id = 1
  FuelPbGen.wrote_surf = False
  FCCGen.file_id = 0

  core = Core(
      (tempsf, tempst, temp_fuel, temp_fuel, 'w', burnups_w,  fuel_comp_folder_w),
      (tempsf, tempst, temp_fuel, temp_fuel, 'a1', burnups_a, fuel_comp_folder_a),
      (tempsf, tempst, temp_fuel, temp_fuel, 'a2', burnups_a, fuel_comp_folder_a),
      (tempsf, tempst, temp_fuel, temp_fuel, 'a3', burnups_a, fuel_comp_folder_a),
      (tempsf, tempst, temp_fuel, temp_fuel, 'a4', burnups_a, fuel_comp_folder_a),
      600+273.15,  # temp_CR
      600+273.15,  # temp_g_CRCC
      600+273.15,  # temp_cool_CRCC, has to be equal to temp_cool_F or temp_cool_B for now, O/W flibeMaterial will be missing
      600+273.15,  # temp_OR
      600+273.15,  # temp_g_ORCC
      600+273.15,  # temp_cool_ORCC
      temp_cool,  # temp_cool_F
      650+273.15,  # temp_blanket
      temp_cool,  # temp_cool_B
      600+273.15,  # temp_Corebarrel
      600+273.15,  # temp_Downcomer
      600+273.15,  # temp_vessel
      gen_dir_name,
      hasShield=hasShield,
      hasRods=hasRods,
      packing_fraction=packing_fraction)

  # write the model to the gen_dir_name
  mkdir(gen_dir_name)
  f = open(''.join([gen_dir_name, '/serp_full_core']), 'w+')
  text = core.generate_output()
  f.write(text)
  f.close

  # write a readme file in the folder
  rd = open(''.join([gen_dir_name, '/readme']), 'w+')
  text = []
  text.append('Has rods: %s\n' %str(hasRods))
  text.append('Packing fraction %f\n' % packing_fraction)
  text.append('Same fuel composition in multi fuel zones: %s\n' % str(isOneFuel))
  text.append('Combined triso coatings into one layer: %s\n' % str(isOneCoating))
  text.append('Coolant temperature %f\n' %temp_cool)
  text.append('Fuel temperature %f\n' %temp_fuel)
  text.append('Fuel type %s\n' %fuel_type)
  text.append('Has shield %s\n' %str(hasShield))

  rd.write(''.join(text))
  rd.close
