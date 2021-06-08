import exiftool, os
from typing import Dict, Iterable, Optional, List, Union, Iterator
from modules.imageRW import Image

GPS_SUFFIX = ['csv']

def findGPSTrack(directory: str) -> Union[str, None]:
    for i in os.listdir(directory):
        if i.split('.')[-1] in GPS_SUFFIX:
            return os.path.join(directory, i)
    return None

def readCSV(path:str) -> dict:
    with open(path, 'r') as fin:
        data = {}
        count = 0
        headings = []
        for i in fin.readlines():
            if count:
                entry = i.replace('\n', '').split(',')
                for j in range(3):
                    data[headings[j]].append(entry[j])
            else:
                headings = i.replace('\n', '').split(',')
                for j in headings:
                    data[j] = []
                count += 1
        return data

def parseHeading(headings: List[str]) -> List[int]:
    '''
    Return the index of the columns in this order: latitude, longitude, time
    '''
    if 'lat' in headings[0].lower():
        if 'lon' in headings[1].lower():
            return [0, 1, 2]
        return [0, 2, 1]
    elif 'lon' in headings[0].lower():
        if 'lat' in headings[1].lower():
            return [1, 0, 2]
        return [1, 2, 0]
    elif 'lat' in headings[1].lower():
        return [2, 0, 1]
    return [2, 1, 0]

def getTrack(filePath: str) -> Dict[str, list]:
    ''' 
    Take the path to a csv file as input and return a dictionary of lists with keys: latitude, longitude and time.
    '''
    data = {'lat': [],
            'long': [],
            'time': []}
    if os.path.isfile(filePath) and filePath.split('.')[-1] == 'csv':
        reader = readCSV(filePath)
        lat_index: Optional[int] = None
        long_index: Optional[int] = None
        time_index: Optional[int] = None

        for entry in reader:
            if lat_index == None:
                lat_index, long_index, time_index = parseHeading(entry)
            else:
                data.get('lat').append(float(entry[lat_index]))
                data.get('long').append(float(entry[long_index]))
                data.get('time').append(entry[time_index])
    else:
        raise IOError("The input file is not a valid GPS track.")
    return data

def setGPS(gpsTrack: dict, iterImages: Iterator[Image]) -> Iterator[Image]:
    '''
    Add GPS data to the images.
    iterGPS is the iterator from getTrack().
    iterImages is an iterable of paths to images.
    '''

if __name__ == '__main__':
    pass
