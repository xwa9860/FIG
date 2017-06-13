
'''
generate Latin Hypercube sampling for T_fuel from a uniform distribution Unif(600, 1200)
'''
from pyDOE import *
from scipy.stats import uniform
from more_itertools import unique_everseen

def sampling_temp(burnup_list, layer_nb, sample_nb):
  '''
  return tsample: a len(burnup_list) x sample_nb matrix of randomly sampled temperatures between 600 and 1200 K 
  '''
  unique_burnups = list(unique_everseen(burnups))
  range = [600, 1200]  # range of the temperatures in K
  sample = lhs(len(unique_burnups)*layer_nb, samples = sample_nb)
  tsample = uniform(loc=range[0], scale=range[1]).ppf(sample)
  res =[t[(burnup-1)*layer_nb:burnup*layer_nb].extend(ones(5)*t[burnup*layer_nb] for burnup in burnup list]
  return tsample


