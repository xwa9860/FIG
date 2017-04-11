#!/usr/bin/python
'''get fuel composition from Mark1.txt file
'''

for p in range(1, 9):
    mat_bu_file = ''.join(['bu', str(p), '.eq'])
    fuel_comp = []
    with open(mat_bu_file, 'r+') as bu_file:
        for line in bu_file:
            fuel_comp.append(''.join(['        ', line]))
        fuel_comp = ''.join(fuel_comp)
        for R in range(1, 5):
            for Z in range(1, 6):
                mat_name = 'm%d%d%d00 $ tmp=1.00588E+03K\n' % (R, Z, p)
                mat_comp = ''.join([mat_name, fuel_comp])
                with open('mat_file', 'a+') as outputf:
                    outputf.write(mat_comp)
