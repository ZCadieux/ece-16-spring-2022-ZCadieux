from ECE16Lib.HRMonitor import HRMonitor
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import stats

def eval_hr_monitor():
    # Load the data as a 500x2 ndarray and extract the 2 arrays
    monitor_rates = []
    directory = './data/A15912942'
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        data = np.genfromtxt(file, delimiter=",")
        t = data[:,0]
        t = (t - t[0])/1e3
        ppg = data[:,1]

        # Test the Heart Rate Monitor with offline data
        hr_monitor = HRMonitor(3000, 50)
        hr_monitor.add(t, ppg)
        hr, peaks, filtered = hr_monitor.process()
        monitor_rates.append(hr)
        # Plot the results
        plt.plot(t, filtered)
        plt.title("Estimated Heart Rate: {:.2f} bpm".format(hr))
        plt.plot(t[peaks], filtered[peaks], 'rx')
        plt.plot(t, [0.6]*len(filtered), "b--")
        plt.show()

    return monitor_rates

ground_truth = [82, 81, 79, 72, 79] # reference heart rates
estimates = eval_hr_monitor() # estimated heart rates from your algorithm
print(ground_truth)
print(estimates)

[R,p] = stats.pearsonr(ground_truth, estimates) # correlation coefficient

plt.figure(1)
plt.clf()

# Correlation Plot
plt.subplot(211)
plt.plot(estimates, estimates)
plt.scatter(ground_truth, estimates)

plt.ylabel("Estimated HR (BPM)")
plt.xlabel("Reference HR (BPM)")
plt.title("Correlation Plot: Coefficient (R) = {:.2f}".format(R))

# Bland-Altman Plot
avg = np.add(ground_truth, estimates)/2 # take the average between each element of the ground_truth and
      # estimates arrays and you should end up with another array
dif = np.subtract(ground_truth, estimates) # take the difference between ground_truth and estimates
std = np.std(dif) # get the standard deviation of the difference (using np.std)
bias = np.average(dif) # get the mean value of the difference
upper_std = (bias+1.96)*std # the bias plus 1.96 times the std
lower_std = (bias-1.96)*std # the bias minus 1.96 times the std

plt.subplot(212)
plt.scatter(avg, dif)

plt.plot(avg, len(avg)*[bias])
plt.plot(avg, len(avg)*[upper_std])
plt.plot(avg, len(avg)*[lower_std])

plt.legend(["Mean Value: {:.2f}".format(bias),
  "Upper bound (+1.96*STD): {:.2f}".format(upper_std),
  "Lower bound (-1.96*STD): {:.2f}".format(lower_std)
])

plt.ylabel("Difference between estimates and ground_truth (BPM)")
plt.xlabel("Average of estimates and ground_truth (BPM)")
plt.title("Bland-Altman Plot")
plt.show()

#changed moving average window and detrend value by small amounts
# issue was lower peaks getting counted when they shouldnt have been