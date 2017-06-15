from util import sample_temperature as st
burnup_list = [1, 1, 2, 3, 4]

tsamp = st.LHS(burnup_list, 4, 2)
print('\ntsamp\n')
print(tsamp)
if tsamp.shape != (2, 4, 4):
  raise ValueError('wrong dimension')

fsamp = st.reshape(tsamp, burnup_list, 4, 2)
print('\nfsamp\n')
print(fsamp)
if fsamp.shape != (2, 4, 4+4):
  raise ValueError('wrong dimension')

fccsamp = st.fcc_sample(fsamp, burnup_list)
print('\nfccsamp\n')
print(fccsamp)
if fccsamp.shape != (2, 5, 4+4):
  print(fccsamp)
  raise ValueError('wrong dimension, should be(2, 5, 8), but is %r' %str(fccsamp.shape))

all_together = st.sample_temperature(burnup_list, 4, 2)
print('\nall_together\n')
print(all_together)
if fccsamp.shape != (2, 5, 4+4):
  raise ValueError('wrong dimension')

