from core_models.reference import create_the_model
import numpy as np


def create_feedback_models(gen_dir_name, flag):
    if flag == 'flibe':
        densities =np.array([1700, 1800, 1900, 2000, 2100])
        temps = (2413-densities)/0.488
        for temp in temps:
            create_the_model(''.join([gen_dir_name, '/', str(int(temp)), '/']), temp_cool=temp)

    elif flag == 'fuel':
        temps = [300, 600, 900, 1200, 1500]
        for temp in temps:
            create_the_model(''.join([gen_dir_name, '/', str(int(temp)), '/']), temp_fuel=temp)


