'''
This file is used to generate cross-sections
'''

#!/usr/bin/python
from FIG.core import Core
from FIG.pb_gen import FuelPbGen
from FIG.pbed_gen import FCCGen
from FIG.serp_concept import Cell, Universe, Surface
from util.mkdir import mkdir
import config
import shutil
import numpy as np
from more_itertools import unique_everseen


def create_models(sample_nb,
                  gen_dir_name, hasRods=[False, False, False, False],
                  fuel_type='eq', hasShield=False, packing_fraction=0.6):
    '''
    create a number of models with sampled temperatures to fit a cross section model
    sample_nb: number of models(data samples)
    '''
    isOneFuel = True
    isOneCoating = False

    if fuel_type == 'eq':
      fuel_comp_folder_w = config.FLUX_ALL_AVE_FOLDER
      fuel_comp_folder_a = config.FLUX_ALL_AVE_FOLDER
      burnups_w = np.array([1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8])
      burnups_a = np.array([1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8])
    else:
      fuel_comp_folder_w = config.FRESH_FOLDER
      fuel_comp_folder_a = config.FRESH_FOLDER
      burnups_w = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
      burnups_a = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    # sample fuel temperatures for each layer
    from util.sample_temperature import sample_temperature
    fuel_nb = 3 
    coating_nb = 5
    burnup_nb = len(list(unique_everseen(burnups_w)))
    temps_mat = sample_temperature(burnup_nb, fuel_nb, coating_nb, sample_nb)
    mkdir(gen_dir_name)
    np.save(gen_dir_name+'temp_mat', temps_mat)

    # generating a set of input files for serpent
    # to generat cross sections for different temperatures
    # each of the 3 fuel layers in triso particles
    # each of the 4 or 8 burnups
    for case, temps in enumerate(temps_mat['sol']):
      # set the counters for incremental parameters back to 0
      Cell.id = 1
      Universe.id = 1
      Surface.id = 1
      FuelPbGen.wrote_surf = False
      FCCGen.file_id = 0

      tempsf = temps[:, 0:fuel_nb]
      tempst = np.ones((burnup_nb, coating_nb)) * 900
      
      # tempst = temps[:, fuel_nb:fuel_nb+coating_nb]
      temp_cool = temps_mat['liq'][case]

      output_dir_name = gen_dir_name + 'input%d/' % case

      core = Core(
          (tempsf, tempst, 900, 900, 'w', burnups_w,  fuel_comp_folder_w),
          (tempsf, tempst, 900, 900, 'a1', burnups_a, fuel_comp_folder_a),
          (tempsf, tempst, 900, 900, 'a2', burnups_a, fuel_comp_folder_a),
          (tempsf, tempst, 900, 900, 'a3', burnups_a, fuel_comp_folder_a),
          (tempsf, tempst, 900, 900, 'a4', burnups_a, fuel_comp_folder_a),
          600+273.15,  # temp_CR
          600+273.15,  # temp_g_CRCC
          600+273.15,  # temp_cool_CRCC, has to be equal to temp_cool_F or temp_cool_B for now, O/W flibeMaterial will be missing
          600+273.15,  # temp_OR
          600+273.15,  # temp_g_ORCC
          600+273.15,  # temp_cool_ORCC
          temp_cool,  # temp_cool_F
          650+273.15,  # temp_blanket
          650+273.15,  # temp_cool_B
          600+273.15,  # temp_Corebarrel
          600+273.15,  # temp_Downcomer
          600+273.15,  # temp_vessel
          output_dir_name,
          hasShield=hasShield,
          hasRods=hasRods,
          packing_fraction=packing_fraction,
          purpose='XS_gen')
    
      # write the model down
      mkdir(output_dir_name)
      f = open(''.join([output_dir_name, '/serp_full_core']), 'w+')
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
    # text.append('Coolant temperature %f\n' %temp_cool)
    # text.append('Fuel temperature %f\n' %temp_fuel)
    text.append('Fuel type %s\n' %fuel_type)
    text.append('Has shield %s\n' %str(hasShield))

    rd.write(''.join(text))
    rd.close
