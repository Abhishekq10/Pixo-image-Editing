from PIL import Image, ImageDraw, ImageFont


def positionMarker(image, draw, text, font, position):
    '''
    determine positioning for text for writing

    Paramteres:
    image: PIL image object
    draw: PIL imageDraw object of same size as image
    text: text to be written on image as watermark (given as string)
    font: freeFontType object for font
    position: position for placing (given as string)
    '''
    textwidth, textheight = draw.textsize(text, font)
    width, height = image.size
    margin = 5
    try:
        if position == "top-left":
            x = margin
            y = margin
        elif position == "top-right":
            x = width - textwidth - margin
            y = margin
        elif position == "bottom-left":
            x = margin
            y = height - textheight - margin
        elif position == "bottom-right":
            x = width - textwidth - margin
            y = height - textheight - margin
        elif position == "center":
            x = int((width - textwidth)/2)
            y = int((height - textheight)/2)
    except:
        print("invalid object input or position specified")
    return x, y

def alphaValueAdder(colorOfText, alpha):
    '''
    change the alpha channel value from 0-1 range to 0-255 range

    Parameters:
    colorOfText: RGBA value of color in tuple
    alpha: alpha value/ transparency in percentage
    '''
    colorOfText = list(colorOfText)
    alpha = int(alpha*255/100)
    colorOfText.append(alpha)
    colorOfText = tuple(colorOfText)
    return colorOfText

def hex_to_rgb(value):
    '''convert color code from hex to RGB
    input is hex string
    return value is RGB tuple
    '''
    value = value.lstrip('#')
    length = len(value)
    return tuple(int(value[i:i + length // 3], 16) for i in range(0, length, length // 3))

def watermarker(in_image, out_image, text, fontface="arial", fontSize=50,
                colorOfText=(255, 255, 255), opacity=50, position="center"):
    '''
    Create a watermark of text of any color and transparency over an image

    Parameters:
    in_image: path of input image
    out_image: path where output is saved
    text: the text to be written on image as watermark
    fontFace: font design to be set for watermark
        1. arial
        2. impact
        3. verdana
    fontSize: size for font of text (default is 50 Pixels)
    colorOfText: color for text in RGB format
    opacity: opacity level for text (default is white with 50% alpha)
    position: positioning of text over image, from
        1. top-left
        2. top-right
        3. center
        4. bottom-left
        5. bottom-right
        (default is center)
    > Read image and create a editable transparent canvas of similar size
    > determine starting pixel position for text
    > placing text on canvas
    > combining images for watermarked result
    '''
    image = Image.open(in_image).convert("RGBA")
    font = ImageFont.truetype(fontface+".ttf", fontSize)
    txt = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)

    startX, startY = positionMarker(image, draw, text, font, position)
    colorOfText = alphaValueAdder(colorOfText, opacity)

    draw.text((startX, startY), text, fill=colorOfText, font=font)
    combined = Image.alpha_composite(image, txt)
    combined = combined.convert("RGB")
    combined.save(out_image)
