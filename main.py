from core_models.ref_radialzones import create_the_model
#from core_models.XS_gen import create_models

folder = 'res/multi_zones/'
gen_dir_name = folder + 'ref_eq_norod/'
create_the_model(gen_dir_name,
                 hasRods=[False, False, False, False])
#gen_dir_name = folder + 'packing_fraction_no_rods/pf_40/'
#create_the_model(gen_dir_name,
#                 hasRods=[False, False, False, False])
#
#gen_dir_name = 'res/multi_zones/ref/rods_272/'
#create_the_model(gen_dir_name,
#                 hasRods=[True, True, False, False])
#
#gen_dir_name = 'res/multi_zones/ref/rods_430/'
#create_the_model(gen_dir_name,
#                 hasRods=[True, False, False, False])
#
#gen_dir_name = 'res/multi_zones/temp_fb_no_rod/fuel_1500/'
#create_the_model(gen_dir_name,
#                 hasRods=[True, True, False, False])

#from core_models.XS_gen import create_models
#
#folder = 'res/multi_zones/XS_gen/'
#create_models(folder)

