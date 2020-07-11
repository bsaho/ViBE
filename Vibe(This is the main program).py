import numpy as np
import os
import random
from os import listdir
from os.path import isfile, join
import glob
from  matplotlib import pyplot as plt
import fastrand
import time
import math

import cv2
import argparse
import os

sampleCount=20
minMatches=2
distanceThreshold =20
subSamplingFactor=5
choices =[-1,1]
threshold_squared =distanceThreshold **2



def delAll():
    os.system(
        'del C:\\Users\\Desktop\\dataset2014\\dataset\\badWeather\\blizzard\\stats.txt')
    os.system(
        'del C:\\Users\\\\Desktop\\dataset2014\\dataset\\baseline\\highway\\stats.txt')
    os.system(
        'del C:\\Users\\\\Desktop\\dataset2014\\dataset\\cameraJitter\\badminton\\stats.txt')
    os.system(
        'del C:\\Users\\\\Desktop\\dataset2014\\dataset\\dynamicBackground\\boats\\stats.txt')
    os.system('del C:\\Users\\\\Desktop\\dataset2014\\dataset\\intermittentObjectMotion\\abandonedBox\\stats.txt')
    os.system(
        'del C:\\Users\\\\Desktop\\dataset2014\\dataset\\lowFramerate\\port_0_17fps\\stats.txt')
    os.system(
        'del C:\\Users\\\\Desktop\\dataset2014\\dataset\\nightVideos\\bridgeEntry\\stats.txt')
    os.system(
        'del C:\\Users\\\\Desktop\\dataset2014\\dataset\\PTZ\\continuousPan\\stats.txt')
    os.system(
        'del C:\\Users\\\\Desktop\\dataset2014\\dataset\\shadow\\backdoor\\stats.txt')
    os.system(
        'del C:\\Users\\\\Desktop\\dataset2014\\dataset\\thermal\\corridor\\stats.txt')
    os.system(
        'del C:\\Users\\\\Desktop\\dataset2014\\dataset\\turbulence\\turbulence0\\stats.txt')



def initBackground (img, sampleCount):
    sampleArray= np.zeros ((img.shape[0],img.shape[1],sampleCount), np.int32)
    choices = [-1,1,0]
    # choices = [2,-2,1,-1,0,3,-3]

    for i in range (0,img.shape [0]-1):
        # print (i)
        for j in range (0,img.shape[1]-1):
            # print (j)
            for k in range (0,sampleCount):
                # print (k)
                randNums=random.choices (choices,k=2)
                while randNums[0]==0 and randNums[1]==0:
                    randNums=random.choices (choices,k=2)


                # rand_noise= img[i][j]+ (fastrand.pcg32bounded(20)) - 10
                # sampleArray[i][j][k]=rand_noise
                sampleArray[i][j][k]= img[(i+randNums[0])][j+randNums[1]]

    return sampleArray

def updateWithVibe (img, sampleArray, distanceThreshold, sampleCount):
    segmentationMap =np.copy (segTemplate)
    # print (img.shape)
    # print (img.shape)

    start = time.time()
    for i in range (0,(img.shape[0]-1)):
        start = time.time()
        for j in range (0,(img.shape[1]-1)):
            count=0
            index=0
            distance=0


            start6=time.time ()
            while ( ( count < minMatches ) and ( index < sampleCount ) ):
                # print (img[i][j])
                distance=0

                # if len (img[i][j])==3:
                #     distance = math.sqrt ((img[i][j][0]-sampleArray[i][j][index][0])**2+(img[i][j][1]-sampleArray[i][j][index][1])**2+(img[i][j][2]-sampleArray[i][j][index][2])**2)
                # else:
                start2 = time.time()
                distance =  ((img[i][j] - sampleArray[i][j][index]))** 2
                end2= time.time ()
                # print ("\t\tTime for each distane calc " + str (end2 - start2))

                # print (distance)
                if (distance < threshold_squared ):
                    count+=1

                index+=1
               
            end6=time.time ()
            # print ("Time for each while loop " + str (end6-start6))
            if count < minMatches:
                segmentationMap [i][j]= 255
        #         segmentationMap[i]=BACKGROUND_PIXEL
            else:
                start3 = time.time()
                randNum= fastrand.pcg32bounded(subSamplingFactor) 
                end3= time.time ()
                # print ("\t\tTime for each random generation " + str (end3 - start3))

                if randNum==0:
                    randNum=fastrand.pcg32bounded(sampleCount)
                    sampleArray[i][j][randNum]=img[i][j]
                randNum= fastrand.pcg32bounded(subSamplingFactor)
                if randNum==0:
                    randNum=random.choice ([-1,1])
                    sampleArray[(i+randNum)][(j+randNum)][randNum]=img[i][j]
        end= time.time ()
        # print ("\tTime for each height loop " + str (end - start))


            
    return segmentationMap, sampleArray


start = time.time()


# folderNames= ["continuousPan"]
folderNames=os.listdir("C:/Users//Desktop/Image Project/sample_cdnet")
print (folderNames)
try:
    folderNames.remove ('.tmp.drivedownload')
except:
    pass
print (folderNames)



        # start = time.time()
        # end= time.time ()
        # print ("Time for each image " + str (end - start))

writeFile= open ("VIBE2_BenchMark.txt", "w+")
for j in folderNames:
    benchmark =[]
    fileNamesPath="C:/Users//Desktop/Image Project/sample_cdnet/" + j+"/input"
    imgPath=fileNamesPath+ "/in000001.jpg"
    print (imgPath)
    fileNames= os.listdir(fileNamesPath)
    image = cv2.imread(imgPath,0)
    try:
        sampleArray= initBackground (image,sampleCount)
    except:
        continue 
    imageArray= dict ()
    segTemplate =np.zeros ((image.shape[0], image.shape[1],3))
    for i in fileNames[0:2]:
        imgPath= fileNamesPath+"/" + i
        # print ("Reading from " + imgPath)
        image = cv2.imread(imgPath,0)
        imageArray[i]=image

#     segMaps=[]
#     counter=2
    for i in imageArray.items ():
        print (i[0])
        name=i[0]

        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        start = time.time()
        try:
            segmentationMap, sampleArray=updateWithVibe (i[1], sampleArray, distanceThreshold, sampleCount) 
        except:
            continue    
        for x in segmentationMap:
            print (x)
        end= time.time ()
        benchmark.append ((end-start))

        # print ("Time for each image " + str (end - start))
        writePath="C:/Users//Desktop/Image Project/sample_cdnet/" + j+"/output/png/" + "b" + name[0:(len(name)-4)] + ".png"
        print ("Writing to " + writePath)
        cv2.imwrite(writePath, segmentationMap)
    writeStr = "For " + j + " the total write time is " + str (sum(benchmark)) + " average is " + str ((sum(benchmark))/10) + "\n"
    writeFile.write (writeStr)

writeFile.close ()

def runOpenCVBGS ():


    folderNames=os.listdir("C:/Users//Desktop/Image Project/sample_cdnet")
    folderNames.remove ('.tmp.drivedownload')

    print (folderNames)
            # start = time.time()
            # end= time.time ()
            # print ("Time for each image " + str (end - start))

    writeFile= open ("LSBP_BenchMark.txt", "w+")

    for j in folderNames:
        imageArray= dict ()

        backSub = cv2.bgsegm.createBackgroundSubtractorLSBP()

        
        fileNamesPath="C:/Users//Desktop/Image Project/sample_cdnet/" + j+"/input"
        fileNames= os.listdir(fileNamesPath)
        for i in fileNames:
            imgPath= fileNamesPath+"/" + i
            image = cv2.imread(imgPath,0)
            imageArray[i]=image

        fileNamesPath2="C:/Users//Desktop/Image Project/sample_cdnet/" + j+"/output/png5LSBP"
        try:
            os.mkdir (fileNamesPath2)
        except:
            pass
        start = time.time ()
        for i in imageArray.items ():
            frame = i[1]
            # print (i[0])
            # if frame is None:
            #     break
            
            fgMask = backSub.apply(frame)
            name=i[0]
            name=name[0:(len(i) - 6)]
            writePath="C:/Users//Desktop/Image Project/sample_cdnet/" + j+"/output/png5LSBP/" + "b" + name + ".png"
            # print ("Writing to " + writePath)
            cv2.imwrite(writePath, fgMask)
        end= time.time ()
        timeRan= end - start
        timeRanAve= timeRan/len (imageArray.items ())
        statsStr= j + " Ran for " + str (timeRan) + " over " + str (len(imageArray.items ())) + " for an average of " + str (timeRanAve) + "\n\n"
        print (statsStr)
        writeFile.write (statsStr)


        writeFile.close ()

#make videos of all the various runs.
def videoMaker ():
    folderNames=["continuousPan"]

    # folderNames=os.listdir("C:/Users//Desktop/Image Project/sample_cdnet")
    # folderNames.remove ('.tmp.drivedownload')
    storePlace="C:/Users//Desktop/Image Project/Videos2/"
    for i in folderNames:
        print (i)
        video_URL = "C:/Users//Desktop/Image Project/sample_cdnet/" + i + "/input/*.jpg" 
        video_URL2 = "C:/Users//Desktop/Image Project/sample_cdnet/" + i + "/output/png/*.png" 
        video_URL3 = "C:/Users//Desktop/Image Project/sample_cdnet/" + i + "/output/png2/*.png" 
        img_array = []
        fileName1=storePlace+ i + "_in.avi"
        fileName2=storePlace + i + "_VIBE.avi"
        fileName3=storePlace + i + "_GMM.avi"
        # print (video_URL)
        print (video_URL)
        print (video_URL2)
        print (video_URL3)
        print ("\n")
        for filename in glob.glob(video_URL):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)


        out = cv2.VideoWriter(fileName1,cv2.VideoWriter_fourcc(*'XVID'), 30, size)
         
        for j in range(len(img_array)):
            out.write(img_array[j])
        out.release()
        img_array=[]



        for filename in glob.glob(video_URL2):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)


        out = cv2.VideoWriter(fileName2,cv2.VideoWriter_fourcc(*'XVID'), 30, size)
         
        for j in range(len(img_array)):
            out.write(img_array[j])
        out.release()
        img_array=[]

        for filename in glob.glob(video_URL3):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)


        out = cv2.VideoWriter(fileName3,cv2.VideoWriter_fourcc(*'XVID'), 30, size)
         
        for j in range(len(img_array)):
            out.write(img_array[j])
        out.release()



# run comparator that shows the final stats
def runComparator ():
    comparStr = "Comparator.exe "
    datasetPath = ["C:/Users//Desktop/dataset2014/dataset/badWeather/blizzard", "C:/Users//Desktop/dataset2014/dataset/baseline/highway", "C:/Users//Desktop/dataset2014/dataset/cameraJitter/badminton", "C:/Users//Desktop/dataset2014/dataset/dynamicBackground/boats", "C:/Users//Desktop/dataset2014/dataset/intermittentObjectMotion/abandonedBox", "C:/Users//Desktop/dataset2014/dataset/lowFramerate/port_0_17fps", "C:/Users//Desktop/dataset2014/dataset/nightVideos/bridgeEntry",
                   "C:/Users//Desktop/dataset2014/dataset/PTZ/continuousPan", "C:/Users//Desktop/dataset2014/dataset/shadow/backdoor", "C:/Users//Desktop/dataset2014/dataset/thermal/corridor",
                   "C:/Users//Desktop/dataset2014/dataset/turbulence/turbulence0"]


    myResultsPath = [" \"C:/Users//Desktop/Image Project/sample_cdnet/blizzard/output/",
                     " \"C:/Users//Desktop/Image Project/sample_cdnet/highway/output/",
                     " \"C:/Users//Desktop/Image Project/sample_cdnet/badminton/output/",
                     " \"C:/Users//Desktop/Image Project/sample_cdnet/boats/output/",
                     " \"C:/Users//Desktop/Image Project/sample_cdnet/abandonedBox/output/",
                     " \"C:/Users//Desktop/Image Project/sample_cdnet/port_0_17fps/output/",
                     " \"C:/Users//Desktop/Image Project/sample_cdnet/bridgeEntry/output/",
                     " \"C:/Users//Desktop/Image Project/sample_cdnet/continuousPan/output/",
                     " \"C:/Users//Desktop/Image Project/sample_cdnet/backdoor/output/",
                     " \"C:/Users//Desktop/Image Project/sample_cdnet/corridor/output/",
                     " \"C:/Users//Desktop/Image Project/sample_cdnet/turbulence0/output/"]


    folders = ["png", "png2", "png3KNN", "png4GMG", "png5LSBP"]

    dataFolders = ["C:/Users//Desktop/dataset2014/dataset/badWeather/blizzard", "C:/Users//Desktop/dataset2014/dataset/baseline/highway", "C:/Users//Desktop/dataset2014/dataset/cameraJitter/badminton", "C:/Users//Desktop/dataset2014/dataset/dynamicBackground/boats", "C:/Users//Desktop/dataset2014/dataset/intermittentObjectMotion/abandonedBox",
                   "C:/Users//Desktop/dataset2014/dataset/lowFramerate/port_0_17fps", "C:/Users//Desktop/dataset2014/dataset/nightVideos/bridgeEntry", "C:/Users//Desktop/dataset2014/dataset/PTZ/continuousPan", "C:/Users//Desktop/dataset2014/dataset/shadow/backdoor", "C:/Users//Desktop/dataset2014/dataset/thermal/corridor", "C:/Users//Desktop/dataset2014/dataset/turbulence/turbulence0"]

    for j in folders:

        try:
            delAll()
        except:
            pass

        for i in range(0, len(myResultsPath)):

            testStr = comparStr + datasetPath[i] + \
                " " + myResultsPath[i] + j + "\""
            print(testStr)
            mkDirStr = "C:/Users//Desktop/Stats/" + j
            try:
                os.mkdir(mkDirStr)
            except:
                pass
            os.system(testStr)
        folderNames = os.listdir(mkDirStr)
        writeName = "C:/Users//Desktop/Stats/" + j + "/" + j + "_stats.txt"

        for i in dataFolders:
            i_l = i.split("/")
            i_l = i_l[6:]
            i_str=""
            i_str= i_str.join(i_l)
            destination = "C:/Users//Desktop/Stats/" + \
                j + "/" + i_str + "_" + "stats.txt"

            i = i + "/stats.txt"
            # i=i.strip ("\'")
            # i=i.strip ("\"")

            # source= i+ "/stats.txt"
            # destination = "C:/Users//Desktop/Stats/" + \
            #     i + "_" + "stats.txt"
            try:

                dest = shutil.copyfile(i, destination)
            except:
                pass

        
        allStats = os.listdir(mkDirStr)
        writeFile = open(writeName, "w+")
        print(allStats)
        for k in allStats:
            filePath = "C:/Users//Desktop/Stats/" + j + "/" + k
            print (filePath)

            f = open(filePath, "r")
            stats = f.readline()
            stats = stats.split(" ")
            TP = float(stats[1])
            FP = float(stats[2])
            FN = float(stats[3])
            TN = float(stats[4])
            TPR = TP / (TP + FN)
            SPC = TN / (FP + TN)
            PPV = TP / (TP + FP)
            FPR = FP / (FP + TN)
            FNR = FN / (FN + TP)
            F1 = (2 * TP) / ((2 * TP) + FP + FN)
            PWC = (FP + FN) / (TP + TN + FN + FP)
            statsStr = "For " + k + "\n\tRecall:  " + str(TPR) + "\n\tSpecificity " + str(SPC) + "\n\tPrecision " + str(
                PPV) + "\n\tFalse Positive Rate " + str(FPR) + "\n\tFalse Negative Rate " + str(FNR) + "\n\tF1 " + str(F1) + "\n\tPWC " + str(PWC) + "\n\n"
            writeFile.write(statsStr)
