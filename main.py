from core_models.ref_radialzones import create_the_model

folder = 'res/multi_zones/ref/'
gen_dir_name = folder + 'hasLinerSS31610mm/'
create_the_model(gen_dir_name,
                 hasRods=[False, False, False, False])
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

