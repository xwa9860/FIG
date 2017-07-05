import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

mat = np.load('sample.npy')
print(mat.shape)
fig, ax = plt.subplots()
ax.plot(mat.reshape(12, 16), 'o')

loc = ticker.MultipleLocator(base=100)
ax.xaxis.set_major_locator(loc)
ax.yaxis.set_major_locator(loc)

# Add the grid
ax.grid(which='major', axis='both', linestyle='-')

#start, end = ax.get_xlim()
#ax.yaxis.set_ticks(np.arange(start, end, 100))
#ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
#ax.grid(True)
plt.show()

