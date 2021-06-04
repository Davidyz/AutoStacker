import numpy as np

from modules.imageRW import Image
from typing import Iterator, Optional, List
from __future__ import annotations

class InputException(Exception):
    pass

def mean(images: Iterator[Image], group_size: int) -> Iterator[Image|None]:
    stackImage: Image|None = None
    while True:
        try:
            i = next(images)
            for j in range(group_size):
                if stackImage:
                    stackImage += i / group_size
                else:
                    stackImage = np.zeros(i.shape, dtype=np.uint32).view(Image)
                    stackImage += i.copy() / group_size
                    stackImage.setExif(i.exif)
            yield stackImage
            stackImage = None
        except StopIteration:
            break

def maxBright(images: Iterator[Image], group_size: int) -> Iterator[Image|None]:
    stackImage: Image|None = None

    while True:
        try:
            i = next(images)
            for j in range(group_size):
                if stackImage:
                    stackImage = np.array(np.maximum(stackImage, i)).view(Image)
                else:
                    stackImage = np.zeros(i.shape, dtype=np.uint32).view(Image)
                    stackImage = np.array(np.maximum(stackImage, i)).view(Image)
                    stackImage.setExif(i.exif)
            yield stackImage
            stackImage = None
        except StopIteration:
            break

def mode(images: Iterator[Image]) -> List[Image]:
    modeArray = []
    return modeArray

ALGORITHMS = {'mean': mean,
              'max': maxBright}

if __name__ == '__main__':
    pass
