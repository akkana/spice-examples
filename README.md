# spice-examples

## Examples of how to use NAIF SPICE for planetary and satellite calculations

NAIF is NASA's Navigation and Ancillary Information Facility, and
[SPICE](https://naif.jpl.nasa.gov/naif/index.html)
is their library for writing software.

Currently most of the examples here use the
[SpiceyPy Python bindings for SPICE](https://github.com/AndrewAnnex/SpiceyPy).

There isn't much documentation for either SPICE or SpiceyPy.
Two useful starting points:

- The [SpiceyPy Documentation](https://spiceypy.readthedocs.io/en/master/)
  includes a copy of the official SPICE lessons, so it's a great place to start.

- [NAIF's Most Used APIs](https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/info/mostused.html)
  has quite a few useful recipes.

The tricky part about programming in SPICE is that most SPICE programs
require SPICE "kernels" which must be downloaded from NAIF. Kernels
contain models and data which are then used by the high-level SPICE
functions. So, for instance, you can copy the occultation example from
the Most Used APIs page, but it won't work unless you also have the
"cas_2005_v17.tm" kernel used in the example -- and the page doesn't
give you any hint where to get that. And if you change the observer
to EARTH instead of CASSINI, it still won't work because then you
need another SPICE kernel to get the Saturn, Sun and Earth data.

## Finding Kernels

So finding kernels is the key to learning to program in SPICE ... and
none of the documentation tells you how to find them. There doesn't
seem to be any document listing what kernels are available and what's
in each of them, so plan on spending some time hunting.
Here's what I've learned so far:

[The top-level page for SPICE kernels](https://naif.jpl.nasa.gov/naif/data.html)
has three links:

- [PDS Archived SPICE Data Sets](https://naif.jpl.nasa.gov/naif/data_pds_archived.html) -
  kernels related to older spacecraft.
- [Operational Flight Projects Kernels and Other Non-archived Project Kernels](https://naif.jpl.nasa.gov/naif/data_operational.html) -
  kernels related to currently operational or recently retired spacecraft
- [Generic Kernels](https://naif.jpl.nasa.gov/naif/data_generic.html) -
  kernels not related to spacecraft, for instance, natural Solar System bodies.

For spacecraft data, click on the appropriate link (depending on
whether the desired spacecraft is currently or recently operational
or not), look for its name and try to guess which file to download.
If you find a better way, let me know and I'll update this README.

Most of my programming involves planets and natural satellites, which
only require the Generic Kernels.

### Searching for a Specific Kernel

If you're just starting out, trying to get the examples to work,
you may already know the filename you need. For instance, suppose
an example uses *de421.bsp* and you just need to know where to find it.

Here's a handy trick. You can get a full listing of the directory
structure for the generic kernels with the lftp program:

```
lftp https://naif.jpl.nasa.gov/pub/naif/generic_kernels/
```

Then, at the lftp prompt, type: ```du -a > generic_manifest.txt```

Exit lftp, and you'll have a file called *generic_manifest.txt*
containing the full structure of all the generic manifests.
You will also have a directory called *naif.jpl.nasa.gov* containing
only empty directories, which you can ```rm -rf``` since it doesn't
do you any good.

(There ought to be some way to do this using wget or curl, but
I couldn't find a way that actually worked. Even better, I'd like
to fetch the whole directory structure but only files starting with
aaa or AAA, not the actual data files. Anyone know how to do that?
I may eventually write a Python script for it.)

Now that you have generic_manifest.txt, you can grep for filenames:
```
$ grep de421.bsp generic_manifest.txt
16397   ./spk/planets/a_old_versions/de421.bsp
```

Append the pathname it gives you to
```https://naif.jpl.nasa.gov/pub/naif/generic_kernels/```
so you can fetch the file with wget:

```
wget https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de421.bsp
```

You can do that for the spacecraft kernels too, but if you start at
the root of the tree it'll be a big fetch, so you might want to do it
just for the spacecraft you're interested in, like Cassini.

### Exploring Generic Kernels

The Generic Kernels don't have a helpful page explaining what's what:
you have to click around in the data,
(https://naif.jpl.nasa.gov/pub/naif/generic_kernels/)
to see what's what.

There's a file called *aareadme.txt* that explains the other subdirectories:
- dsk, Digital Shape Kernel (for modeling the shape of a few natural bodies)
- fk, Frames Kernel (for specific missions, it's not clear what they contain)
- lsk, Leapseconds Kernel (for accurate time calculations)
- pck, Planetary Constants Kernel (data related to orbits of major
  natural solar system bodies)
- spk, Spacecraft and Planet Kernel (orbits and other details of
  planets, natural satellites, and a few comets and asteroids,
  plus the location of the Deep Space  Network (DSN) ground stations
  relative to the center of the earth).
- stars, a few star catalogs.

In each of these directories (and most of their subdirectories), the
file *aa_summaries.txt* gives you information about what's there.

So, suppose I want to write a program to see when Ganymede transits Jupiter.
Probably a lot of kernels have Jupiter in them, but Ganymede will be
harder, so let's start by looking for that. It's a natural satellite,
so I'll guess it will be somewhere
*https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk*,
so I go there. *AAREADME_SPKs.txt* in that directory isn't helpful,
just generic information about kernels, but there are subdirectories
*asteroids, comets, lagrange_point, planets, satellites, stations*.
In *satellites*, the file *AAREADME_Satellite_SPKs* tells me that
there may be one or several files for each planet that has satellites,
and that there's no overlap: so Ganymede will be in only one of the
Jupiter SPK files. It also tells me that the *aa_summaries* file gives
me a listing of which satellites are in which file.

So next, I read
[aa_summaries.txt](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/aa_summaries.txt)
in that directory, and right away I see that
```
GANYMEDE (503) w.r.t. JUPITER BARYCENTER (5)
```
is in jup310.bsp, so that's the file I want to download.

You'll generally find you need several kernels. For instance,
for Ganymede and Jupiter, when I tried it with just jup310.bsp
I got an error about needing leap seconds, and when I fixed that
I got a different error. In the end,
I needed naif0009.tls for leap seconds,
jup310.bsp for Ganymede and Jupiter,
and
pck00008.tpc for a variable called BODY503_RADII
(I guess jup310.bsp has orbits but not sizes).

Figuring out what kernels you need is a fairly elaborate and
mysterious process and is definitely the hardest part of using SPICE.

## Specifying Kernels

Once you have your kernels downloaded, you can specify them in Python
like this:

```
# Needed for leap seconds:
spiceypy.furnsh("/path/to/kernels/tls/naif0009.tls")

# Jupiter and its major moons:
spiceypy.furnsh("/path/to/kernels/bsp/jup310.bsp")
```

You don't have to use subdirectories like tls and bsp, but a lot
of the code seems structured like that so I'm following suit.
For the path on your filesystem, so you can either have
a relative directory called *kernels*, or set up some known location
like ~/.cache/SPICE/kernels or ~/SPICE/kernels or whatever you like.
I'm going to use an absolute path.

In a lot of SPICE examples, you'll see *furnsh* called on a file ending
in *.tm*. Such a file might look like this:

```
\begindata
KERNELS_TO_LOAD = ( 'kernels/tls/naif0009.tls',
                    'kernels/bsp/sat288.bsp',
                    'kernels/bsp/jup310.bsp',
                    'kernels/pck/pck00008.tpc' )
\begintext
```

I'm not sure I see the advantage of this; I think I'm going to stick
to separate *furnsh* calls built into my Python scripts so my scripts
can work without needing a .tm file. That's one of the problems with
those otherwise useful examples on the
[Most Used APIs](https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/info/mostused.html)
page -- since they assume a .tm file but they don't include that file,
you have no idea what kernels you need to make the examples work.

## RTFM

I know I've been negative about the documentation: it's mostly poorly
written and makes it very hard to get started or to figure out kernels.
But the documentation for individual functions is quite extensive and
well worth reading. For instance, there are some nice examples of
how to find occultations of Titan by Saturn and vice versa in the
[gfoclt documentation page](https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/spicelib/gfoclt.html)
and that's fairly typical for documentation of SPICE functions:
there's a lot of good information there even if some of the examples
aren't clear about what kernels they use.

