import os
from PIL import Image
from os.path import splitext


def convertPngToJpg(in_image, outputPath):
    '''
    open file in folder "inputPath" one by one
    convert color channel
    save file as JPG format image in folder "outputPath"

    Input Parameters for the method:
    inputpath = the path of directory with input image files.
    outputPath = the path of directory where output image files should be stored.
    '''
    target = [".jpg", ".jpeg", ".png"]
    
    img = Image.open(in_image)
    img = img.convert("RGB")
    file = os.path.basename(in_image)
    print(file)
    filename, extension = splitext(file)
    print(filename)
    print(extension)
    try:
        if extension not in [target]:
            img.save(outputPath+filename+".jpg", quality=65, optimize=True)
    except OSError:
        print('Cannot convert %s' % in_image)

def get_all_file_paths(directory):

    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # returning all file paths
    print(file_paths)
    return file_paths

