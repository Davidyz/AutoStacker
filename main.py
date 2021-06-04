from modules import algo, imageRW, gps
import sys, os
from typing import List, Optional, Union


class ArgumentError(Exception):
    pass

def parseArgs(args: List[str], config: dict[str, Union[str, int, None]] = {'source':None, 'target': None, 'group-size': 1, 'mode': 'mean'}) -> Optional[dict]:
    '''
    parse the command line arguments:
    -s: specify the source directory of the images. this directory may contain images and a gps track file.
    -t: specify the name of output directory or file.
    -group-size (-gs): specify the number of images per stack. if not specified, all photos are merged into one stack.
    -mode (-m): specify the mode of stacking. has to be one of 'mean', 'max'.
    -track: specify a gps track that is not in the source directory.
    '''
    if args == []:
        for i in config.keys():
            if config.get(i) == None:
                raise ArgumentError("Please check the command line arguments.")
        return config
    elif args[0] == '-h':
        # print help messages
        pass
    elif args[0] == '-s':
        if os.path.isdir(args[1]):
            config['source'] = args[1]
            return parseArgs(args[2:], config)
        else:
            raise ArgumentError("The source directory does not exist.")
    elif args[0] == '-t':
        if os.path.isdir(args[1]) or args[1].split('.')[-1].lower() in imageRW.SUFFIX:
            config['target'] = args[1]
            return parseArgs(args[2:], config)
        else:
            raise ArgumentError("The target has to be an existing directory or a file name with suffix jpg or tiff.")
    elif args[0] in ('-group-size', '-gs'):
        try:
            config['group-size'] = int(args[1])
            return parseArgs(args[2:], config)
        except Exception:
            print("Invalid input for group size. Please check your input.")
            sys.exit()
    elif args[0] in ('-mode', 'm'):
        if args[1] in algo.ALGORITHMS.keys():
            config['mode'] = args[1]
            return parseArgs(args[2:], config)
        else:
            raise ArgumentError("The stacking mode is not supported.")
    elif args[0] == '-track':
        if args[1].split('.')[-1] in gps.GPS_SUFFIX:
            config['gpsFile'] = args[1]
            return parseArgs(args[2:], config)
    else:
        raise ArgumentError("Cannot recognize the input {}.".format(args[0]))

def main():
    config: Optional[dict] = parseArgs(sys.argv[1:])
    if config.get('gpsFile') == None:
        config['gpsFile'] = gps.findGPSTrack(config['source'])
    
    if imageRW.countImage(config['source']) % int(config['group_size']):
        print("Warning: The group size is not a factor of the total number of images. The quality of the last image might be affected.")

    sourceGen = imageRW.read(config['source'])
    targetGen = algo.ALGORITHMS[config['mode']](sourceGen, config['group_size'])
    for image in targetGen:
        image.setPath(os.path.join(config['target'], ))     # need to work out the new image names.
        image.write()
if __name__ == '__main__':
    pass
