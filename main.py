# from core_models.temp_fb import create_feedback_models

# folder = 'res/temp_coef/flibe/'
# gen_dir_name = folder
# create_feedback_models(gen_dir_name, 'flibe')
# folder = 'res/temp_coef/fuel/'
# gen_dir_name = folder
# create_feedback_models(gen_dir_name, 'fuel')
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

#folder = 'res/XS_gen_eq_500/'
#create_models(500, folder, fuel_type='eq')


from core_models.reference import create_the_model

gen_dir_name = 'res/reference_no_xe/'
create_the_model(gen_dir_name,
                hasRods=[False, False, False, False],
                fuel_type='eq',
                packing_fraction=0.60)
