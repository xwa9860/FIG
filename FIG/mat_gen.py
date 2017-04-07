#!/usr/bin/python
# assume mat density defined as mass density g/cm3
import bisect

# temp available in the gre7 thermal scattering lib for graphite
# http://montecarlo.vtt.fi/download/SSS_THERMAL.pdf
temp_list = [700, 800, 1000, 1200, 1600, 2000]
id_list = [16, 18, 20, 22, 24, 26]


class MatGen:

    def parse(self, a_mat, type, tmp):
        if type == 's':
            str_list = []
            if a_mat.flag == 'moder':
                if tmp:
                    str_list.append(
                        '\nmat %s -%E moder grph_%s 6000 tmp %f\n %s' %
                        (a_mat.name, a_mat.density, a_mat.name,
                         a_mat.temp, a_mat.mat_comp))
                else:
                    str_list.append(
                        '\nmat %s -%E moder grph_%s 6000\n %s' %
                        (a_mat.name, a_mat.density, a_mat.name,
                         a_mat.mat_comp))
                str_list.append(
                    'therm grph_%s gre7.%dt\n' %
                    (a_mat.name,
                     id_list[bisect.bisect_left(temp_list, a_mat.temp)]))
            else:
                if tmp:
                    str_list.append(
                        '\nmat %s -%E tmp %f\n %s\n' %
                        (a_mat.name, a_mat.density, a_mat.temp, a_mat.mat_comp))
                else:
                    str_list.append(
                        '\nmat %s -%E\n %s\n' %
                        (a_mat.name, a_mat.density, a_mat.mat_comp))
            return ''.join(str_list)
