import numpy as np
import cv2
import matplotlib.pyplot as plt
import pandas as pd
from Filtering_Functions import *
# for loading .tif images we use the module below if you don't have the library
# installed use the command below:
# !pip3 install PIL
from PIL import Image


def Image_Alignment(img1, img2, a, b, c, d, norm):
    height = img1.shape[0]
    width = img2.shape[1]
    dist = np.zeros((d - c, b - a))
    for i in range(a,b):
        for j in range(c,d):
            if i <= 0 and j <= 0:
                temp = sum(sum(pow(abs(img1[0:-1+j, 0:-1+i] - img2[-j:-1, -i:-1]), norm)))
                temp = temp/((height+j)*(width+i))
                dist[j-c, i-a] = temp
            
            if i >= 0 and j >= 0:
                temp = sum(sum(pow(abs(img1[j:-1, i:-1] - img2[0:-1-j, 0:-1-i]), norm)))
                temp = temp/((height-j)*(width-i))
                dist[j-c, i-a] = temp
            
            if i > 0 and j < 0:
                temp = sum(sum(pow(abs(img1[0:-1+j, i:-1] - img2[-j:-1, 0:-1-i]), norm)))
                temp = temp/((height+j)*(width-i))
                dist[j-c, i-a] = temp
            
            if i < 0 and j > 0:
                temp = sum(sum(pow(abs(img1[j:-1, 0:-1+i] - img2[0:-1-j, -i:-1]), norm)))
                temp = temp/((height-j)*(width+i))
                dist[j-c, i-a] = temp
    loc = np.array(np.where(dist == dist.min()))
    hor_shift = loc[1][0]
    ver_shift = loc[0][0]
    return (hor_shift, ver_shift)

def Image_Pyramid(img, norm):
    img = img[0:3*int(img.shape[0]/3),:]
    img1 = img[0:int(img.shape[0]/3)]
    img2 = img[int(img.shape[0]/3):2*int(img.shape[0]/3)]
    img3 = img[2*int(img.shape[0]/3):3*int(img.shape[0]/3)]
    img1 = img1/np.max(img)
    img2 = img2/np.max(img)
    img3 = img3/np.max(img)

    rows = img1.shape[0]
    columns = img1.shape[1]
    percent = 0.1

    img1 = img1[int(rows*percent):-int(rows*percent), int(columns*percent):-int(columns*percent)]
    img2 = img2[int(rows*percent):-int(rows*percent), int(columns*percent):-int(columns*percent)]
    img3 = img3[int(rows*percent):-int(rows*percent), int(columns*percent):-int(columns*percent)]

    blurred_img1 = Filtering(img1, Gaussian2D(2,5))
    blurred_img2 = Filtering(img2, Gaussian2D(2,5))
    blurred_img3 = Filtering(img3, Gaussian2D(2,5))
    
    temp_img1 = blurred_img1[0:blurred_img1.shape[0]:16, 0:blurred_img1.shape[1]:16]
    temp_img2 = blurred_img2[0:blurred_img2.shape[0]:16, 0:blurred_img2.shape[1]:16]
    temp_img3 = blurred_img3[0:blurred_img3.shape[0]:16, 0:blurred_img3.shape[1]:16]
    
    height = temp_img1.shape[0]
    width = temp_img2.shape[1]
    
    a1 = -10
    b1 = 10
    c1 = -10
    d1 = 10

    a2 = -10
    b2 = 10
    c2 = -10
    d2 = 10

    (hor1, ver1) = Image_Alignment(temp_img2, temp_img1, a1, b1, c1, d1, norm)
    (hor2, ver2) = Image_Alignment(temp_img2, temp_img3, a2, b2, c2, d2, norm)
    
    step = 6
    for i in [8, 4, 2, 1]:
        a1 = (hor1 + a1)*2 - step
        b1 = a1 + step*2
        c1 = (ver1 + c1)*2 - step
        d1 = c1 + step*2

        a2 = (hor2 + a2)*2 - step
        b2 = a2 + step*2
        c2 = (ver2 + c2)*2 - step
        d2 = c2 + step*2
        temp_img1 = blurred_img1[0:blurred_img1.shape[0]:i, 0:blurred_img1.shape[1]:i]
        temp_img2 = blurred_img2[0:blurred_img2.shape[0]:i, 0:blurred_img2.shape[1]:i]
        temp_img3 = blurred_img3[0:blurred_img3.shape[0]:i, 0:blurred_img3.shape[1]:i]
        (hor1, ver1) = Image_Alignment(temp_img2, temp_img1, a1, b1, c1, d1, norm)
        (hor2, ver2) = Image_Alignment(temp_img2, temp_img3, a2, b2, c2, d2, norm)
    
    
    a, c = c1+ver1, c2+ver2
    b, d = a1+hor1, a2+hor2
    
    return (a,b,c,d)

def Image_Registration(a, b, c, d, img):
    img = img[0:3*int(img.shape[0]/3),:]
    img1 = img[0:int(img.shape[0]/3)]
    img2 = img[int(img.shape[0]/3):2*int(img.shape[0]/3)]
    img3 = img[2*int(img.shape[0]/3):3*int(img.shape[0]/3)]
    img1 = img1/np.max(img)
    img2 = img2/np.max(img)
    img3 = img3/np.max(img)
    x = img1.shape[0]
    y = img1.shape[1]

    X1 = max(0, a, c)
    Y1 = max(0, b, d)
    X2 = min(x+0, x+a, x+c)
    Y2 = min(y+0, y+b, y+d)

    registered_img = np.zeros((X2-X1, Y2-Y1, 3))
    registered_img[:,:,0] = img1[X1-a:X2-a, Y1-b:Y2-b]
    registered_img[:,:,1] = img2[X1:X2, Y1:Y2]
    registered_img[:,:,2] = img3[X1-c:X2-c, Y1-d:Y2-d]    
    return registered_img    

def Cropping(img):
    height = img.shape[0]
    width = img.shape[1]
    
    border_1 = 0
    border_2 = -1
    border_3_1 = 0
    border_4_1 = -1
    border_3_2 = 0
    border_4_2 = -1
    
    for i in range(300):
        if sum(img[:,i,0] == 1) > height/3 or sum(img[:,i,1] == 1) > height/3 or sum(img[:,i,2] == 1) > height/3:
            border_1 = i
        
        if sum(img[:,-1-i,0] == 1) > height/3 or sum(img[:,-1-i,1] == 1) > height/3 or sum(img[:,-1-i,2] == 1) > height/3:
            border_2 = -1-i
        
        if sum(img[i,:,0] == 1) > width/3 or sum(img[i,:,1] == 1) > width/3 or sum(img[i,:,2] == 1) > width/3:
            border_3_1 = i
        
        if sum(img[-1-i,:,0] == 1) > width/3 or sum(img[-1-i,:,1] == 1) > width/3 or sum(img[-1-i,:,2] == 1) > width/3:
            border_4_1 = -1-i
    
    for i in range(200):    
        if sum(img[i,border_1:border_2,0] == 1) > (width-border_1-border_2)/4 or sum(img[i,border_1:border_2,1] == 1) > (width-border_1-border_2)/4 or sum(img[i,border_1:border_2,2] == 1) > (width-border_1-border_2)/4:
            border_3_2 = i
        
        if sum(img[-1-i,border_1:border_2,0] == 1) > (width-border_1-border_2)/4 or sum(img[-1-i,border_1:border_2,1] == 1) > (width-border_1-border_2)/4 or sum(img[-1-i,border_1:border_2,2] == 1) > (width-border_1-border_2)/4:
            border_4_2 = -1-i
    
    border_3 = max(border_3_1, border_3_2)
    border_4 = min(border_4_1, border_4_2)
    
    return (border_1, border_2, border_3, border_4)


if __name__ == '__main__':
    im = Image.open('master-pnp-prok-00800-00889a.tif')
    img = np.array(im)
    img = np.float64(img)
    img = img[0:3*int(img.shape[0]/3),:]
    img1 = img[0:int(img.shape[0]/3)]
    img2 = img[int(img.shape[0]/3):2*int(img.shape[0]/3)]
    img3 = img[2*int(img.shape[0]/3):3*int(img.shape[0]/3)]
    img1 = img1/np.max(img)
    img2 = img2/np.max(img)
    img3 = img3/np.max(img)
    
    a,b,c,d = Image_Pyramid(img, 1)
    registered_img = Image_Registration(a, b, c, d, img)
        
    Kernel1 = np.array([[1,0,-1],[2,0,-2],[1,0,-1]])
    registered_img = np.float32(registered_img)
    filtered_img_1 = np.zeros((registered_img.shape[0] - 3,registered_img.shape[1] - 3,3))
    filtered_img_1[:,:,0] = Filtering(registered_img[:,:,0], Kernel1)
    filtered_img_1[:,:,1] = Filtering(registered_img[:,:,1], Kernel1)
    filtered_img_1[:,:,2] = Filtering(registered_img[:,:,2], Kernel1)
    
    Kernel2 = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
    filtered_img_2 = np.zeros((registered_img.shape[0] - 3,registered_img.shape[1] - 3,3))
    filtered_img_2[:,:,0] = Filtering(registered_img[:,:,0], Kernel2)
    filtered_img_2[:,:,1] = Filtering(registered_img[:,:,1], Kernel2)
    filtered_img_2[:,:,2] = Filtering(registered_img[:,:,2], Kernel2)
    
    filtered_img = np.zeros(filtered_img_1.shape)
    filtered_img = np.sqrt(pow(filtered_img_1, 2) + pow(filtered_img_2, 2))
    filtered_img[:,:,0] = filtered_img[:,:,0]/np.max(filtered_img[:,:,0])
    filtered_img[:,:,1] = filtered_img[:,:,1]/np.max(filtered_img[:,:,1])
    filtered_img[:,:,2] = filtered_img[:,:,2]/np.max(filtered_img[:,:,2])
    
    filtered_img[filtered_img >= 0.1] = 1
    filtered_img[filtered_img < 0.1] = 0
    border_1, border_2, border_3, border_4 = Cropping(filtered_img)
    
    cv2.imwrite('image.jpg', np.uint8(registered_img[border_3+3:border_4-3,border_1+3:border_2-3,:]*255))
