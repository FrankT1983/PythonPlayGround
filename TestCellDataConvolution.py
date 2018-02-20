#!/usr/bin/python
from PIL import Image
from subprocess import call
import os
import shutil
import sys
import tempfile


def saveToTemp(img, name, tmpFolder) :
    filepath = tmpFolder + name + ".tif"
    img.save(filepath)
    return filepath


def runConvolution(img , algo, toolpath, psfPath, name, outpath , outpath2) :
    print(name)

    tempdir = tempfile.mkdtemp()

    filepath = saveToTemp(img, name, tempdir)

    command = "java -jar " + toolpath + " run -image file " + filepath + " -psf file " + psfPath + " -algorithm "+ algo +" -out series pref -display no -path " + outpath + " -monitor console"
    print(str(command))
    call(command, shell=True)

    if len(os.listdir(outpath)) < 1 :
        return None


    outfile = outpath + "/"+ os.listdir(outpath)[0]
    destinationFile = outpath2 +  "/" + name + ".tif"
    shutil.copy2(outfile, destinationFile)

    #os.remove(outfile)
    os.remove(filepath)
    shutil.rmtree(tempdir)

    return destinationFile


def splitAndRunAlgo(img, algorithm,toolpath, psfPath, splitDest, processedDest, finalDest, resultname) :
    r, g, b = img.split()
    rFile = runConvolution(r,algorithm,toolpath, psfPath, "red" , splitDest, processedDest,)
    gFile = runConvolution(g,algorithm,toolpath, psfPath, "green" , splitDest, processedDest,)
    bFile = runConvolution(b,algorithm,toolpath, psfPath, "blue" , splitDest, processedDest,)

    rconf = Image.open(rFile).convert('L')
    gconf = Image.open(gFile).convert('L')
    bconf = Image.open(bFile).convert('L')

    res = Image.merge("RGB", (rconf,gconf,bconf))

    resultPath = finalDest + resultname
    res.save(resultPath)
    return resultPath







start = 0
images = 10
basepath= 'C:/Tmp/deconv/'
toolpath= 'C:/PHD/UnitTest/DeconvolutionLab2custom.jar'
psfpath= 'C:/PHD/Git/omero-parallel-processing/Writing/Data/PsfForApplication.tif'

print(str(sys.argv))
if (len(sys.argv) > 5):
    start = int(sys.argv[1])
    images = int(sys.argv[2])
    basepath = sys.argv[3]
    toolpath = sys.argv[4]
    psfpath = sys.argv[5]




for x in range(start,start+images):
    fileName = 'image' + str(x).zfill(5) + '.png'
    curImg = Image.open(basepath + fileName)
    result = splitAndRunAlgo(curImg,"CONV", toolpath, psfpath, basepath+ "output" , basepath+ "output2" , basepath+ "output3/" , "conv"+fileName )

    del curImg
    os.remove(basepath + fileName)



#    print("\n-------------------------Reverse-------------------------\n")
#    convImg = Image.open(result)
#    result = splitAndRunAlgo(curImg, "RLTV 10 0,1000", "C:/Tmp/deconv/output4", "C:/Tmp/deconv/output5", "C:/Tmp/deconv/output6/" , "reconst" + fileName)
#    quit(0)




