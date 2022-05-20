import glob
import numpy as np
import ECE16Lib.DSP as filt
import matplotlib.pyplot as plt

# Retrieve a list of the names of the subjects
def get_subjects(directory):
  filepaths = glob.glob(directory + "\\*")
  return [filepath.split("\\")[-1] for filepath in filepaths]

# Retrieve a data file, verifying its FS is reasonable
def get_data(directory, subject, trial, fs):
  search_key = "%s\\%s\\%s_%02d_*.csv" % (directory, subject, subject, trial)
  filepath = glob.glob(search_key)[0]
  t, ppg = np.loadtxt(filepath, delimiter=',', unpack=True)
  t = (t-t[0])/1e3
  hr = get_hr(filepath, len(ppg), fs)

  fs_est = estimate_fs(t)
  if(fs_est < fs-1 or fs_est > fs):
    print("Bad data! FS=%.2f. Consider discarding: %s" % (fs_est,filepath))

  return t, ppg, hr, fs_est

# Estimate the heart rate from the user-reported peak count
def get_hr(filepath, num_samples, fs):
  count = int(filepath.split("_")[-1].split(".")[0])
  seconds = num_samples / fs
  return count / seconds * 60 # 60s in a minute

# Estimate the sampling rate from the time vector
def estimate_fs(times):
  return 1 / np.mean(np.diff(times))

# Filter the signal (as in the prior lab)
def process(x):
  x = filt.detrend(x, 25)
  x = filt.moving_average(x, 5)
  x = filt.gradient(x)
  return filt.normalize(x)

# Verify the downloaded data
if __name__ == "__main__":
  directory = ".\\data"
  fs = 50
  subjects = get_subjects(directory)

  for subject in subjects:
    for trial in range(1,6):

      t, ppg, hr, fs_est = get_data(directory, subject, trial, fs)
      ppg_filtered = process(ppg)
      print("File: %s_%d, HR: %d, FS: %.2fHz" % (subject,trial,hr,fs_est))

      plt.subplot(211)
      plt.plot(t, ppg)
      plt.subplot(212)
      plt.plot(t, ppg_filtered)
      plt.show()