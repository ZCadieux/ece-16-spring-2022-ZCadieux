import glob
import numpy as np
import ECE16Lib.DSP as filt
import matplotlib.pyplot as plt
# The GMM Import
from sklearn.mixture import GaussianMixture as GMM
# Import for Gaussian PDF
from scipy.stats import norm

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

# Plot each component of the GMM as a separate Gaussian
def plot_gaussian(weight, mu, var):
  weight = float(weight)
  mu = float(mu)
  var = float(var)

  x = np.linspace(0, 1)
  y = weight * norm.pdf(x, mu, np.sqrt(var))
  plt.plot(x, y)

# Estimate the heart rate given GMM output labels
def estimate_hr(labels, num_samples, fs):
  peaks = np.diff(labels, prepend=0) == 1
  count = sum(peaks)
  seconds = num_samples / fs
  hr = count / seconds * 60 # 60s in a minute
  return hr, peaks

# Test GMM Modeling
if __name__ == "__main__":
  fs = 50
  directory = ".\\data"
  subject = "a03884563"

  # Load all the data for the subject
  train_data = np.array([])
  for trial in range(1,6):
    print(directory, subject, trial, fs)
    t, ppg, hr, fs_est = get_data(directory, subject, trial, fs)
    ppg_filtered = process(ppg)
    train_data = np.append(train_data, ppg_filtered)

  # Train the GMM with the training data
  gmm = GMM(n_components=2).fit(train_data.reshape(-1,1))

  # Compare the histogram with the GMM to make sure it is a good fit
  plt.hist(train_data, 100, density=True)
  plot_gaussian(gmm.weights_[0], gmm.means_[0], gmm.covariances_[0])
  plot_gaussian(gmm.weights_[1], gmm.means_[1], gmm.covariances_[1])
  plt.show()

  # Test the GMM on the same training data... BAD!!!
  for trial in range(1,6):
    t, ppg, hr, fs_est = get_data(directory, subject, trial, fs)
    ppg_filtered = process(ppg)

    labels = gmm.predict(ppg_filtered.reshape(-1,1))
    hr_est, peaks = estimate_hr(labels, len(ppg), fs)
    print("File: %s_%s: HR: %3.2f, HR_EST: %3.2f" % (subject,trial,hr,hr_est))

    plt.plot(ppg_filtered)
    plt.plot(peaks)
    plt.show()