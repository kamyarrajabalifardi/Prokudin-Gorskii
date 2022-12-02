import numpy as np
import cv2


def Gaussian2D(L, sigma = 1.0):
    Kernel = np.zeros((2*L+1, 2*L+1))
    for i in range(-L, L+1):
        for j in range(-L, L+1):
            Kernel[L+i, L+j] = np.exp(-( (i)**2 + (j)**2 )/(2*sigma**2))
    Kernel = Kernel/(sum(sum(Kernel)))
    return Kernel

def Gaussian_Filtering(img, L, sigma = 1.0):
    Kernel = Gaussian2D(L, sigma)
    padded_img = np.zeros((img.shape[0] + 2*L, img.shape[1] + 2*L))
    padded_img[L:img.shape[0] + L, L:img.shape[1] + L] = img
    padded_img_temp = padded_img
    
    rows = padded_img.shape[0]
    columns = padded_img.shape[1]
    print(padded_img)
    for i in range(L, rows-L):
        for j in range(L, columns-L):
            padded_img[i][j] = sum(sum(padded_img_temp[i-L:i+L+1, j-L:j+L+1]*Kernel))
                          
    return padded_img[L: rows-L, L:columns-L] 

def Filtering(Mat, Kernel):
    rows = Kernel.shape[0]
    columns  = Kernel.shape[1]
    filtered_Mat = np.zeros((Mat.shape[0]-rows, Mat.shape[1]-columns), dtype = np.float64)
    for i in range(rows):
        for j in range(columns):
            filtered_Mat += Kernel[i][j]*Mat[i:-1-rows+i+1, j:-1-columns+j+1]
    filtered_Mat[filtered_Mat > 1] = 1   
    return filtered_Mat

def Sobel_Filtering(img):
    Kernel1 = np.array([[1,0,-1],[2,0,-2],[1,0,-1]])
    img = np.float32(img)
    filtered_img_1 = np.zeros((img.shape[0] - 3,img.shape[1] - 3,3))
    filtered_img_1[:,:,0] = Filtering(img[:,:,0], Kernel1)
    filtered_img_1[:,:,1] = Filtering(img[:,:,1], Kernel1)
    filtered_img_1[:,:,2] = Filtering(img[:,:,2], Kernel1)

    Kernel2 = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
    filtered_img_2 = np.zeros((img.shape[0] - 3,img.shape[1] - 3,3))
    filtered_img_2[:,:,0] = Filtering(img[:,:,0], Kernel2)
    filtered_img_2[:,:,1] = Filtering(img[:,:,1], Kernel2)
    filtered_img_2[:,:,2] = Filtering(img[:,:,2], Kernel2)
    filtered_img = np.zeros(filtered_img_1.shape)
    filtered_img = np.sqrt(pow(filtered_img_1, 2) + pow(filtered_img_2, 2))
    filtered_img[:,:,0] = filtered_img[:,:,0]/np.max(filtered_img[:,:,0])
    filtered_img[:,:,1] = filtered_img[:,:,1]/np.max(filtered_img[:,:,1])
    filtered_img[:,:,2] = filtered_img[:,:,2]/np.max(filtered_img[:,:,2])
    
    filtered_img[filtered_img >= 0.1] = 1
    filtered_img[filtered_img < 0.1] = 0
    
    return filtered_img