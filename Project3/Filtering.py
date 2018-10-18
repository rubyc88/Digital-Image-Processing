from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import math 
import scipy.stats as st
from mpl_toolkits.mplot3d import Axes3D

height=256
width = 256
radius = 100
cropx = 256
cropy = 256


Lena = Image.open("Lena.png") # 300x300
Crowd = Image.open("Crowd.png") # 512x512

imageArray=np.ones([height,width],dtype=np.int)*256
whiteImage=Image.fromarray(imageArray)
circle = ImageDraw.Draw(whiteImage)
circle.ellipse((height/2-radius, width/2-radius, height/2+radius, width/2+radius),fill="black")

def imageToArray (name):
    global pixel_values
    width, height = name.size
    pixel_values = list(name.getdata())
    pixel_values = np.array(pixel_values).reshape([height,width])
    pixel_values = np.array(object=pixel_values, dtype=int)
    return pixel_values, 

def cropImage(image):
    global croppedImage
    width, height = image.size
    left = width/2 - cropx/2
    top = height/2 - cropy/2
    right = width/2 + cropx/2
    bottom = height/2 + cropx/2
    croppedImage=image.crop((left, top,right,bottom))

def AverageFilter(image, n):
    title= str('Average Filter')
    if image==Lena:
        picture = str('Lena')
    elif image == Crowd:
        picture = str('Crowd')
    else:
        picture = str('Circle')

    cropImage(image)
    imageToArray(croppedImage)
    averageKernel=np.ones((n,n),dtype=int)*(1/(n*n))
    average_array = ndimage.convolve(pixel_values, averageKernel,mode='constant',cval=0.0)
    newImage=Image.fromarray(abs(average_array),mode=None)
    
    fig = plt.figure()
    Left=fig.add_subplot(121)
    Left.imshow(croppedImage)
    Left.set_xticks([])
    Left.set_yticks([])
    Left.set_xlabel('Original Image')

    Left=fig.add_subplot(122)
    Left.imshow(newImage)
    Left.set_xticks([])
    Left.set_yticks([])
    Left.set_xlabel('Effects of ' + str(n)+ 'X' + str(n) + ' Averageing Kernel')

    plt.show()


def SobelFilter(image,direction):
    if image==Lena:
        picture = str('Lena')
    elif image == Crowd:
        picture = str('Crowd')
    else:
        picture = str('Circle')

    cropImage(image)
    imageToArray(croppedImage)
    if direction == str('down'):
        sobel = np.array([1,0,-1,2,0,-2,1,0,-1]).reshape(3,3)
    elif direction == str('right'):
        sobel = np.array([1,2,1,0,0,0,-1,-2,-1]).reshape(3,3)
    elif direction == str('backdiag'):
        sobel = np.array([0,1,2,-1,0,1,-2,-1,0]).reshape(3,3)
    elif direction ==str('forwarddiag'):
        sobel = np.array([-2,-1,0,-1,0,1,0,1,2]).reshape(3,3)
    sobel_array = ndimage.convolve(pixel_values, sobel,mode='constant',cval=0.0)
    newImage=Image.fromarray(abs(sobel_array),mode=None)
    newImage.show()

def PrewittFilter(image,direction, fft=False):
    if image==Lena:
        picture = str('Lena')
    elif image == Crowd:
        picture = str('Crowd')
    else:
        picture = str('Circle')

    cropImage(image)
    imageToArray(croppedImage)
    if direction == str('down'):
        prewitt = np.array([1,1,1,0,0,0,-1,-1,-1]).reshape(3,3)
    elif direction == str('right'):
        prewitt = np.array([1,0,-1,1,0,-1,1,0,-1]).reshape(3,3)
    elif direction == str('backdiag'):
        prewitt = np.array([0,1,1,-1,0,1,-1,-1,0]).reshape(3,3)
    elif direction ==str('forwarddiag'):
        prewitt = np.array([-1,-1,0,-1,0,1,0,1,1]).reshape(3,3)
    prewitt_array = ndimage.convolve(pixel_values, prewitt,mode='constant',cval=0.0)
    newImage=Image.fromarray(abs(prewitt_array),mode=None)
    newImage.show()

def laplacianFilter(image,number):
    if image==Lena:
        picture = str('Lena')
    elif image == Crowd:
        picture = str('Crowd')
    else:
        picture = str('Circle')

    cropImage(image)
    imageToArray(croppedImage)
    if number == -4:
        laplacian=np.array([0,1,0,1,-4,1,0,1,0]).reshape(3,3)
    if number == -8:
        laplacian=np.array([1,1,1,1,-8,1,1,1,1]).reshape(3,3)
    if number == 4:
        laplacian=np.array([0,-1,0,-1,4,-1,0,-1,0]).reshape(3,3)
    if number ==8:
        laplacian=np.array([-1,-1,-1,-1,8,-1,-1,-1,-1]).reshape(3,3) 
    laplacian_array = ndimage.convolve(pixel_values, laplacian,mode='constant',cval=0.0)
    newImage=Image.fromarray(abs(laplacian_array),mode=None)
    newImage.show()

def robertsFilter(image,direction):
    if image==Lena:
        picture = str('Lena')
    elif image == Crowd:
        picture = str('Crowd')
    else:
        picture = str('Circle')

    cropImage(image)
    imageToArray(croppedImage)
    if direction == str('forwarddiag'):
        roberts=np.array([1,0,0,-1]).reshape(2,2)
    elif direction == str('backdiag'):
        roberts=np.array([0,1,-1,0]).reshape(2,2)
    roberts_array = ndimage.convolve(pixel_values, roberts,mode='constant',cval=0.0)
    newImage=Image.fromarray(abs(roberts_array),mode=None)
    newImage.show()
    
def gaussianFilter(image,n,sigma):
    if image==Lena:
        picture = str('Lena')
    elif image == Crowd:
        picture = str('Crowd')
    else:
        picture = str('Circle')

    cropImage(image)
    imageToArray(croppedImage)
    guassian=np.zeros([n,n])
    for x in range (-int(n/2),int(n/2)+1):
        for y in range (-int(n/2),int(n/2)+1):
            s=(-(math.pow(x,2)+math.pow(y,2)))
            d=(2*math.pow(sigma,2))
            v=(s/d)
            guassian[x+int(n/2),y+int(n/2)]=(1/(2*np.pi*(sigma**2)))*(np.e**v)
    guassian=guassian/(sum(sum(guassian)))
    guassian_array = ndimage.convolve(pixel_values, guassian,mode='constant',cval=0.0)
    newImage=Image.fromarray(abs(guassian_array),mode=None)
    newImage.show()

def fftFilters(image, idealorNot=True, filter='lowpass',sigmaLow=1, sigmaHi=2,raidus1=1,raidus2=2):
   
    if image==Lena:
        picture = str('Lena')
    elif image == Crowd:
        picture = str('Crowd')
    else:
        picture = str('Circle')

    cropImage(image)
    imageToArray(croppedImage)
    xgrid=np.arange(-height/2,height/2,1)
    ygrid=np.arange(-width/2,width/2,1)
    x,y=np.meshgrid(xgrid,ygrid)
    h=np.zeros([height,width])
    if idealorNot == True:
        if filter == str("lowpass"):
            filters=((x**2+y**2)<raidus1**2)
            title=str('Ideal Low Pass Filter')
        if filter == str("highpass"):
            filters=((x**2+y**2)>raidus1**2)
            title = str('Ideal High Pass Filter')
        if filter == str("bandpass"):
            filters1=((x**2+y**2)>raidus1**2)
            filters2=((x**2+y**2)<raidus2**2)
            filters=filters2*filters1
            title=str('Ideal Band Pass Filter')
        if filter == str("bandstop"):
            filters1=1-((x**2+y**2)>raidus1**2)
            filters2=((x**2+y**2)<raidus2**2)
            filters=filters1-filters2
            title=str('Ideal Band Stop Filter')
        h[filters==True]=1
        h[filters==False]=0

    if idealorNot == False:
        sigmaLow=2*sigmaLow**2
        sigmaHi=2*sigmaHi**2
        if filter==str("lowpass"):
            filters=np.exp(-(x**2+y**2)/sigmaLow)
            title=str('Gaussian Low Pass Filter')
            dim=str('Sigma Value of: ' + str(sigmaLow))
        if filter == str("highpass"):
            filters=1-np.exp(-(x**2+y**2)/sigmaLow)
            title=str('Gaussian High Pass Filter')
            dim=str('Sigma Value of: ' + str(sigmaLow))
        if filter == str("bandpass"):
            filters= np.exp(-(x**2+y**2)/sigmaHi)- np.exp(-(x**2+y**2)/sigmaLow)
            filters=filters/np.max(np.max(filters))
            title=str('Gaussian Band Pass Filter')
            dim=str('Between Sigma Values: ' + str(sigmaHi) +' & ' + str(sigmaLow))
        if filter == str("bandstop"):
            filters=np.exp(-(x**2+y**2)/sigmaHi)- np.exp(-(x**2+y**2)/sigmaLow)
            filters=1-filters
            filters=filters/np.max(np.max(filters))
            title=str('Gaussian Band Stop Filter')
            dim=str('Between Sigma Values: ' + str(sigmaHi) +' & ' + str(sigmaLow))

    #FFT of image
    image_fft = np.fft.fft2(pixel_values)
    #shifting the FFT of image
    image_fft_shift = np.fft.fftshift(image_fft)

    #to display FFT of image
    magnitude_spectrum = 20*np.log(np.abs(image_fft_shift))
    newImage=Image.fromarray(abs(magnitude_spectrum),mode=None)
    
    # image * filter
    image_filter=image_fft_shift*filters
    
    #inverse shift
    inverseShift_image_filter=np.fft.ifftshift(image_filter)
    #inverse DFT
    inverseDFT_inverseShift_image_filter=np.fft.ifft2(inverseShift_image_filter)
    #abs
    newImage1=Image.fromarray(abs(inverseDFT_inverseShift_image_filter),mode=None)
    newImage1=(newImage1/np.max(np.max(newImage1))*255)
   
    fig = plt.figure()
    
    #Left = fig.add_subplot(141,projection='3d')
    #Left.plot_surface(x,y,filters, cmap='bone')
    #Left.set_xticks([])
    #Left.set_yticks([])
    #Left.set_zticks([])
    
    Left=fig.add_subplot(141)
    Left.imshow(image)
    Left.set_xticks([])
    Left.set_yticks([])
    Left.set_xlabel('Original Image')

    Left_Center = fig.add_subplot(142)
    Left_Center.imshow(newImage)
    Left_Center.set_xticks([])
    Left_Center.set_yticks([])
    Left_Center.set_xlabel('Spectrum of Image')

    Right_Center = fig.add_subplot(143)
    Right_Center.imshow(filters,cmap='bone')
    Right_Center.set_xticks([])
    Right_Center.set_yticks([])
    Right_Center.set_xlabel('Filter')

    Right = fig.add_subplot(144)
    Right.imshow(newImage1,cmap='gray')
    Right.set_xticks([])
    Right.set_yticks([])
    Right.set_xlabel(picture)

    fig.tight_layout()
    fig.suptitle(title,fontsize=16, y =.9 )
    #fig.suptitle(dim,  y =.3) 
    
    plt.show()    
            

#PrewittFilter(Lena,direction ='forwarddiag',fft=True)
#SobelFilter(whiteImage,direction= 'right',filename='Lena',fft=True)
#SobelFilter(Lena,direction= 'down',filename='Lena')
AverageFilter(whiteImage,3)
#AverageFilter(Lena,11,Lena,fft=True)
#AverageFilter(Lena,3,Lena)
#AverageFilter(Lena,15)
#AverageFilter(Crowd,9)
#cropImage(Crowd)
#gaussianFilter(Lena,3,100,fft=True)
#gaussianFilter(Lena,10,5,filter='lowpass',fft=True)
#laplacianFilter(Lena,-4,fft=True)
#laplacianFilter(Lena,8)
#laplacianFilter(Lena,4)
#laplacianFilter(Lena,-8)
#robertsFilter(Lena, direction='backdiag',fft=True)
#fftFilters(Lena,idealorNot=False,filter='bandpass',sigma=1)
#fftFilters(Lena,idealorNot=False,filter='bandstop',sigmaLow=5, sigmaHi=25,raidus1=1,raidus2=25)
#fftFilters(Lena,idealorNot=True,filter='highpass')
