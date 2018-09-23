#!/usr/bin/env python3

#
# Solution mrotat
#
# From the official SpiceyPy "Binary PCK" lesson
# https://spiceypy.readthedocs.io/en/doc_changes_conda_forge_etc/binary_pck.html
# which in turn is taken from the official SPICE lessons.
#

from __future__ import print_function

#
# SpiceyPy package:
#
import spiceypy
import os

KERNELDIR = os.path.expanduser("~/SPICE/kernels")

kernels = [
    # Needed for leap seconds:
    os.path.join(KERNELDIR, "tls", "naif0009.tls"),

    # needed for body radii:
    os.path.join(KERNELDIR, "pck", "pck00008.tpc"),

    # Don't know what the rest of these are:
    os.path.join(KERNELDIR, "spk", "de414_2000_2020.bsp"),
    os.path.join(KERNELDIR, "fk", "moon_060721.tf"),
    os.path.join(KERNELDIR, "pck", "moon_pa_de403_1950-2198.bpc")
]

def load_kernels():
    for k in kernels:
        spiceypy.furnsh(k)

def unload_kernels():
    # Provided purely as an example. spice.kclear() is a simpler option.
    for k in kernels:
        spiceypy.unload(k)

def mrotat():
    #
    # Convert our UTC string to seconds past J2000 TDB.
    #
    timstr = '2007 JAN 1 00:00:00'
    et     = spiceypy.str2et( timstr )

    #
    # Look up the apparent position of the Earth relative
    # to the Moon's center in the IAU_MOON frame at ET.
    #
    [imoonv, ltime] = spiceypy.spkpos(
        'earth', et, 'iau_moon', 'lt+s', 'moon' )

    #
    #Express the Earth direction in terms of longitude
    #and latitude in the IAU_MOON frame.
    #
    [r, lon, lat] = spiceypy.reclat( imoonv )

    print( '\n'
           'Moon-Earth direction using low accuracy\n'
           'PCK and IAU_MOON frame:\n'
           'Earth lon (deg):        {0:15.6f}\n'
           'Earth lat (deg):        {1:15.6f}\n'.format(
               lon * spiceypy.dpr(),
               lat * spiceypy.dpr() )  )
    #
    # Look up the apparent position of the Earth relative
    # to the Moon's center in the MOON_ME frame at ET.
    #
    [mmoonv, ltime] = spiceypy.spkpos( 'earth', et, 'moon_me',
                                       'lt+s', 'moon'        )
    #
    # Express the Earth direction in terms of longitude
    # and latitude in the MOON_ME frame.
    #
    [r, lon, lat] = spiceypy.reclat( mmoonv )

    print( 'Moon-Earth direction using high accuracy\n'
           'PCK and MOON_ME frame:\n'
           'Earth lon (deg):        {0:15.6f}\n'
           'Earth lat (deg):        {1:15.6f}\n'.format(
               lon * spiceypy.dpr(),
               lat * spiceypy.dpr() )  )
    #
    # Find the angular separation of the Earth position
    # vectors in degrees.
    #
    sep = spiceypy.dpr() * spiceypy.vsep( imoonv, mmoonv )

    print( 'For IAU_MOON vs MOON_ME frames:' )
    print( 'Moon-Earth vector separation angle (deg):     '
           '{:15.6f}\n'.format( sep )  )
    #
    # Look up the apparent position of the Earth relative
    # to the Moon's center in the MOON_PA frame at ET.
    #
    [pmoonv, ltime] = spiceypy.spkpos( 'earth', et, 'moon_pa',
                                       'lt+s',  'moon'        )
    #
    # Express the Earth direction in terms of longitude
    # and latitude in the MOON_PA frame.
    #
    [r, lon, lat] = spiceypy.reclat( pmoonv )

    print( 'Moon-Earth direction using high accuracy\n'
           'PCK and MOON_PA frame:\n'
           'Earth lon (deg):        {0:15.6f}\n'
           'Earth lat (deg):        {1:15.6f}\n'.format(
               lon * spiceypy.dpr(),
               lat * spiceypy.dpr() )  )
    #
    # Find the angular separation of the Earth position
    # vectors in degrees.
    #
    sep = spiceypy.dpr() * spiceypy.vsep( pmoonv, mmoonv )

    print( 'For MOON_PA vs MOON_ME frames:' )
    print( 'Moon-Earth vector separation angle (deg):     '
           '{:15.6f}\n'.format( sep )  )
    #
    # Find the apparent sub-Earth point on the Moon at ET
    # using the MOON_ME frame.
    #
    [msub, trgepc, srfvec ] = spiceypy.subpnt(
        'near point: ellipsoid', 'moon',
        et,  'moon_me', 'lt+s',  'earth' )
    #
    # Display the sub-point in latitudinal coordinates.
    #
    [r, lon, lat] = spiceypy.reclat( msub )

    print( 'Sub-Earth point on Moon using high accuracy\n'
           'PCK and MOON_ME frame:\n'
           'Sub-Earth lon (deg):   {0:15.6f}\n'
           'Sub-Earth lat (deg):   {1:15.6f}\n'.format(
               lon * spiceypy.dpr(),
               lat * spiceypy.dpr()  )  )
    #
    # Find the apparent sub-Earth point on the Moon at
    # ET using the MOON_PA frame.
    #
    [psub, trgepc, srfvec] = spiceypy.subpnt(
        'near point: ellipsoid',  'moon',
         et,   'moon_pa', 'lt+s', 'earth'    )
    #
    # Display the sub-point in latitudinal coordinates.
    #
    [r, lon, lat] = spiceypy.reclat( psub )

    print( 'Sub-Earth point on Moon using high accuracy\n'
           'PCK and MOON_PA frame:\n'
           'Sub-Earth lon (deg):   {0:15.6f}\n'
           'Sub-Earth lat (deg):   {1:15.6f}\n'.format(
               lon * spiceypy.dpr(),
               lat * spiceypy.dpr() )  )
    #
    # Find the distance between the sub-Earth points
    # in km.
    #
    dist = spiceypy.vdist( msub, psub )

    print( 'Distance between sub-Earth points (km): '
           '{:15.6f}\n'.format( dist )  )

if __name__ == '__main__':
    load_kernels()
    mrotat()
    unload_kernels()



