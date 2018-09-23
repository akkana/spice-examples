#!/usr/bin/env python3

# Cassini position example, from
# https://spiceypy.readthedocs.io/en/master/exampleone.html
# fleshed out with some more details about how to fetch and load the kernels.

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import spiceypy as spice

import os

# The kernels are at the following URLs:
#   https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/a_old_versions/naif0009.tls
#   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/sclk/cas00084.tsc
#   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/pck/cpck05Mar2004.tpc
#   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/fk/release.11/cas_v37.tf
#   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/ck/04135_04171pc_psiv2.bc
#   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/030201AP_SK_SM546_T45.bsp
#   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/ik/release.11/cas_iss_v09.ti
#   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/020514_SE_SAT105.bsp
#   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/981005_PLTEPH-DE405S.bsp

kernels = [
    "tls/naif0009.tls",
    "cassini/cas00084.tsc",
    "tpc/cpck05Mar2004.tpc",
    "bsp/020514_SE_SAT105.bsp",
    "bsp/981005_PLTEPH-DE405S.bsp",
    "bsp/030201AP_SK_SM546_T45.bsp",
    "cassini/04135_04171pc_psiv2.bc",
    "cassini/cas_v37.tf",
    "cassini/cas_iss_v09.ti"
]

# Set to the directory where you store your SPICE kernels:
KERNELDIR = os.path.expanduser("~/SPICE/kernels")

for k in kernels:
    spice.furnsh(os.path.join(KERNELDIR, k))

step = 4000
# we are going to get positions between these two dates
utc = ['Jun 20, 2004', 'Dec 1, 2005']

# get et values one and two, we could vectorize str2et
etOne = spice.str2et(utc[0])
etTwo = spice.str2et(utc[1])
print("ET One: {}, ET Two: {}".format(etOne, etTwo))

# get times
times = [x*(etTwo-etOne)/step + etOne for x in range(step)]

# check first few times:
print(times[0:3])

# check the documentation on spkpos before continuing
# help(spice.spkpos)

#Run spkpos as a vectorized function
positions, lightTimes = spice.spkpos('Cassini', times, 'J2000', 'NONE', 'SATURN BARYCENTER')

# Positions is a 3xN vector of XYZ positions
print("Positions: ")
print(positions[0])

# Light times is a N vector of time
print("Light Times: ")
print(lightTimes[0])

# Clean up the kernels
spice.kclear()

# Use matplotlib’s 3D plotting to visualize Cassini’s coordinates.
# First convert the positions list to a 2D numpy array
# for easier indexing in the plot.
positions = np.asarray(positions).T # positions is a list, make it an ndarray for easier indexing
fig = plt.figure(figsize=(9, 9))
ax  = fig.add_subplot(111, projection='3d')
ax.plot(positions[0], positions[1], positions[2])
plt.title('SpiceyPy Cassini Position Example from Jun 20, 2004 to Dec 1, 2005')
plt.show()



