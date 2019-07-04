import os
import time
import cv2
import numpy as np

def extractDimension(imageList, same=False, count=0):
    '''
    find dimensions of images and make list of them

    Parameters:
    imageList: list containing image object as numpy arrays
    same: boolean for repeating same image for montage
        (when true same dimensions are set for as many times as "count")
    count: number of repetitions for same image on montage

    '''
    height, width = [], []
    if same == 1:
        while len(imageList) != 1:
            imageList.pop()
        for i in range(count-1):
            imageList.append(imageList[0])
    for i in imageList:
        height.append(i.shape[0])
        width.append(i.shape[1])
    return height, width

def png_with_white(arr):
    '''
    Convert all transparent pixels to white for result

    Parameter:
    arr: numpy array for image object

    > select pixels with alpha value zero,
    > set color to white and alpha value to full
    '''
    arr[arr[:, :, 3] == 0] = 255
    return arr

def createCanvasForSize(canvasHeight, canvasWidth, channels):
    '''
    create a white canvas for given dimensions

    Parameters:
    canvasHeight, canvasWidth: dimensions for canvas in Pixels
    channels: number of color channels for image
    (eg: 3 for RGB,BGR ; 4 for RGBA,BGRA,HSVA etc.)
    '''
    canvas = 255 * np.ones(shape=[canvasHeight, canvasWidth, channels], dtype=np.uint8)
    return canvas

def pasteImageOnCanvas(canvas, imageToPaste, channels):
    '''
    Paste image on canvas(or another image) at a centered position

    Parameters: 
    canvas and imageToPaste are object of image type
    channles: number  of color channels for image 
    '''
    canvasHeight, canvasWidth = canvas.shape[:2]
    imageHeight, imageWidth = imageToPaste.shape[:2]
    imageToPaste = cv2.cvtColor(imageToPaste, cv2.COLOR_BGR2BGRA)
    canvas[int((canvasHeight-imageHeight)/2):int((canvasHeight+imageHeight)/2), 
    int((canvasWidth-imageWidth)/2):int((canvasWidth+imageWidth)/2)] = imageToPaste
    if channels==4:  
        canvas[:, :, 3] = 255
    return canvas

def makeImagesSameSize(images):
    '''
    Make all images same size for montage preparation

    Parameters:
    images: list containing image objects as numpy arrays

    > make a list for all heights and widths of images
    > select maximum of them as standard
    > make canvas of standard size, paste each image on a canvas
    > no return, input object is tranformed
    '''
    height, width = extractDimension(images)
    canvasHeight = max(height)
    canvasWidth = max(width)
    for i in range(len(images)):
        canvas = createCanvasForSize(canvasHeight, canvasWidth, 4)
        images[i] = pasteImageOnCanvas(canvas, images[i], 4)

def LinearHorizontalStackMultipleImages(images, overlap, same, count):
    '''
    Make a linear combo of images as horizontal stack

    Parameters:
    images: list of image object as numpy arrays
    overlap: overlap for images in percentage
    same: boolean choice for repeating same image over and over
    count: number of repitition for same image

    > make all images same size
    > create a canvas by size for images and overlap
    > paste images on canvas in horizontal stack order
    > return a horizontal stack combo of images as image object
    '''
    makeImagesSameSize(images)
    height,width = extractDimension(images, same, count)
    canvasHeight = max(height)
    canvasWidth = sum(width) - int(overlap*(sum(width[1:])))

    result = np.zeros((canvasHeight, canvasWidth, 4), np.uint8)
    result[0:height[0], 0:width[0], :] = images[0]
    cursorYAxis=0

    for i in range(1, len(images)):
        cursorYAxis += width[i-1]
        cursorYAxis = int(cursorYAxis - overlap*width[i])
        heightImg, widthImg = images[i].shape[:2]
        idx = int((height[i]-heightImg)/2)
        for a in range(0, heightImg):
            for b in range(0, widthImg):
                if not images[i][a, b, 2] == 0:
                    result[a+idx, b+cursorYAxis, :] = images[i][a, b, :]
    return result

def LinearVerticalStackMultipleImages(images, overlap, same, count):
    '''
    Make a linear combo of images as vertical stack

    Parameters:
    images: list of image object as numpy arrays
    overlap: overlap for images in percentage
    same: boolean choice for repeating same image over and over
    count: number of repitition for same image

    > make all images same size
    > create a canvas by size for images and overlap
    > paste images on canvas in vertical stack order
    > return a vertical stack of images as image object
    '''
    makeImagesSameSize(images)
    height, width = extractDimension(images, same, count)
    canvasWidth = max(width)
    canvasHeight = sum(height) - int(overlap*(sum(height[1:])))

    result = np.zeros((canvasHeight, canvasWidth, 4), np.uint8)
    result[0:height[0], 0:width[0], :] = images[0]
    cursorXAxis = 0

    for i in range(1, len(images)):
        cursorXAxis += height[i-1]
        cursorXAxis = int(cursorXAxis - overlap*height[i])
        heightImg, widthImg = images[i].shape[:2]
        idx = int((width[i]-widthImg)/2)
        for a in range(0, heightImg):
            for b in range(0, widthImg):
                if not images[i][a, b, 2] == 0:
                    result[a+cursorXAxis, b+idx, :] = images[i][a, b, :] 
    return result

def comboGridRepeatedImage(images, gridx, gridy):
    ''' creating a grid of same image repeated as per input grid size
    
    Parameters:
    images: list of image objects as numpy arrays
    gridx: number of images on width of grid
    gridy: number of image on height of grid

    > create rows and columns as arrays from the list of images
    > concatenate/join images in rows for grid
    > concatenate/join rows to form grid
    > return a grid montage of repeated images as image object

    # when grid size product is less than total number of images
        then first images are used
    # when gird size product is more than the total number of images
        exception is thrown and just prints error on terminal
    '''
    row = []
    col = []
    try:
        for i in range(gridx):
            row.append(images[0])
        rowImg = np.hstack(row)
        for i in range(gridy):
            col.append(rowImg)
        result = np.vstack(col)
        return result
    except:
        print("grid size given more than the number of images fed")

def comboGridOfDifferentImages(images, gridx, gridy):
    ''' creating a grid of images as per input grid size
    
    Parameters:
    images: list of image objects as numpy arrays
    gridx: number of images on width of grid
    gridy: number of image on height of grid

    > create rows and columns as arrays from the list of images
    > concatenate/join images in rows for grid
    > concatenate/join rows to form grid
    > return grid montage of different images as image object

    # when grid size product is less than total number of images
        then first images are used
    # when gird size product is more than the total number of images
        exception is thrown and just prints error on terminal
    '''
    row = []
    col = []
    imgCount = 0
    makeImagesSameSize(images)
    try:
        for i in range(gridy):
            for j in range(gridx):
                row.append(images[imgCount])
                imgCount += 1
            rowImg = np.hstack(row)
            col.append(rowImg)
            row = []
        result = np.vstack(col)
        return result
    except:
        print("grid size given more than the number of images fed")

def comboLinearStack(images, overlap=0, direction="horizontal", sameImgRepeat=False, count=0):
    '''
    Create a linear stack combo of images with options like direction, overlap, repeat

    Parameters:
    images: list of image objects as numpy arrays
    overlap: ovaerlap of image in percentage (default is 0)
    direction: specify as string: "horizontal"/"vertical" 
        (default selection is "horiontal")
    sameImgRepeat: boolean choice to repeat same image over the combo or not
        (default false)
    count: number of repitition for same image default(zero)

    > convert overlap to fraction
    > decide stack type from direction
    > create stack as per direction 
    > return linear combo of images

    # any other input on direction than specified shall throw an exception
    # when repeat set to False, count input is unused
    '''
    overlap = (overlap/100.0)
    try:
        if direction == "horizontal":
            result = LinearHorizontalStackMultipleImages(images, overlap, sameImgRepeat, count)
        elif direction == "vertical":
            result = LinearVerticalStackMultipleImages(images, overlap, sameImgRepeat, count)
        return result
    except:
        print("invalid direction input")

def comboGrid(images, sameImgRepeat=False, gridx=1, gridy=1):
    '''
    Create a grid combo of images as per size specified

    Parameters:
    images: list of image objects as numpy arrays
    sameImgRepeat: boolean choice for repeating the same image over grid
    gridx: number of images on width of grid
    gridy: number of image on height of grid

    > whether image is to be same or different
    > create grid of repeated or different images
    > return grid combo of images as image object
    '''
    if sameImgRepeat == True:
        result = comboGridRepeatedImage(images, gridx, gridy)
    else:
        result = comboGridOfDifferentImages(images, gridx, gridy)
    return result

def createCombo(in_path, out_path, comboType, overlap=0, direction="horizontal", repeatImage=False,
                repeatCount=0, numberOfImagesXaxis=0, numberOfImagesYaxis=0):
    #designing combo of images from as per data in csv file
    '''
    Create different types of combos and montages from product images
    like stacks and custom sized grids
    Parameters:
        1. in-path: input directory with input image(s)
        2. out_path: output directory for saving output combo image
        3. comboType: combo type : integer choice from
        4. overlap(float): overlap of images in percentage
        5. horizontal(boolean): direction for stacking horizontal/vertical
        6. repeatImage: boolean choice for repeating same image on grid/stack or use
            multiple input images
        7. repeatCount: count for no of repetitions
        8. numberOfImagesXaxis: x-dimension for size of grid (width in no of images)
        9. numberOfImagesYaxis: y-dimension for size of grid (height in no of images)

    > set current working dir path to input folder
    > open all images and make a list of image object to pass to combo methods
    > decide combo method as per given type parameter from linear/grid
    > save the created combo at out_path location

    # input of comboType other than specified throws an exception
    # input folder may contain other files, only images of type
        PNG, JPG, JPEG, GIf are accepted, others discarded
    '''
    start = time.time()
    folder = os.listdir(in_path)
    files = []
    for file in folder:
        filename, extension = os.path.splitext(file)
        if extension not in ["png","jpg","jpeg","gif"]:
            image = cv2.imread(in_path+'/'+file, -1)
            files.append(image)
        else:
            continue
    try:
        if comboType == "linear":
            result = comboLinearStack(files, overlap, direction, repeatImage, repeatCount)
        elif comboType == "grid":
            result = comboGrid(files, repeatImage, numberOfImagesXaxis, numberOfImagesYaxis)
        
        cv2.imwrite(out_path +'/output.png', result)
        end = time.time()
        print(end - start)
    except:
        print("invalid input")
    return 0

