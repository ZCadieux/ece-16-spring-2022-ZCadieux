import numpy as np #import numpy

# 1D Array
a = np.array([1, 2, 3])
#print(a)

# 2D Array
a = np.array([(1,2,3),(4,5,6)])
#print(a)

# 3D Array (shape = (2,2,3))
a = np.array([[[1,2,3],[4,5,6]],[[7,8,9],[10,11,12]]])
#print(a)
#print(a.shape)

# Python list to NumPy array
myList = [1,2,9,8]
a = np.array(myList)
#print(a)

# initialize without lists
# using np.zeros
a = np.zeros((2,2))
#print(a)

# using np.ones
a = np.ones((3,3))
#print(a)

# Restructuring Arrays
# with numpy.reshape()
a = np.array([(1,2,3),(4,5,6)])
a.reshape(3,2)
#print(a)

#with numpy.flatten()
a = np.array([(1,2,3),(4,5,6)])
b = a.flatten()
b.shape # (6,) NOT (6,1)!
#print(a)
#print(b)