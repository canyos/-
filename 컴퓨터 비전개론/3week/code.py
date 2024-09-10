from PIL import Image
import math
import numpy as np

"""
Get and use the functions associated with gaussconvolve2d that you used in the last HW02.
"""
def gauss1d(sigma):
    # implement
    length = math.ceil(sigma*6) #sigma*6의 올림을 구한다.
    if length%2==0:#올림한 수가 짝수라면 1더한다.
        length+=1
    x = np.arange(length) - length//2 #0이 중심인 length길이의 array 생성
    x = np.exp((-x*x)/(2*sigma*sigma))# 배열에 대해 density function 적용
    x = x/np.sum(x)#합이 1이 되도록 normalize
    return x

def gauss2d(sigma):
    # implement
    x= gauss1d(sigma)#1차원 gaussian filter 생성
    x = np.outer(x,x)#1D gaussian filter를 외적해 2D gaussian filter 생성
    return x

def convolve2d(array,filter):
    
    # implement
    height, width = array.shape#이미지의 높이 너비
    filterSize = filter.shape[0] # 필터 한변의 길이
    paddingSize = filterSize//2 # 패딩으로 채워야할 크기

    paddingArray = array.copy() 
    paddingArray = np.pad(paddingArray,((paddingSize,paddingSize),(paddingSize,paddingSize)),
           'constant', constant_values=0) # 패딩사이즈 만큼 상하좌우를 0 으로 패딩 

    
    np.flip(filter, axis=0) 
    np.flip(filter, axis=1)#filter의 상하좌우 반전

    x = np.zeros((height, width)) #filtering 한 이미지 저장할 변수
    for i in range(height) : 
        for j in range(width) : 
            window = paddingArray[i:i+filterSize, j:j+filterSize] #이미지 i,j의 근처의 패딩사이즈 정사각형
            x[i,j] = np.sum(window*filter) #convolution한 값을 새로운 이미지의 값으로 저장
    
    return x 
    

def gaussconvolve2d(array,sigma):
    # implement
    filter = gauss2d(sigma)#sigma로 2d gaussian filter생성
    x = convolve2d(array, filter)#이미지와 filter로 filtering한 이미지 생성
    return x

def reduce_noise(img):
    """ Return the gray scale gaussian filtered image with sigma=1.6
    Args:
        img: RGB image. Numpy array of shape (H, W, 3).
    Returns:
        res: gray scale gaussian filtered image (H, W).
    """
    #implement
    image = img.convert('L')#그레이스케일로 변환
    image = np.asarray(image).astype(np.float32)
    res = gaussconvolve2d(image, 1.6)#sigma 1.6으로 gaussian filter적용
    res = np.clip(res, 0, 255) #0~255범위로 조정
    
    return res

def sobel_filters(img):
    """ Returns gradient magnitude and direction of input img.
    Args:
        img: Grayscale image. Numpy array of shape (H, W).
    Returns:
        G: Magnitude of gradient at each pixel in img.
            Numpy array of shape (H, W).
        theta: Direction of gradient at each pixel in img.
            Numpy array of shape (H, W).
    Hints:
        - Use np.hypot and np.arctan2 to calculate square root and arctan
    """
    #implement 
    filterX = np.array([[1,0,-1],[2,0,-2],[1,0,-1]],np.float32) #sobel filter생성
    filterY = np.array([[-1,-2,-1],[0,0,0],[1,2,1]],np.float32)
    
    Ix = convolve2d(img,filterX)#convolution해 gradient생성
    Image.fromarray(Ix.astype('uint8')).save('.\\iguana_gradientX.bmp', 'BMP')
    Iy = convolve2d(img,filterY)
    Image.fromarray(Ix.astype('uint8')).save('.\\iguana_gradientY.bmp', 'BMP')

    G = np.hypot(Ix,Iy)#각 원소에 대해 G[i,j] = sqrt(Ix[i,j]**2 + Iy[i,j]**2)
    G = G / np.max(G) * 255 #0~255 범위로 매핑
    theta = np.arctan2(Iy, Ix) #아크탄젠트 함수로 theta 구함
    return (G, theta)

def non_max_suppression(G, theta):
    """ Performs non-maximum suppression.
    This function performs non-maximum suppression along the direction
    of gradient (theta) on the gradient magnitude image (G).
    Args:
        G: gradient magnitude image with shape of (H, W).
        theta: direction of gradients with shape of (H, W).
    Returns:
        res: non-maxima suppressed image.
    """
    
    H, W = G.shape
    res = np.zeros((H, W)) #0으로 된 빈 맵
    angle = theta * 180 / np.pi  # radian을 호도법으로 변경 변환
    #-22.5~22.5 오른쪽 -180~-157.5 , 157.5~180 가로방향
    #22.5~67.5 오른쪽 위 -112.5~-157.5 왼쪽 아래
    #67.5~112.5 위 -67.5~-112.5 아래 
    #-22.5~-67.5 오른쪽 아래 112.5~157.5 왼쪽 위
    for i in range(1, H - 1):
        for j in range(1, W - 1):
            # 가로
            if (-22.5 < angle[i, j] < 22.5) or (-180 <= angle[i, j] <= -157.5) or (157.5 < angle[i, j] <= 180):
                left = G[i, j - 1]
                right = G[i, j + 1]

            # / 대각선
            elif 22.5 <= angle[i, j] < 67.5 or -157.5 <= angle[i,j] < -112.5:
                left = G[i - 1, j + 1]
                right = G[i + 1, j - 1]

            # \ 대각선
            elif 67.5 <= angle[i, j] < 112.5 or -112.5<= angle[i,j] < -67.5:
                left = G[i - 1, j]
                right = G[i + 1, j]

            # 수직
            elif 112.5 <= angle[i, j] < 157.5 or -67.5 < angle[i,j] <= -22.5 :
                left = G[i - 1, j - 1]
                right = G[i + 1, j + 1]

            if (G[i, j] > left) and (G[i, j] > right):   # 좌우보다 더 크면 저장
                res[i, j] = G[i, j]
    
    return res
    
    
def double_thresholding(img):
    """ 
    Args:
        img: numpy array of shape (H, W) representing NMS edge response.
    Returns:
        res: double_thresholded image.
    """
    #implement     
    diff = np.max(img) - np.min(img)  #threshold 생성
    thresholdH = np.min(img) + diff * 0.15
    thresholdL = np.min(img) + diff * 0.03

    weak = 80
    strong = 255

    res = np.zeros(img.shape) #0으로 채워진 맵 생성
    #np.where(조건, 참 반환값, 거짓 반환값)
    res = np.where((thresholdL <= img) & (img < thresholdH), np.ones(img.shape) * weak, res)    # thresholds 사이면 weak
    res = np.where(thresholdH <= img, np.ones(img.shape) * strong, res) # high threshold 이상이면 strong
    return res

def dfs(img, res, i, j, visited=[]):
    # calling dfs on (i, j) coordinate imply that
    #   1. the (i, j) is strong edge
    #   2. the (i, j) is weak edge connected to a strong edge
    # In case 2, it meets the condition to be a strong edge
    # therefore, change the value of the (i, j) which is weak edge to 255 which is strong edge
    res[i, j] = 255

    # mark the visitation
    visited.append((i, j))

    # examine (i, j)'s 8 neighbors
    # call dfs recursively if there is a weak edge
    for ii in range(i-1, i+2) :
        for jj in range(j-1, j+2) :
            if (img[ii, jj] == 80) and ((ii, jj) not in visited) :
                dfs(img, res, ii, jj, visited)

def hysteresis(img):
    """ Find weak edges connected to strong edges and link them.
    Iterate over each pixel in strong_edges and perform depth first
    search across the connected pixels in weak_edges to link them.
    Here we consider a pixel (a, b) is connected to a pixel (c, d)
    if (a, b) is one of the eight neighboring pixels of (c, d).
    Args:
        img: numpy array of shape (H, W) representing NMS edge response.
    Returns:
        res: hysteresised image.
    """
    #implement 
    H, W = img.shape
    res = np.zeros((H, W))

    for i in range(1, H - 1):
        for j in range(1, W - 1): # 테두리를 제외한 모든 픽셀
            if (img[i][j] == 255):  # strong pixel이면
                dfs(img, res, i, j)    # dfs 수행
    return res

def main():
    RGB_img = Image.open('./iguana.bmp')
    print(1)
    noise_reduced_img = reduce_noise(RGB_img)
    Image.fromarray(noise_reduced_img.astype('uint8')).save('.\\iguana_blurred.bmp', 'BMP')
    print(2)
    g, theta = sobel_filters(noise_reduced_img)
    Image.fromarray(g.astype('uint8')).save('.\\iguana_sobel_gradient.bmp', 'BMP')
    Image.fromarray(theta.astype('uint8')).save('.\\iguana_sobel_theta.bmp', 'BMP')
    print(3)
    non_max_suppression_img = non_max_suppression(g, theta)
    Image.fromarray(non_max_suppression_img.astype('uint8')).save('.\\iguana_non_max_suppression.bmp', 'BMP')
    print(4)
    double_threshold_img = double_thresholding(non_max_suppression_img)
    Image.fromarray(double_threshold_img.astype('uint8')).save('.\\iguana_double_thresholding.bmp', 'BMP')
    print(5)
    hysteresis_img = hysteresis(double_threshold_img)
    Image.fromarray(hysteresis_img.astype('uint8')).save('.\\iguana_hysteresis.bmp', 'BMP')

main()