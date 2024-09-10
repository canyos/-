from PIL import Image
import numpy as np
import math

def boxfilter(n):
    assert n%2==1 # n이 홀수 인지 assert를 통해 검사한다
    x = np.ones((n,n))/(n*n)# 1로 채워진 n*n 배열을 생성 후 n^2으로 나누어 합을 1로 만들어 준다.
    return x

def gauss1d(sigma):
    length = math.ceil(sigma*6) #sigma*6의 올림을 구한다.
    if length%2==0:#올림한 수가 짝수라면 1더한다.
        length+=1
    x = np.arange(length) - length//2 #0이 중심인 length길이의 array 생성
    x = np.exp((-x*x)/(2*sigma*sigma))# 배열에 대해 density function 적용
    x = x/np.sum(x)#합이 1이 되도록 normalize
    return x

def gauss2d(sigma):
    x= gauss1d(sigma)#1차원 gaussian filter 생성
    x = np.outer(x,x)#1D gaussian filter를 외적해 2D gaussian filter 생성
    return x

def convolve2d(array, filter):
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
    
    return np.clip(x,0,255) #값을 0~255사이로 지정해준다.
    

def gaussconvolve2d(array, sigma):
    filter = gauss2d(sigma)#sigma로 2d gaussian filter생성
    x = convolve2d(array, filter)#이미지와 filter로 filtering한 이미지 생성
    return x


def main():
    
    print("n : 3 \n" , boxfilter(3))
    #print("n : 4 \n" , boxfilter(4)) error
    print("n : 7 \n" , boxfilter(7))

    print("sigma : 0.3 \n" , gauss1d(0.3))
    print("sigma : 0.5 \n" , gauss1d(0.5))
    print("sigma : 1 \n" , gauss1d(1))
    print("sigma : 2 \n" , gauss1d(2))

    print("sigma : 0.5 \n" , gauss2d(0.5))
    print("sigma : 1 \n" , gauss2d(1))
    
    #Part1 4-c,4-d
    image = Image.open('.\\2week\\images\\1a_steve.bmp')#사진을 image로 open
    image.show()#사진을 PIL로 show
    image = image.convert('L')#그레이스케일로 변환
    im_array = np.asarray(image)#이미지를 numpy array로 변환
    sigma = 3
    new_image = gaussconvolve2d(im_array, sigma) #이미지를 실수형으로 변환해 convolution
    new_image = Image.fromarray(new_image.astype('uint8'))#filtering된 이미지를 실수형으로 전환해 이미지로 저장
    new_image.save(".\\2week\\result\\1a_steve.bmp","bmp")#이미지를 storage에 저장
    new_image.show()#filtering된 이미지 show

    #part2 -1
    
    sigma = 10 #시그마를 상대적으로 큰 값 지정
    image = Image.open('.\\2week\\images\\2a_mangosteen.bmp')#사진을 image로 open
    image = np.asarray(image)
    
    r,g,b = image[:,:,0], image[:,:,1], image[:,:,2] #이미지에서 각 r,g,b원소 뽑아냄
    
    r = gaussconvolve2d(r,sigma) #r,g,b 에 대해 각각 convolution함
    g = gaussconvolve2d(g,sigma)
    b = gaussconvolve2d(b,sigma)

    lowf = np.dstack([r,g,b]).astype(np.uint8) #convolution된 r,g,b를 다시 합쳐 이미지 생성
    lowfImage = Image.fromarray(lowf)
    lowfImage.save(".\\2week\\result\\2a_mangosteen_low.bmp","bmp")

    #2-2
    image = Image.open('.\\2week\\images\\2b_orange.bmp')#사진을 image로 open
    image = np.asarray(image)
    r,g,b = image[:,:,0], image[:,:,1], image[:,:,2] #이미지에서 각 r,g,b원소 뽑아냄
    r = gaussconvolve2d(r,sigma) #r,g,b 에 대해 각각 convolution함
    g = gaussconvolve2d(g,sigma)
    b = gaussconvolve2d(b,sigma)

    lowf2 = np.dstack([r,g,b]).astype(np.uint8) #convolution된 r,g,b를 다시 합쳐 이미지 생성
    highf = image - lowf2.astype(np.int16) #원본 이미지에서 low frequency 이미지 빼 high frequency 이미지 생성
    highf = np.clip(highf,-128,127)#high frequency는 -128~127사이 값을 가져야한다.
    highf_image = (highf+np.ones_like(highf)*128).astype(np.uint8)#시각화 위해 128 더함
    highfImage = Image.fromarray(highf_image) 
    highfImage.save(".\\2week\\result\\2b_orange_high.bmp","bmp")
    
    #2-3
    hybrid = lowf + highf #mangosteen이미지의 low frequency와 orange이미지의 high frequency합쳐 새로운 이미지 생성 
    hybrid = np.clip(hybrid,0,255)
    hybridImage = Image.fromarray(hybrid.astype(np.uint8))
    hybridImage.save(".\\2week\\result\\hybrid.bmp","bmp")


    

main()


    

    
    

    