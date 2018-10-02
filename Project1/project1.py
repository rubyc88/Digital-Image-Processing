from PIL import Image
from PIL import ImageDraw
import numpy as np 
from random import randint
from scipy import ndimage

np.set_printoptions(threshold=np.nan)
isri = Image.open("isri.png")
skull = Image.open("skull.gif")

def imageToArray (name):
    global height
    global width
    global pixel_values

    width, height = name.size
    pixel_values = list(name.getdata())
    pixel_values = np.array(pixel_values).reshape((height,width))

    if name==skull:
        for i in range(0,height,1):
            for j in range(0,width,1):
                if pixel_values[i][j]>128:
                    pixel_values[i][j]=1
                else:
                    pixel_values[i][j]=0
    #np.savetxt("pixelvalues.csv" ,pixel_values,delimiter=",")
    return pixel_values

def n4(imageName):
    global connectedArray
    imageToArray (imageName)
    connectedArray=np.zeros([height,width],dtype=np.int)
    k=1

    for x in range (0, height, 1):
        for y in range(0, width, 1):
            #checks to see if pixel value is already a zero, if so keeps it a zero
            if pixel_values[x][y]==0:
                connectedArray[x][y]=pixel_values[x][y]
            else:
                # if the pixel above and the pixel left are 0 put value as k, increment k
                if pixel_values[x][y-1]==0 and pixel_values[x-1][y]==0: 
                        connectedArray[x][y]=k
                        k+=1
                # if pixel to the left is not 0 and the pixel above is 0 put the value of the left into current location        
                elif pixel_values[x][y-1]!=0 and pixel_values[x-1][y]==0:
                   connectedArray[x][y]=connectedArray[x][y-1]

                #if the pixel value to the left is not 0 and the pixel to top is not 0 set all values to the minimum value 
                elif pixel_values[x][y-1]!=0 and pixel_values[x-1][y]!=0:
                    if connectedArray[x][y-1] == connectedArray[x-1][y]:
                        connectedArray[x][y] = connectedArray[x][y-1]
                    elif connectedArray[x][y-1] != connectedArray[x-1][y]: 
                        connectedArray[x][y] = connectedArray[x-1][y]
                        #for values in connected array that are equal to connectedArray[x][y-1] set it equal to connectedArray[x-1][y]
                        connectedArray[connectedArray == connectedArray[x][y-1]] = connectedArray[x-1][y]
                
                #if pixel to the left is zero and the pixel above is not 0 put the value of the above pixel in connected array
                elif pixel_values[x][y-1]==0 and pixel_values[x-1][y]!=0:
                    connectedArray[x][y]= connectedArray[x-1][y]
    r, g, b =colorArray(connectedArray)   
    
    r = Image.fromarray(r, mode=None)
    g = Image.fromarray(g, mode=None)
    b = Image.fromarray(b, mode=None)
    
    mergeImage = Image.merge("RGB",(r,g,b))
    bbox(connectedArray,mergeImage)
    mergeImage.show()
    
def n8(imageName):
    imageToArray (imageName)
    connectedArray=np.zeros([height, width])
    k=1

    for x in range (0, height, 1):
        for y in range(0, width, 1):
            #checks to see if pixel value is already a zero, if so keeps it a zero
            if pixel_values[x,y]==0:
                connectedArray[x,y]=pixel_values[x,y]
            else:
                # if the pixel above and the pixel left are 0 put value as k, increment k    Case 1
                if pixel_values[x-1,y+1]==0 and pixel_values[x-1,y]==0 and pixel_values[x-1,y-1]==0 and pixel_values[x,y-1]==0: 
                        connectedArray[x][y]=k
                        k+=1
                #Case 2
                elif pixel_values[x-1,y+1]!=0 and pixel_values[x-1,y]==0 and pixel_values[x-1,y-1]==0 and pixel_values[x,y-1]==0:
                    connectedArray[x,y]=connectedArray[x-1,y+1]
                #Case 3
                elif pixel_values[x-1,y+1]==0 and pixel_values[x-1,y]!=0 and pixel_values[x-1,y-1]==0 and pixel_values[x,y-1]==0:
                    connectedArray[x,y]=connectedArray[x-1,y]
                #Case 4
                elif pixel_values[x-1,y+1]!=0 and pixel_values[x-1,y]!=0 and pixel_values[x-1,y-1]==0 and pixel_values[x,y-1]==0:
                    connectedArray[x,y]=connectedArray[x-1,y]
                #Case 5
                elif pixel_values[x-1,y+1]==0 and pixel_values[x-1,y]==0 and pixel_values[x-1,y-1]!=0 and pixel_values[x,y-1]==0: 
                    connectedArray[x,y]=connectedArray[x-1,y-1]
                #Case 6
                elif pixel_values[x-1,y+1]!=0 and pixel_values[x-1,y]==0 and pixel_values[x-1,y-1]!=0 and pixel_values[x,y-1]==0:
                    if connectedArray[x-1,y+1] == connectedArray[x-1,y-1]:
                        connectedArray[x,y]=connectedArray[x-1,y+1]
                    else:
                         #for values in connected array that are equal to connectedArray[x][y-1] set it equal to connectedArray[x-1][y]
                        connectedArray[x,y] = connectedArray[x-1,y+1]
                        connectedArray[connectedArray == connectedArray[x-1,y-1]] = connectedArray[x-1,y+1]
                #Case 7
                elif pixel_values[x-1,y+1]==0 and pixel_values[x-1,y]!=0 and pixel_values[x-1,y-1]!=0 and pixel_values[x,y-1]==0:
                    connectedArray[x,y]=connectedArray[x-1,y-1]
                #Case 8
                elif pixel_values[x-1,y+1]!=0 and pixel_values[x-1,y]!=0 and pixel_values[x-1,y-1]!=0 and pixel_values[x,y-1]==0:
                    connectedArray[x,y]=connectedArray[x-1,y+1]
                #Case 9 
                elif pixel_values[x-1,y+1]==0 and pixel_values[x-1,y]==0 and pixel_values[x-1,y-1]==0 and pixel_values[x,y-1]!=0:
                    connectedArray[x,y]=connectedArray[x,y-1]
                #Case 10
                elif pixel_values[x-1,y+1]!=0 and pixel_values[x-1,y]==0 and pixel_values[x-1,y-1]==0 and pixel_values[x,y-1]!=0:
                    if connectedArray[x-1,y+1]==connectedArray[x,y-1]:
                        connectedArray[x,y]=connectedArray[x-1,y+1]
                    else:    
                        #for values in connected array that are equal to connectedArray[x][y-1] set it equal to connectedArray[x-1][y]
                        connectedArray[x,y] = connectedArray[x-1,y+1]
                        connectedArray[connectedArray == connectedArray[x,y-1]] = connectedArray[x-1,y+1]
                #Case 11
                elif pixel_values[x-1,y+1]==0 and pixel_values[x-1,y]!=0 and pixel_values[x-1,y-1]==0 and pixel_values[x,y-1]!=0:
                    connectedArray[x,y]=connectedArray[x-1,y]
                #Case 12
                elif pixel_values[x-1,y+1]!=0 and pixel_values[x-1,y]!=0 and pixel_values[x-1,y-1]==0 and pixel_values[x,y-1]!=0:
                    connectedArray[x,y]=connectedArray[x-1,y+1]
                #Case 13
                elif pixel_values[x-1,y+1]==0 and pixel_values[x-1,y]==0 and pixel_values[x-1,y-1]!=0 and pixel_values[x,y-1]!=0:
                    connectedArray[x,y]=connectedArray[x,y-1]
                #Case 14
                elif pixel_values[x-1,y+1]!=0 and pixel_values[x-1,y]==0 and pixel_values[x-1,y-1]!=0 and pixel_values[x,y-1]!=0:
                    if connectedArray[x-1,y+1]==connectedArray[x-1,y-1]==connectedArray[x,y-1]:
                        connectedArray[x,y]=connectedArray[x-1,y+1]
                    else:
                        connectedArray[x,y]=connectedArray[x-1,y+1]
                        connectedArray[connectedArray == connectedArray[x-1,y-1]] = connectedArray[x-1,y+1]
                        connectedArray[connectedArray == connectedArray[x,y-1]] = connectedArray[x-1,y+1]
                #Case 15
                if pixel_values[x-1,y+1]==0 and pixel_values[x-1,y]!=0 and pixel_values[x-1,y-1]!=0 and pixel_values[x,y-1]!=0:
                        connectedArray[x,y]=connectedArray[x-1,y]
                #Case 16
                if pixel_values[x-1,y+1]!=0 and pixel_values[x-1,y]!=0 and pixel_values[x-1,y-1]!=0 and pixel_values[x,y-1]!=0:
                        connectedArray[x,y]=connectedArray[x-1,y+1]

    r, g, b =colorArray(connectedArray)   
    
    r = Image.fromarray(r, mode=None)
    g = Image.fromarray(g, mode=None)
    b = Image.fromarray(b, mode=None)

    mergeImage = Image.merge("RGB",(r,g,b))
    bbox(connectedArray,mergeImage)
    mergeImage.show()

def colorArray(array):
    global uList
    uList=np.unique(array)
    r = np.zeros((height, width), dtype='uint8')
    g = np.zeros((height, width), dtype='uint8')
    b = np.zeros((height, width), dtype='uint8')

    # making the original picture RGB
    r[array==0] = 255
    g[array==0] = 255
    b[array==0] = 255

    for i in uList:
        if i !=0:
            r[array==i] = np.random.randint(0,high=255)
            g[array==i] = np.random.randint(0,high=255)
            b[array==i] = np.random.randint(0,high=255)
    return r, g, b

# 
def bbox(array, img):
    for colors in uList:
        if colors!=0:
            x1=ndimage.find_objects(array==colors)[0][0].start
            x2=ndimage.find_objects(array==colors)[0][1].start
            y1=ndimage.find_objects(array==colors)[0][0].stop 
            y2=ndimage.find_objects(array==colors)[0][1].stop
            ImageDraw.Draw(img).rectangle([(x2,x1),(y2,y1)], outline=1)
n4(isri)
n4(skull)
n8(isri)
n8(skull)