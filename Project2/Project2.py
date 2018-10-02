from PIL import Image
from PIL import ImageDraw
import numpy as np 
from scipy import ndimage
import os
import sys
import matplotlib.pyplot as plt
import glob

pout = Image.open('pout.PNG')

def imageToArray (name):
    global height
    global width
    global pixel_values
    width, height = name.size
    pixel_values = list(name.getdata())
    pixel_values = np.array(pixel_values).reshape([height,width])
    pixel_values = np.array(object=pixel_values, dtype=int)
    return pixel_values

def makeHistogram1(image, filename,picture):
    img=Image.open(image)
    imageToArray(img)
    fig,(left, right) = plt.subplots(1,2)

    left.hist(np.ndarray.flatten(pixel_values),bins=255 ,color='green')
    left.set_title(" Quantity of Pixels per Pixel Value")
    left.set_ylabel('Quantity')
    left.set_xlabel('Pixel Values')
    left.axis(xmin=0, xmax=255)


    right.set_xticks([])
    right.set_yticks([])
    #right.set_title(filename)
    right.imshow(img)

    fig.tight_layout()
    os.chdir(r"C:\Users\rubyc\Google Drive\School\Fall 2018\Digital Image Processing ECE 457\Project2")
    if picture == str("Lena"):
        plt.savefig(filename +".png")
    elif picture == str("Crowd"):
        plt.savefig(filename+".png")


def makeHistogram(originalImage,image,filename,function, value):
    new=imageToArray(image)
    fig, ax = plt.subplots(2,2)

    top_left = ax[0,0]
    top_left.set_xticks([])
    top_left.set_yticks([])
    top_left.set_title(filename +" Original")
    top_left.imshow(originalImage)

    top_right = ax[0,1]
    top_right.set_xticks([])
    top_right.set_yticks([])
    top_right.set_title(filename)
    top_right.imshow(image)

    bottom_left = ax[1,0]
    _, _, _ = bottom_left.hist(np.ndarray.flatten(new),bins=255 ,color='green')
    bottom_left.set_title(str(filename)+" Quantity of Pixels per Pixel Value")
    bottom_left.set_ylabel('Quantity')
    bottom_left.set_xlabel('Pixel Values')
    bottom_left.axis(xmin=0, xmax=255)

    bottom_right = ax[1,1]
    xlim_array=np.arange(255)
    bottom_right.set_title("Transfer Function")
    bottom_right.axis(xmin=0, xmax=255, ymin=0, ymax = 255)
    
    if function == str('shift'):
        shift_xlim_array = xlim_array + value
        shift_xlim_array[shift_xlim_array>255]=255
        shift_xlim_array[shift_xlim_array<0]=0
        bottom_right.plot(xlim_array,shift_xlim_array,color='blue')
        
    elif function == str('stretch'):
        stretch_xlim_array = xlim_array * value
        stretch_xlim_array[stretch_xlim_array>255]=255
        stretch_xlim_array[stretch_xlim_array<0]=0
        bottom_right.plot(xlim_array,stretch_xlim_array,color='blue')

    elif function ==str('cdf'):
        histo,_ =np.histogram(np.ndarray.flatten(new),256)
        cdf_cumsum= np.cumsum(histo)
        cdf = ((cdf_cumsum -1)/cdf_cumsum[-1])*255
        cdf = np.array(object=cdf, dtype=int)
        x=range(0,256)
        bottom_right.plot(x,cdf,color='blue')

    fig.tight_layout()
    plt.savefig(filename+ " "+ function+" "+ str(value) +".png")
    #plt.show()
    
def shift(name, valueToAdd,filename):
    imageToArray(name)
    addArray = np.zeros((height,width))
    addArray = addArray + valueToAdd
    shiftArray = addArray+pixel_values
    shiftArray[shiftArray>255]=255
    shiftArray[shiftArray<0]=0
    newImage=Image.fromarray(shiftArray, mode= None)
    makeHistogram(name,newImage,filename,function=str('shift'),value=valueToAdd)

def stretchImage(image, valueToMultiply, filename):
    imageToArray(image)
    stretchArray = pixel_values*valueToMultiply
    stretchArray[stretchArray>255]=255
    stretchArray[stretchArray<0]=0
    newImage=Image.fromarray(stretchArray, mode = None)
    makeHistogram(image,newImage,filename,function = str('stretch'),value=valueToMultiply) 

def cdf(image,filename):
    imageToArray(image)
    histo,bin_edges =np.histogram(np.ndarray.flatten(pixel_values),256)
    cdf_cumsum= np.cumsum(histo)
    cdf = ((cdf_cumsum -1)/cdf_cumsum[-1])*255
    image2 = np.interp(np.ndarray.flatten(pixel_values),bin_edges[:-1],cdf)
    image2_reshape = image2.reshape(height,width)
    newImage = Image.fromarray(image2_reshape,mode = None)
    makeHistogram(image,newImage, filename,function = str('cdf'),value = 1)

#shift(pout,-50,'Pout')
#shift(pout,-25,'Pout')
#shift(pout,-75,'Pout')
#shift(pout, -100, 'Pout')
#stretchImage(pout,.25,'Pout')
#stretchImage(pout,.50,'Pout')
#stretchImage(pout,2,'Pout')
#stretchImage(pout,4,'Pout')
cdf(pout,'Pout')

BFvideo1=Image.open('BFvideo1.png')
BFvideo2=Image.open('BFvideo2.png')
BFvideo3=Image.open('BFvideo3.png')
BFvideo4=Image.open('BFvideo4.png')
BFvideo5=Image.open('BFvideo5.png')

def imagesubtract(picture1, picture2,handeling,name1,name2):
    image2 = imageToArray(picture2)
    image1 = imageToArray(picture1)

    fig,(left, right) = plt.subplots(1,2)
    left.set_xticks([])
    left.set_yticks([])

    newArray = image2-image1
    if handeling == str('abs'):
        newArray1=abs(newArray)
        x=range(0,255)
        right.plot(x,newArray1)
        right.axis(xmin=np.amin(newArray), xmax=np.max(newArray), ymin=0, ymax=np.amax(newArray))


    if handeling == str('squish'):
        newArray1 = ((newArray +255)/2)
        x=range(0,255)
        right.plot(newArray,newArray1)
    if handeling == str('none'):
        newArray = newArray
        xlim_array=np.arange(255)
        right.plot(xlim_array,newArray)
    newPicture = Image.fromarray(newArray,mode=None)
    left.imshow(newPicture)

    plt.savefig(name2 + " - "+ name1 +" "+ str('squish') +".png")
    #plt.show()
    #newPicture.show() 

imagesubtract(BFvideo1,BFvideo2,handeling=str('squish'),name1=str('BFvideo1'),name2=str('BFvideo2'))
imagesubtract(BFvideo1,BFvideo3,handeling=str('squish'),name1=str('BFvideo1'),name2=str('BFvideo3'))
imagesubtract(BFvideo1,BFvideo4,handeling=str('squish'),name1=str('BFvideo1'),name2=str('BFvideo4'))
imagesubtract(BFvideo1,BFvideo5,handeling=str('squish'),name1=str('BFvideo1'),name2=str('BFvideo5'))

imagesubtract(BFvideo2,BFvideo3,handeling=str('squish'),name1=str('BFvideo2'),name2=str('BFvideo3'))
imagesubtract(BFvideo2,BFvideo4,handeling=str('squish'),name1=str('BFvideo2'),name2=str('BFvideo4'))
imagesubtract(BFvideo2,BFvideo5,handeling=str('squish'),name1=str('BFvideo2'),name2=str('BFvideo5'))

imagesubtract(BFvideo3,BFvideo4,handeling=str('squish'),name1=str('BFvideo3'),name2=str('BFvideo4'))
imagesubtract(BFvideo3,BFvideo5,handeling=str('squish'),name1=str('BFvideo3'),name2=str('BFvideo5'))

imagesubtract(BFvideo4,BFvideo5,handeling=str('squish'),name1=str('BFvideo4'),name2=str('BFvideo5'))

    
#imagesubtract(BFvideo1,BFvideo2,handeling=str('squish'))
#imagesubtract(BFvideo1,BFvideo3,handeling=str('squish'))
#imagesubtract(BFvideo1,BFvideo4,handeling=str('squish'))
#imagesubtract(BFvideo1,BFvideo5,handeling=str('squish'))

#imagesubtract(BFvideo2,BFvideo3,handeling=str('squish'))
#imagesubtract(BFvideo2,BFvideo4,handeling=str('squish'))
#imagesubtract(BFvideo2,BFvideo5,handeling=str('squish'))

#imagesubtract(BFvideo3,BFvideo4,handeling=str('squish'))
#imagesubtract(BFvideo3,BFvideo5,handeling=str('squish'))

#imagesubtract(BFvideo4,BFvideo5,handeling=str('squish'))

#imagesubtract(BFvideo1,BFvideo2,handeling=str('none'))


#Lena_files = glob.glob(r"C:\Users\rubyc\Google Drive\School\Fall 2018\Digital Image Processing ECE 457\Homework1\IntensityQuantized\Lena*.png")
#Crowd_files = glob.glob(r"C:\Users\rubyc\Google Drive\School\Fall 2018\Digital Image Processing ECE 457\Homework1\IntensityQuantized\Crowd*.png")


#for i in range(0, len(Lena_files),1):
    #print(Lena_files[i])
    #makeHistogram1(Lena_files[i],str(i), str("Lena"))
    #makeHistogram1(Lena_files[i],str("Lena_Max_Impulses ") + str(i), str("Lena"))
    #makeHistogram1(Crowd_files[i],str("intensity_") + str(i) +str("_Crowd"), str("Crowd"))