#!/usr/bin/env python3

# Find transits and occultations of planetary moons,
# currently of Jupiter or Saturn,
# as seen from the center of the Earth.
# Model both target bodies as ellipsoids.
# Search for every type of occultation.

# Adapted from the example on the documentation page for gfoclt
# https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/spicelib/gfoclt.html

import spiceypy

import os

KERNELDIR = os.path.expanduser("~/SPICE/kernels")

# Needed for leap seconds:
spiceypy.furnsh(os.path.join(KERNELDIR, "tls", "naif0009.tls"))

# Needed for body radii:
spiceypy.furnsh(os.path.join(KERNELDIR, "pck", "pck00008.tpc"))

# Jupiter and its major moons:
spiceypy.furnsh(os.path.join(KERNELDIR, "bsp", "jup310.bsp"))

# Saturn and its moons:
spiceypy.furnsh(os.path.join(KERNELDIR, "bsp", "sat288.bsp"))

# Generic solar system data; apparently it's already furnished
# by the Jupiter and Saturn moons files.
# spiceypy.furnsh(os.path.join(KERNELDIR, "bsp", "de421.bsp"))

types = [ "FULL", "ANNULAR", "PARTIAL", "ANY" ]

MAXWIN = 200

def occultations(body1, body2, start, end):
    cnfine = spiceypy.utils.support_types.SPICEDOUBLE_CELL(MAXWIN)
    result = spiceypy.utils.support_types.SPICEDOUBLE_CELL(MAXWIN)

    # Obtain the TDB time bounds of the confinement
    # window, which is a single interval in this case.
    et0 = spiceypy.str2et(start)
    et1 = spiceypy.str2et(end)

    # Insert the time bounds into the confinement window
    spiceypy.wninsd(et0, et1, cnfine)

    # 15-minute step. Ignore any occultations lasting less than 15 minutes.
    # Units are TDB seconds.
    step = 900.0

    obsrvr = "Earth"

    # Loop over the occultation types.
    for occtype in types:
        # For each type, do a search for both transits of
        # Titan across Saturn and occultations of Titan by Saturn.
        for j in range(2):
            if not j:
                front = body1
                fframe = "IAU_" + body1
                back = body2
                bframe = "IAU_" + body2
            else:
                front = body2
                fframe = "IAU_" + body2
                back = body1
                bframe = "IAU_" + body1

            spiceypy.gfoclt(occtype,
                            front, "ellipsoid", fframe,
                            back,  "ellipsoid", bframe,
                            "lt", obsrvr, step,
                            cnfine, result)

            # Display the results
            print()
            title = spiceypy.repmc("Condition: # occultation of # by #", "#",
                                   occtype)
            title = spiceypy.repmc(title, "#", back)
            title = spiceypy.repmc(title, "#", front)
            print(title)

            for r in result:
                print(spiceypy.timout(r, "YYYY Mon DD HR:MN:SC"))


if __name__ == '__main__':
    start = "2018 SEP 01 00:00:00 TDB"
    end = "2019 JAN 01 00:00:00 TDB"
    occultations("GANYMEDE", "JUPITER", start, end)

    # There are no Saturn/Titan transits at the end of 2018, maybe
    # because of the wide ring tilt, so use 2008 instead as a demo.
    start = "2008 SEP 01 00:00:00 TDB"
    end = "2009 JAN 01 00:00:00 TDB"
    occultations("TITAN", "SATURN", start, end)




