import os, rawpy, exif, imageio, subprocess
import numpy as np
from typing import Iterator
from __future__ import annotations

class Image(np.ndarray):
    def __new__(cls, array: np.ndarray, meta=None, path=None) -> Image:
        self = array.view(Image, dtype=array.dtype)
        self.__exif = meta
        self.__path = path  # should be the path to the image.
        self.source = []    # record the source images of a stacked image. useful when copying exif data.
        return self

    @property
    def path(self) -> str:
        return self.__path

    @property
    def exif(self) -> dict:
        if not self.__exif:
            self.loadExif()
        return self.__exif

    def setPath(self, path):
        self.__path = path

    def setExif(self, meta):
        self.__exif = meta

    def write(self, path=None):
        if path or self.__path:
            if self.__path == '':
                self.__path = path
            imageio.imsave(self.__path, self.view(np.ndarray))

    def loadExif(self) -> dict:
        if self.__path and os.path.isfile(self.__path):
            rawExif = subprocess.check_output(['exiftool', self.__path]).decode().split('\n')
            data = {}
            for i in rawExif:
                key = i.split(':')[0].rstrip().lstrip()
                value = ':'.join(i.split(':')[1:]).rstrip().lstrip()
                if value == '':
                    continue
                if value[-1] == ',':
                    value = value[:-1]
                data[key] = value
            return data
        else:
            raise TypeError("This file does not contain valid exif.")

    def copy(self) -> Image:
        new_image = Image(self.view(np.ndarray))
        new_image.setExif(self.exif)
        return new_image

def getBits(path: str) -> int:
    rawExif = subprocess.check_output(['exiftool', path]).decode().split('\n')
    data = {}
    for i in rawExif:
        key = i.split(':')[0].rstrip().lstrip()
        value = ':'.join(i.split(':')[1:]).rstrip().lstrip()
        if value == '':
            continue
        if value[-1] == ',':
            value = value[:-1]
        data[key] = value

    bits = data.get("Bits Per Sample")
    if bits != None:
        return int(''.join([i for i in bits if i in '1234567890']))
    raise TypeError("The file does not have a \"Bits Per sample\" tag.")

def read(path: str, lazy: bool = True) -> Iterator[Image]:
    '''
    A generator that read files from the given path.
    The use of generators prevent loading too much files into the memory.
    lazy: if True, the generator will delete the img object after it's processed. If False, be careful with memory management.
    '''
    files = [os.path.sep.join([path, i]) for i in os.listdir(path)]
    files.sort()
    for i in files:
        with rawpy.imread(i) as raw:
            img = raw.postprocess(output_bps=16).view(Image)
            img.setPath(i)
            img.loadExif()
            yield img
            if lazy:
                del img     # this line will not be executed until the iteration goes into the next loop.

if __name__ == '__main__':
    pass
