import numpy as np
import matplotlib.pyplot as plt
import sys

path_data = str(sys.argv[1])
path_data_s = str(sys.argv[2])
name = str(sys.argv[3])

data = np.load(path_data)
data = np.transpose(data)

plt.title(name)

plt.plot(data[0],data[1],label='Data raw',marker='s')

if path_data_s != '0':
	data_s = np.load(path_data_s)
	data_s =  np.transpose(data_s)
	plt.plot(data_s[0],data_s[1],label='Data reduced',marker='o')

print(np.shape(data_s))
plt.xlabel('x / mm')
plt.ylabel('y / mm')
plt.legend()
plt.axis('scaled')
plt.show()

#Pfade von *.npy anpassen, dass sie individuell sind und auch wieder gelöscht werden. Sonst nur ein plot möglich
