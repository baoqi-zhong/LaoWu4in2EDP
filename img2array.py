from PIL import Image

img = Image.open('./image/testImage.jpg')
outImg = img.convert('L')

for y in range(outImg.size[1]):
    for x in range(outImg.size[0]):
        if outImg.getpixel((x, y)) > 128:
            err = outImg.getpixel((x, y)) - 255
            outImg.putpixel((x, y), 255)
        else:
            err = outImg.getpixel((x, y))
            outImg.putpixel((x, y), 0)
        
        a = int(err * 7/16)
        b = int(err * 1/16)
        c = int(err * 5/16)
        d = int(err * 3/16)

        if (x != outImg.size[0] - 1) and (y != outImg.size[1] - 1) and (x != 0):
            outImg.putpixel((x + 1, y), (min(outImg.getpixel((x + 1, y)) + a, 255)))
            outImg.putpixel((x - 1, y + 1), (min(outImg.getpixel((x - 1, y + 1)) + b, 255)))
            outImg.putpixel((x, y + 1), (min(outImg.getpixel((x, y + 1)) + c, 255)))
            outImg.putpixel((x + 1, y + 1), (min(outImg.getpixel((x + 1, y + 1)) + d, 255)))

result = """#include "imagedata.h"
#include <avr/pgmspace.h>

const unsigned char IMAGE_BLACK[] PROGMEM = {"""

for y in range(outImg.size[1]):
    for x in range(outImg.size[0] // 8):
        temp = 0
        for i in range(8):
            temp <<= 1
            if outImg.getpixel((x * 8 + i, y)) > 128:
                temp += 1
            
        result += "0x"+hex(temp)[2:].rjust(2, "0").upper() + ", "
    result += "\n"

result += "};"
open("imagedata.cpp", "w").write(result)
