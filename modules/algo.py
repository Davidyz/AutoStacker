import numpy as np

from modules.imageRW import Image
from typing import Iterable, Optional
from __future__ import annotations

class InputException(Exception):
    pass

def mean(images: Iterable[Image], group_size: int = None) -> Image:
    total = None
    for i in images:
        if total:
            total += i / group_size
        else:
            total = np.zeros(i.shape, dtype=np.uint32).view(Image)
            total += i.copy() / group_size
            total.setExif(i.exif)
    
    if total != None:
        return total
    raise InputException("The first parameter is an empty iterator.")

def maxBright(images: Iterable[Image]) -> Image:
    maxArray: Optional[Image] = None
    for i in images:
        if isinstance(maxArray, Image):
            maxArray = np.array(np.maximum(maxArray, i)).view(Image)
            maxArray.loadExif()
        else:
            maxArray = i.copy()

    if maxArray != None:
        return maxArray
    raise InputException("The first parameter is an empty iterator.")

def mode(images: Iterable[Image]) -> Image:
    modeArray: Optional[Image] | None = None
    return modeArray

if __name__ == '__main__':
    pass
