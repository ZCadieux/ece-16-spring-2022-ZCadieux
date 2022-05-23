from ECE16Lib.CircularList import CircularList
import ECE16Lib.DSP as filt
import numpy as np
import scipy.signal as sig

"""
A class to enable a simple step counter
"""
class Pedometer:
  """
  Encapsulated class attributes (with default values)
  """
  __steps = 0        # the current step count
  __jumps = 0        # the current jump count
  __l1 = None        # CircularList containing L1-norm
  __filtered = None  # CircularList containing filtered signal
  __num_samples = 0  # The length of data maintained
  __new_samples = 0  # How many new samples exist to process
  __fs = 50           # Sampling rate in Hz
  __b = None         # Low-pass coefficients
  __a = None         # Low-pass coefficients
  __thresh_low_s = 10   # Threshold from Tutorial 2
  __thresh_high_s = 150 # Threshold from Tutorial 2
  __thresh_low_j = 150   # Jump lower threshold
  __thresh_high_j = 300 # Jump upper threshold

  """
  Initialize the class instance
  """
  def __init__(self, num_samples, fs, data=None, low_s = 20, high_s = 100, low_j=150, high_j = 300):
    self.__steps = 0
    self.__jumps = 0
    self.__num_samples = num_samples
    self.__fs = fs
    self.__l1 = CircularList(data, num_samples)
    self.__filtered = CircularList([], num_samples)
    self.__b, self.__a = filt.create_filter(3, 2, "lowpass", fs)
    self.__thresh_low_s = low_s   # Threshold from Tutorial 2
    self.__thresh_high_s = high_s # Threshold from Tutorial 2
    self.__thresh_low_j = low_j   # Jump lower threshold
    self.__thresh_high_j = high_j # Jump upper threshold

  """
  Add new samples to the data buffer
  Handles both integers and vectors!
  """
  def add(self, ax, ay, az):
    l1 = filt.l1_norm(ax, ay, az)
    if isinstance(ax, int):
      num_add = 1
    else:
      num_add = len(ax)
      l1 = l1.tolist()

    self.__l1.add(l1)
    self.__new_samples += num_add

  """
  Process the new data to update step/jump count
  """
  def process(self):
    # Grab only the new samples into a NumPy array
    x = np.array(self.__l1[ -self.__new_samples: ])

    # Filter the signal (detrend, LP, MA, etc…)
    ma = filt.moving_average(x, 25)
    dt = filt.detrend(ma)
    x = filt.filter(self.__b, self.__a, dt)

    # Store the filtered data
    self.__filtered.add(x.tolist())

    # Count the number of peaks in the filtered data
    count_s, peaks_s = filt.count_peaks(x,self.__thresh_low_s,self.__thresh_high_s)
    count_j, peaks_j = filt.count_peaks(x,self.__thresh_low_j,self.__thresh_high_j)
    

    # Update the step count and reset the new sample count
    self.__steps += count_s
    self.__jumps += count_j
    self.__new_samples = 0

    # Return the step count, peak locations, and filtered data
    return self.__steps, peaks_s, self.__jumps, peaks_j, np.array(self.__filtered)

  """
  Clear the data buffers and step count
  """
  def reset(self):
    self.__steps = 0
    self.__jumps = 0
    self.__l1.clear()
    self.__filtered = np.zeros(self.__num_samples)