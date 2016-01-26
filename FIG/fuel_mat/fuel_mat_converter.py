#!/usr/bin/python
'''
generate pebble position (material distribution) files

'''
#with open('bk_batch.sub', 'a+') as m:
temp = 900
for i in range(1, 9):
  with open('fuel_comp%d' %i, 'w+') as f:
    with open('bu%d.eq'%i, 'r+') as input:
        lines = input.readlines()
        for line in lines:
            f.write(line[3:20])
            f.write('\n')

# #change pb position input file name in the serpent input files fhr_burnup_fuel
# with open('fhr_burnup_fuel', 'r+') as f:
#     with open('fhr_sep_input', 'w+') as input:
#       cur_fhr_data = f.read()
#       cur_fhr_data = cur_fhr_data.replace('pebbles_position_i', 'pebble_pos'+str(i))
#       input.write(cur_fhr_data)
#       rename('fhr_sep_input', 'fhr_burnup_fuel'+str(i))

      #m.write('srun sss2 fhr_burnup_fuel'+str(i)+'\n')
