from core_models.temp_fb import create_feedback_models

folder = 'res/temp_coef/flibe/'
gen_dir_name = folder
create_feedback_models(gen_dir_name, 'flibe')
folder = 'res/temp_coef/fuel/'
gen_dir_name = folder
create_feedback_models(gen_dir_name, 'fuel')
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

# from core_models.XS_gen import create_models

# folder = 'res/XS_gen_100/'
# create_models(100, folder)


# from core_models.reference import create_the_model

# gen_dir_name = 'res/packing_fraction/62/'
# gen_dir_name = 'res/reference/'
# create_the_model(gen_dir_name,
#                 hasRods=[False, False, False, False],
#                 packing_fraction=0.62)
