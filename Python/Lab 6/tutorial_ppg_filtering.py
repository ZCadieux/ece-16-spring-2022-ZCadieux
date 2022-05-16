import ECE16Lib.DSP as filt
from matplotlib import pyplot as plt
import numpy as np

# Load the data as a 500x2 ndarray and extract the 2 arrays
data = np.genfromtxt("./data/ramsink_01_13.csv", delimiter=",")
t = data[:,0]
t = (t - t[0])/1e3
ppg = data[:,1]

# Detrend the signal and plot the result
dt = filt.detrend(ppg, 25)

plt.subplot(211)
plt.title("Detrend")
plt.plot(t, ppg)
plt.subplot(212)
plt.plot(t, dt)
plt.show()

# Smooth the signal with a small moving average
ma = filt.moving_average(dt, 5)

plt.subplot(211)
plt.title("Moving Average")
plt.plot(t, ppg)
plt.subplot(212)
plt.plot(t, ma)
plt.show()

# Highlight the peaks with the derivative
grad = filt.gradient(ma)

plt.subplot(211)
plt.title("Gradient")
plt.plot(t, ppg)
plt.subplot(212)
plt.plot(t, grad)
plt.show()

# Normalize the signal
norm = filt.normalize(grad)

plt.subplot(211)
plt.title("Normalize")
plt.plot(t, ppg)
plt.subplot(212)
plt.plot(t, norm)
plt.show()

# Count the peaks
thresh = 0.6
count, peaks = filt.count_peaks(norm, thresh, 1)

plt.plot(t, norm)
plt.title("Detected Peaks = %d" % count)
plt.plot(t[peaks], norm[peaks], 'rx')
plt.plot(t, [thresh]*len(norm), "b--")
plt.show()

# Compute the heart rate
avg_beat_time = np.mean(np.diff(t[peaks]))
bpm = 60/avg_beat_time
print("Estimated heart rate: {:.2f} bpm".format(bpm))

# Estimated rate of 74.37 bpm