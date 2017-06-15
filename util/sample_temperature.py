
'''
generate Latin Hypercube sampling for T_fuel from a uniform distribution Unif(600, 1200)
'''
from pyDOE import *
from scipy.stats import uniform
from more_itertools import unique_everseen
import numpy as np


def sample_temperature(burnup_list, layer_nb, sample_nb):
  '''
  the 'main' function in this file
  layer_nb: the number of layers in a triso, including fuel and other layers,
  e.g.: if the outer layers are combined as one and the fuel kernel is divided into 3 layers, then layer_nb = 4
  '''
  LHSamp = LHS(burnup_list, layer_nb, sample_nb)
  reshapeSamp = reshape(LHSamp, burnup_list, layer_nb, sample_nb)
  return reshapeSamp

def LHS(burnup_list, layer_nb, sample_nb):
  '''
  return tsample: a len(burnup_list) x sample_nb matrix of randomly sampled temperatures between 600 and 1200 K 
  '''
  unique_burnups = list(unique_everseen(burnup_list))
  range = [600, 1200]  # range of the temperatures in K
  sample = lhs(len(unique_burnups)*layer_nb, samples = sample_nb)
  tsample = uniform(loc=range[0], scale=range[1]).ppf(sample).reshape((sample_nb, len(unique_burnups), layer_nb))
  return tsample

def reshape(mat, burnup_list, layer_nb, sample_nb):
  '''
  reshape the result from sampling_temp to a matrix that can be used for creating the
  FCC unit cell
  '''
  bu_nb = len(list(unique_everseen(burnup_list)))
  full_mat =np.append(mat[:, :, 0:layer_nb-1], 
                      mat[:,:, layer_nb-1].reshape(sample_nb, bu_nb, 1)*np.ones((sample_nb, bu_nb, 5)), axis=2)
  return full_mat 

def fcc_sample(full_mat, burnup_list):
  '''
  take a matrix of temperatures of unique burnups
  copy and rearrange the rows for 14 pebbles in a fcc
  '''
  res =np.array([[[full_mat[i, burnup-1, j] for j in range(full_mat.shape[2])] for burnup in burnup_list] for i in range(full_mat.shape[0])])
  return res


