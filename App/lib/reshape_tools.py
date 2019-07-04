import cv2
from PIL import Image
import numpy as np

def removeWhitesFromBackground(img):
    '''
    Convert all white pixels to transparent

    input parameter is the image object
    '''
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    cv2.waitKey(0)
    img.save("temp.png", "PNG")

def maxWidthOfGrayObject(imgray):
    '''
    finding width of object for border identification
    finds an approx width of object in pixels

    input parameter is a binary/ grayscale image
    '''
    w = []
    x = []
    for i in range(imgray.shape[0]):
        xmin = [5000]
        datWid = []
        count = 0
        for j in range(imgray.shape[1]):
            if imgray[i][j] == 255:
                count = 0
                datWid.append(count)
            else:
                count = count + 1
                datWid.append(count)
                xmin.append(j)
        w.append(max(datWid))
        x.append(min(xmin))
    x = min(x)
    w = max(w)
    return x,w

def maxHeightOfGrayObject(imgray):
    '''
    finding height of object for border identification
    finds an approx height of the object in pixels

    input parameter is a binary/ grayscale image
    '''
    h = []
    y = []
    for j in range(imgray.shape[1]):
        datH = []
        ymin = [5000]
        count = 0
        for i in range(imgray.shape[0]):
            if imgray[i][j] == 255:
                count = 0
                datH.append(count)
            else:
                count = count+1
                datH.append(count)
                ymin.append(i)
        y.append(min(ymin))
        h.append(max(datH))
    y = min(y)
    h = max(h)
    return y, h

def trim(img):
    '''
    trim the image to minimal object border only
    
    input parameter is the image object itself, not path

    > find height and width of the object
    > crop image to almost object only
    > a max size for object is taken as 5000x5000 pixels
    '''
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x, w = maxWidthOfGrayObject(imgray)
    y, h = maxHeightOfGrayObject(imgray)

    trimmed_img = img[y:y+int(1.05*h), x:x+int(1.05*w)]
    return trimmed_img

def createCanvas(canvasHeight, canvasWidth, channels, aspectRatio=(1, 1), percentageMargin=0):
    '''
    Create a canvas as per specifications

    Parameters:
    Height and width for canvas
    number of color channels for image
    aspect ratio for canvas (default shape is square)
    margins to be added (default is zero margin)

    > determine a size for canvas
    > ressize as per given aspect ratio
    > compensate for margins
    > canvas created is white in color
    '''
    a, b = aspectRatio[:]
    if a > b:
        canvasWidth = int(canvasWidth*a/b)
    elif b > a:
        canvasHeight = int(canvasHeight*b/a)
    percentageMargin = (percentageMargin + 100)/100.00
    canvasWidth, canvasHeight = int(canvasWidth*percentageMargin), int(canvasHeight*percentageMargin)
    square = 255 * np.ones(shape=[canvasHeight, canvasWidth, channels], dtype=np.uint8)
    return square

def pasteImageOnCanvas(canvas, imageToPaste, channels):
    '''
    Paste image on canvas(or another image) at a centered position

    Parameters: 
    canvas and imageToPaste are object of image type
    channles: number  of color channels for image 
    '''
    canvasHeight, canvasWidth = canvas.shape[:2]
    imageHeight, imageWidth = imageToPaste.shape[:2]
    canvas[int((canvasHeight-imageHeight)/2):int((canvasHeight+imageHeight)/2), 
    int((canvasWidth-imageWidth)/2):int((canvasWidth+imageWidth)/2)] = imageToPaste
    if channels==4:  
        canvas[:, :, 3] = 255

def reshape_Image(in_image, out_image, trimOrNot=False, aspectRatio=(1, 1), percentageMargin=0):
    '''
    An image can be reshaped to square or any aspect ratio with specified margins
    
    Parameters:
    in_image: file path for input image as string
    out_image: file path for output image as string
    trimOrNot: True/False choice, to trim object to zero margins or not
    aspectRatio: tuple of integer values -> format(width, height) ratio
    margins: input as percentage over object size

    No return data, the output is saved at specified location
    
    (a temp file is saved and required for faster processing like object border
    identificationand image data passing)

    > Read image and trim excess parts
    > create canvas for reshaping
    > Pasting image over canvas
    '''
    image = Image.open(in_image).convert("RGBA")
    
    if(trimOrNot):
        removeWhitesFromBackground(image)
        img1 = cv2.imread("temp.png", -1)
        imgToPaste = trim(img1)
    else:
        imgToPaste = image
    height, width, channels= imgToPaste.shape

    canvasWidth = height if height > width else width
    canvasHeight = height if height > width else width

    canvas = createCanvas(canvasHeight, canvasWidth, channels, aspectRatio, percentageMargin)
    pasteImageOnCanvas(canvas, imgToPaste, channels)
    cv2.imwrite(out_image, canvas)

def addMargins(in_image, out_image, percentageMargin=0, marginPixels=0):
    '''
    Add margin or frame to an image:
    Margins size can be given as percentage over image size, or in Pixels

    Parameters:
    in_image: file path for input image as string
    out_image: file path for output image as string
    percentageMargin: size of margin given as percentage over image size
    marginPixels: margin size given in pixels
    (any one size of margin to be provided, when both are given then the larger is used)

    > Read Image from path
    > determine margin size from inputs,
    > create a canvas with appropriate dimensions
    > Paste image over canvas
    '''
    image = cv2.imread(in_image)
    height, width, channels = image.shape

    margin_on_height = int(percentageMargin*height/100)
    margin_on_width = int(percentageMargin*width/100)

    if marginPixels > margin_on_height and marginPixels > margin_on_width:
        margin_on_height = marginPixels
        margin_on_width = marginPixels

    canvas = createCanvas(height+margin_on_height, width+margin_on_width, channels, (width, height))
    pasteImageOnCanvas(canvas, image, channels)
    cv2.imwrite(out_image, canvas)
    
def resizeImage(in_image, out_image, scale_percent, scaledSizeInPixels):
    '''
    Resize any image, making it bigger, smaller, or changing dimensions specifically

    Parameters:
    in_image: file path for input image as string
    out_image: file path for output image as string
    scale_percent: scaling size given as percentage over original size of image
    like 200 makes 2x bigger, 50 makes half the size
    scaledSizeInPixels: dimensions for scaling given in pixels
    format for dimensions => (width,height) input as tuple

    (any one scaling input to be given, when both are provided then the larger is used)
    
    > Read image from paths
    > Determine rescaling dimensions
    > Resizing the image to new dimensions 
    '''
    img = cv2.imread(in_image)
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    if ((dim[0] < scaledSizeInPixels[0]) and (dim[1] < scaledSizeInPixels[1])):
        dim = scaledSizeInPixels
    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    
    print('Resized Dimensions : ', resized.shape)
    cv2.imwrite(out_image, resized)
