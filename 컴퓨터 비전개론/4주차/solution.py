import numpy as np
import cv2
import math
import random


def RANSACFilter(
        matched_pairs, keypoints1, keypoints2,
        orient_agreement, scale_agreement):
    """
    This function takes in `matched_pairs`, a list of matches in indices
    and return a subset of the pairs using RANSAC.
    Inputs:
        matched_pairs: a list of tuples [(i, j)],
            indicating keypoints1[i] is matched
            with keypoints2[j]
        keypoints1, 2: keypoints from image 1 and image 2
            stored in np.array with shape (num_pts, 4)
            each row: row, col, scale, orientation
        *_agreement: thresholds for defining inliers, floats
    Output:
        largest_set: the largest consensus set in [(i, j)] format

    HINTS: the "*_agreement" definitions are well-explained
           in the assignment instructions.
    """
    assert isinstance(matched_pairs, list)
    assert isinstance(keypoints1, np.ndarray)
    assert isinstance(keypoints2, np.ndarray)
    assert isinstance(orient_agreement, float)
    assert isinstance(scale_agreement, float)
    ## START
    largest_set = [] #가장 많은 inlier이 들은 집합

    #print(keypoints1, keypoints2)
    #print(orient_agreement, scale_agreement)
    orient_agreement = orient_agreement / 180 * math.pi
    for i in range(10) : # 10번 반복
        rand = random.randrange(0, len(matched_pairs)) 
        choice = matched_pairs[rand] # matched_pairs 중 하나를 랜덤으로 선택

        orientation_i = (keypoints1[choice[0]][3] - keypoints2[choice[1]][3]) % (2 * math.pi) # 선택한 매치에 대해 orientation 계산
        scale_i = keypoints2[choice[1]][2] / keypoints1[choice[0]][2] # 선택한 매치에 대해 scale ratio 계산

        temp = []

        for j in range(len(matched_pairs)): # 다른 모든 match에 대해 계산
            if j != rand:
                # rand가 아닌 match에 대해 orientation 계산
                orientation_j = (keypoints1[matched_pairs[j][0]][3] - keypoints2[matched_pairs[j][1]][3]) % (2 * math.pi)

                # rand가 아닌 match에 대해 scale ratio 계산
                scale_j = keypoints2[matched_pairs[j][1]][2] / keypoints1[matched_pairs[j][0]][2]

                # orientation차이가 agreement보다 작은지 확인
                if (abs(orientation_i - orientation_j) < orient_agreement) or (abs(orientation_i - orientation_j) > (2 * math.pi) - orient_agreement):
                    # scale비율이 +-agreement 이내인지 확인
                    if( scale_i - scale_i * scale_agreement < scale_j < scale_i + scale_i * scale_agreement):
                        temp.append(j)# 둘 다 agreement하면 index를 temp에 저장
        
        if len(temp) > len(largest_set): # 가장 많은 match를 가진 temp를 largest_set에 저장
            largest_set = temp

    for i in range(len(largest_set)):#index로 저장한 배열을 다시 descriptor로 바꿈
        largest_set[i] = (matched_pairs[largest_set[i]][0], matched_pairs[largest_set[i]][1])
        
    ## END
    assert isinstance(largest_set, list)
    return largest_set



def FindBestMatches(descriptors1, descriptors2, threshold):
    """
    This function takes in descriptors of image 1 and image 2,
    and find matches between them. See assignment instructions for details.
    Inputs:
        descriptors: a K-by-128 array, where each row gives a descriptor
        for one of the K keypoints.  The descriptor is a 1D array of 128
        values with unit length.
        threshold: the threshold for the ratio test of "the distance to the nearest"
                   divided by "the distance to the second nearest neighbour".
                   pseudocode-wise: dist[best_idx]/dist[second_idx] <= threshold
    Outputs:
        matched_pairs: a list in the form [(i, j)] where i and j means
                       descriptors1[i] is matched with descriptors2[j].
    """
    assert isinstance(descriptors1, np.ndarray)
    assert isinstance(descriptors2, np.ndarray)
    assert isinstance(threshold, float)
    ## START
    ## the following is just a placeholder to show you the output format
    y1 = descriptors1.shape[0]#1번 그림 descriptor 개수
    y2 = descriptors2.shape[0]#2번 그림 descriptor 개수
    
    temp = np.zeros(y2)#1번그림과 2번그림의 유사도 저장할 공간

    matched_pairs = []#유사한 descriptor저장할 공간

    for i in range(y1):
        for j in range(y2):
            temp[j] = math.acos(np.dot(descriptors1[i],descriptors2[j]))#1번 그림 descriptor마다 2번 그림의 모든 descriptor의 유사도 검사해 temp해 저장
        
        compare = sorted(range(len(temp)), key = lambda k : temp[k])#temp값을 기준으로 index정렬
        
        if(temp[compare[0]] / temp[compare[1]] < threshold):#가장 유사한 값을 두번째로 유사한 값으로 나눈 ratio distance사용 
            matched_pairs.append([i,compare[0]])            #threshold이상이면 matched_pairs에 저장
    ## END
    
    return matched_pairs


def KeypointProjection(xy_points, h):
    """
    This function projects a list of points in the source image to the
    reference image using a homography matrix `h`.
    Inputs:
        xy_points: numpy array, (num_points, 2)
        h: numpy array, (3, 3), the homography matrix
    Output:
        xy_points_out: numpy array, (num_points, 2), input points in
        the reference frame.
    """
    assert isinstance(xy_points, np.ndarray)
    assert isinstance(h, np.ndarray)
    assert xy_points.shape[1] == 2
    assert h.shape == (3, 3)

    # START
    
    hc_xys = np.pad(xy_points,pad_width=((0,0),(0,1)), mode= 'constant', constant_values= 1)
    xys_p = h @ hc_xys.T #homography매트릭스와 연산
    z_cor = np.where(xys_p[-1:] == 0 , 1e-10, xys_p[-1:]) #z좌표가 0이라면 매우 작은 수로 대치
    hc_xys_p = xys_p/z_cor #z좌표로 나누어 평면으로 옮김
    xys_p = hc_xys_p[:-1, :] #z좌표 같으므로 제거
    xy_points_out = xys_p.T #transpose해 위치 표시

    
    # END
    return xy_points_out

def RANSACHomography(xy_src, xy_ref, num_iter, tol):
    """
    Given matches of keyponit xy coordinates, perform RANSAC to obtain
    the homography matrix. At each iteration, this function randomly
    choose 4 matches from xy_src and xy_ref.  Compute the homography matrix
    using the 4 matches.  Project all source "xy_src" keypoints to the
    reference image.  Check how many projected keyponits are within a `tol`
    radius to the coresponding xy_ref points (a.k.a. inliers).  During the
    iterations, you should keep track of the iteration that yields the largest
    inlier set. After the iterations, you should use the biggest inlier set to
    compute the final homography matrix.
    Inputs:
        xy_src: a numpy array of xy coordinates, (num_matches, 2)
        xy_ref: a numpy array of xy coordinates, (num_matches, 2)
        num_iter: number of RANSAC iterations.
        tol: float
    Outputs:
        h: The final homography matrix.
    """
    assert isinstance(xy_src, np.ndarray)
    assert isinstance(xy_ref, np.ndarray)
    assert xy_src.shape == xy_ref.shape
    assert xy_src.shape[1] == 2
    assert isinstance(num_iter, int)
    assert isinstance(tol, (int, float))
    tol = tol*1.0

    # START
    
    max_inliers = 0
    h = None
    N = xy_src.shape[0]
    for _ in range(num_iter):
        
        sample = np.random.choice(N,4,replace = False)
        src_sample = xy_src[sample]
        ref_sample = xy_ref[sample]
        
        
        A=[]
        for i in range(4):
            x,y = src_sample[i]
            x_p, y_p = ref_sample[i]
            A.append([x, y, 1, 0, 0, 0, -x_p*x, -x_p*y, -x_p])
            A.append([0, 0, 0, x, y, 1, -y_p*x, -y_p*y, -y_p])
        A = np.array(A)

        #At=0
        eig_val, eig_vec = np.linalg.eig(A.T.dot(A))#A의 고유값,고유벡터
        min_index = eig_val.argmin() #최소 고유값 인덱스
        #최소값 가지는 고유벡터를 3*3모양으로 다시만들음
        homography = np.array(eig_vec[:, min_index]).reshape((3, 3))

        #src를 구한 homography를 통해 projection
        xy_out = KeypointProjection(xy_src, homography)

        # 유클리드 거리 계산
        dists = np.sqrt(np.sum((xy_out - xy_ref)**2, axis=1))

        # inlier개수최대로 가지는 h구하기
        inliers_num = np.count_nonzero(dists <= tol) #tol보다 작은 distance가지는 것만 inlier
        if inliers_num > max_inliers:
            h = homography
            max_inliers = inliers_num

    # END
    assert isinstance(h, np.ndarray)
    assert h.shape == (3, 3)
    return h


def FindBestMatchesRANSAC(
        keypoints1, keypoints2,
        descriptors1, descriptors2, threshold,
        orient_agreement, scale_agreement):
    """
    Note: you do not need to change this function.
    However, we recommend you to study this function carefully
    to understand how each component interacts with each other.

    This function find the best matches between two images using RANSAC.
    Inputs:
        keypoints1, 2: keypoints from image 1 and image 2
            stored in np.array with shape (num_pts, 4)
            each row: row, col, scale, orientation
        descriptors1, 2: a K-by-128 array, where each row gives a descriptor
        for one of the K keypoints.  The descriptor is a 1D array of 128
        values with unit length.
        threshold: the threshold for the ratio test of "the distance to the nearest"
                   divided by "the distance to the second nearest neighbour".
                   pseudocode-wise: dist[best_idx]/dist[second_idx] <= threshold
        orient_agreement: in degrees, say 30 degrees.
        scale_agreement: in floating points, say 0.5
    Outputs:
        matched_pairs_ransac: a list in the form [(i, j)] where i and j means
        descriptors1[i] is matched with descriptors2[j].
    Detailed instructions are on the assignment website
    """
    orient_agreement = float(orient_agreement)
    assert isinstance(keypoints1, np.ndarray)
    assert isinstance(keypoints2, np.ndarray)
    assert isinstance(descriptors1, np.ndarray)
    assert isinstance(descriptors2, np.ndarray)
    assert isinstance(threshold, float)
    assert isinstance(orient_agreement, float)
    assert isinstance(scale_agreement, float)
    matched_pairs = FindBestMatches(
        descriptors1, descriptors2, threshold)
    matched_pairs_ransac = RANSACFilter(
        matched_pairs, keypoints1, keypoints2,
        orient_agreement, scale_agreement)
    return matched_pairs_ransac
