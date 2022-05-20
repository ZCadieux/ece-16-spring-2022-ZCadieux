# Import for searching a directory
import glob

# The usual suspects
import numpy as np
import ECE16Lib.DSP as filt
import matplotlib.pyplot as plt

# The GMM Import
from sklearn.mixture import GaussianMixture as GMM

# Import for Gaussian PDF
from scipy.stats import norm
from scipy import stats

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

# Run the GMM with Leave-One-Subject-Out-Validation
if __name__ == "__main__":
  #GENERATE DATA
  fs = 50
  directory = ".\\data"
  subjects = get_subjects(directory)
  ground_truthHRs = []
  estimatedHRs = []

  # Leave-One-Subject-Out-Validation
  # 1) Exclude subject
  # 2) Load all other data, process, concatenate
  # 3) Train the GMM
  # 4) Compute the histogram and compare with GMM
  # 5) Test the GMM on excluded subject
  for exclude in subjects:
    print("Training - excluding subject: %s" % exclude)
    train_data = np.array([])
    for subject in subjects:
      for trial in range(1,6):
        t, ppg, hr, fs_est = get_data(directory, subject, trial, fs)

        if subject != exclude:
          train_data = np.append(train_data, process(ppg))

    # Train the GMM
    train_data = train_data.reshape(-1,1) # convert from (N,1) to (N,) vector
    gmm = GMM(n_components=2).fit(train_data)

    # PLOTTING REMOVED
    # Test the GMM on excluded subject
    print("Testing - all trials of subject: %s" % exclude)
    for trial in range(1,6):
      t, ppg, hr, fs_est = get_data(directory, exclude, trial, fs)
      test_data = process(ppg)

      labels = gmm.predict(test_data.reshape(-1,1))

      hr_est, peaks = estimate_hr(labels, len(ppg), fs)
      print("File: %s_%s: HR: %3.2f, HR_EST: %3.2f" % (exclude,trial,hr,hr_est))
      ground_truthHRs.append(hr)
      estimatedHRs.append(hr_est)

      # PLOTTING REMOVED
    
  # DATA ANALYSIS
  RMS = np.sqrt(np.sum((np.subtract(ground_truthHRs, estimatedHRs)**2)/len(estimatedHRs)))
  [R,p] = stats.pearsonr(ground_truthHRs, estimatedHRs) # correlation coefficient
  dif = np.subtract(ground_truthHRs, estimatedHRs) # take the difference between ground_truth and estimates
  bias = np.average(dif) # get the mean value of the difference
  print(RMS)
  print(R)
  print(bias)
  plt.plot(estimatedHRs, estimatedHRs)
  plt.scatter(ground_truthHRs, estimatedHRs)
  plt.xlabel("Reference HR (BPM)")
  plt.ylabel("GMM Estimated HR (BPM)")
  plt.title("RMS = {:.2f}, Correlation = {:.2f}, Bias = {:.2f}".format(RMS, R, bias))
  plt.show()
