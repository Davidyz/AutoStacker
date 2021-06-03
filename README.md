# AutoStacker

**!!! This project is still under development and is not functional yet !!!**

This is a script that attempts to automate the stacking process for noise
reduction and/or simulating long-exposure effect.

## Compatibility

This script uses [rawpy](https://pypi.org/project/rawpy/) and
[numpy](https://numpy.org/) to read and process the raw images. To figure out
whether the script can support the raw file for your camera, check it out on 
rawpy [official website](https://pypi.org/project/rawpy/).

Since this project uses Type Hinting, a relatively new version of CPython is
recommended but other version might work too. I developed this in a CPython 3.9
environment.

## Aim

This script aims to perform 3 types of actions:

1. when you want to do a time-lapse with images that are too noisy. In this
case, you may use this script to do mean-stacking on the images. For example,
say you have 100 images with names from `DSC0001.NEF` to `DSC0100.NEF` and they
are too noisy, this script will stack a number of them together to reduce noise.
This reduces the number of images, and hence potentially the length of your
final videos, but may be helpful if your images are unacceptably noisy.

2. when you want to stack for one single image from a large number of images.
You may use PhotoShop for this, but it is not available on Linux which I heavily
use, and it may consume too much memory. This script attempts to achieve the
same thing with less resources (or at least do this in a (command-line only)
Linux environment, so that you can move this heavy work to a server and free the
resources on your PC).

3. by using an individual `*.csv` file containing `time`, `latitude` and
`longitude` data, add GPS data to the images. This can, and should be done on
`JPG` files because it is harder to deal with exif of raw images.

>Note that, because the RAW images contains un-debayered data, the debayer
>algorithm of choice may be different from those used by your favourite
>software. I will try to make this tunable, but before this, you may use your
>own software to do the debayering in batch and produce `.tiff` files which
>preserve a lot of details, and then use this script for stacking.

## Project Structure

```sh
modules/
        algo.py   // algorithms to call for the stacking.
        imageRW.py  // read and write the images.
```

## Dependencies
Executable: [exiftool](https://exiftool.org/) in your `$PATH`.  
Python PyPi dependencies can be found (and installed) in [requirements.txt](requirements.txt).
