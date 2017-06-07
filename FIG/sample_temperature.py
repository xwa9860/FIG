
'''
generate Latin Hypercube sampling for T_fuela_1-24 from a uniform distribution
'''
from pyDOE import *
from scipy.stats import uniform

def sampling_temp(factor_nb, sample_nb):
  range = [600, 1200]  # range of the temperatures in K
  sample = lhs(factor_nb, samples = sample_nb)
  tsample = uniform(loc=range[0], scale=range[1]).ppf(sample)
  return tsample


