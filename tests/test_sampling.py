from util import sample_temperature as st
burnup_nb = 4

tsamp = st.LHS(burnup_nb, 4, 2)
print('\ntsamp\n')
print(tsamp)
if tsamp.shape != (2, 4, 4):
  raise ValueError('wrong dimension')

fsamp = st.reshape(tsamp, burnup_nb, 3, 1, 2)
print('\nfsamp\n')
print(fsamp)
if fsamp.shape != (2, 4, 4):
  raise ValueError('wrong dimension')

all_together = st.sample_temperature(burnup_nb, 3, 1, 2)
print('\nall_together\n')
print(all_together)
if all_together.shape != (2, 4, 4):
  raise ValueError('wrong dimension')

