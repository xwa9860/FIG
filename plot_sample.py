import numpy as np
import matplotlib.pyplot as plt

mat = np.load('temp.npy')
plt.hist(mat[:, :, 1])
plt.savefig('1')
