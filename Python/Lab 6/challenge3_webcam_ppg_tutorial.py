from hashlib import new
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
plt.style.use('seaborn-whitegrid')

ppg = []
timestamps = []
#cap = cv2.VideoCapture(0) # choose your appropriate camera!
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while(True):
  _, frame = cap.read() 
  new_sample = frame.mean(axis=0).mean(axis=0)
  new_sample = -new_sample[2] # replace the ? with index of the RED channel
  ppg.append(new_sample) # append new_sample to ppg
  timestamps.append(time.time_ns()/10**9)
  cv2.imshow('Input', frame)
  c = cv2.waitKey(1)
  if c == 27:
    break
cap.release()
cv2.destroyAllWindows()

fig = plt.figure()
ax = plt.axes()
p = ppg[10:]
t = np.array(timestamps[10:]) # so we can easily subtract the first time
t = t - t[0]
print(t)
ax.set_xlabel("time(s)")
ax.set_ylabel("Red Channel Value")

ax.plot(t, p)
plt.show()
