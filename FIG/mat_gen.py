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
            str_list.append('\nmat %s -%E'
                            % (a_mat.name, a_mat.density))
            if a_mat.flag == 'moder':
                str_list.append(' moder grph_%s 6000'
                                % a_mat.name)
            if tmp:
                str_list.append(' tmp %f'
                                % a_mat.temp)
            if a_mat.rgb:
                str_list.append(' rgb %s'
                                % (' '.join(str(x) for x in a_mat.rgb)))
            str_list.append('\n %s'
                            % a_mat.mat_comp)

            if a_mat.flag == 'moder':
                str_list.append(
                    'therm grph_%s gre7.%dt\n' %
                    (a_mat.name,
                     id_list[bisect.bisect_left(temp_list, a_mat.temp)]))
            return ''.join(str_list)
