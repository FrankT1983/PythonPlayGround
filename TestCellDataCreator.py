#!/usr/bin/python
from PIL import Image
import math
import datetime
from random import randint,shuffle
import sys


#O(n) but less random
def createImageSimple(width, height, name, cellpath,  cellcount):
    img = Image.new('RGB', (width, height))

    singleCell = Image.open(cellpath)
    singleCellHeight = singleCell.height
    singleCellWidth = singleCell.width
    singleCellRadius = int(math.sqrt(singleCellHeight*singleCellHeight+ singleCellWidth*singleCellWidth )/2) +10

    posiblePossitions = []

    for x in range(int(width / singleCellRadius)-1) :
        for y in range(int(height / singleCellRadius)-1):
            posiblePossitions.append((x,y))

    shuffle(posiblePossitions)
    for i in range(cellcount):
        x = int((posiblePossitions[i][0]*singleCellRadius)+singleCellRadius*0.5)
        y = int((posiblePossitions[i][1]*singleCellRadius)+singleCellRadius*0.5)
        singleCellRot = singleCell.rotate(randint(0, 360))
        img.paste(singleCellRot, (x, y))
    img.save(name)

# O(n^2) but more random
def createImage(width, height, name, cellpath, cellcount):
    img = Image.new('RGB', (width, height))

    singleCell = Image.open(cellpath)
    singleCellHeight = singleCell.height
    singleCellWidth = singleCell.width
    singleCellRadius = int(math.sqrt(singleCellHeight*singleCellHeight+ singleCellWidth*singleCellWidth )/2) +4

    positions = []
    maxTries = 1000

    for i in range(cellcount) :
        #print("Current " + str(i))
        num_try = 0
        while num_try < maxTries:
            min_range = width
            x = randint(40,width-40)
            y = randint(40, height - 40)

            center_x = int(x +singleCellWidth / 2)
            center_y = int(y + singleCellHeight / 2)

            for j in range(len(positions)):
                dist = int(math.sqrt( math.pow(positions[j][0]-center_x,2) + math.pow(positions[j][1]-center_y,2)))
                min_range =  min(dist,min_range)

            if (min_range < singleCellRadius*2) :
                num_try += 1
                #print('.', end='')
                continue

            singleCellRot = singleCell.rotate(randint(0, 360))

            img.paste(singleCellRot, (x,y))
            positions.append((center_x,center_y))
            break

#        if num_try is maxTries:
#            print("Could not fitt cell")
#        else:
#            print("created " + str(i) + " took " + str(num_try) + " tries")
    img.save(name)



# 12 Mega Pixel : Axiocam 512 color
width = 4048
height = 3040


# 6 Mega Pixel
width = 3008
height = 2008

# FD Math wants powers of two
#width = 2048
#height = 2048


start = 500
images = 100
basepath= 'c:/tmp/testData2/'

print(str(sys.argv))
if (len(sys.argv) > 3):
    start = int(sys.argv[1])
    images = int(sys.argv[2])
    basepath = sys.argv[3]




file = open("fileList","w")
file.close()
print(str(datetime.datetime.now()))
for x in range(start,start+images):
    x_tmp = str(x)
    filename = basepath + 'image' + x_tmp.zfill(5) + '.png'
    cellpath = basepath + 'SingleCellSquare2.png'
    cellCount = int(( (0.9946326 + 0.005373555*x - 0.000006169842*x*x + 2.23396e-9*x*x*x - 2.333781e-13*x*x*x*x)/7) *5000)  #12
    #cellCount = int(((0.9946326 + 0.005373555 * x - 0.000006169842 * x * x + 2.23396e-9 * x * x * x - 2.333781e-13 * x * x * x * x) / 7) * 3000)


    print(str(cellCount) + " : " + filename + "   ")
    createImageSimple(width,height,filename, cellpath , cellCount)

    file = open("fileList", "a")
    file.write(str(filename) + "\n")
    file.close()
    print(" done " + str(datetime.datetime.now()))

print(str(datetime.datetime.now()))