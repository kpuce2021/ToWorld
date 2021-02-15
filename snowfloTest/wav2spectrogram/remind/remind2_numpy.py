'''
    numpy: 머신러닝 구현시 필수로 사용되는 라이브러리
    1. pip install 커맨드를 이용해 설치
       numpy, pandas, matplotlib, tensorflow ...
       유명 머신러닝 프레임워크도 설치 가능
    2. import 방식
       2-1. import numpy -> full name 이용 "numpy"
       2-2. import numpy as np -> nickname 이용 "np"
       2-3. from numpy import exp -> . 사용하지 않고 바로 사용 (exp만 사용)
       2-4. from numpy import * -> 모두 사용
       
    3. 벡터, 행렬 등을 표현 및 연산하는 라이브러리
       list와 비슷해보임

       list간의 합 연산 = 행렬의 합 연산 x, list 간의 append 연산
       list가 아닌 np.array를 사용할 것
       
    4. 머신러닝/딥러닝을 위해서는 numpy를 이용한 행렬 연산이 매우 중요
    
    vector
    1. 1차원
    2. numpy.array([ , , ... , , ])를 이용
    3. vector의 사칙 연산 = 각 원소별로 연산
    
    matrix
    1. 2차원
    2. numpy.array([ , , ... ], [ , , ... ], ... ,[ , , ...])를 이용

    공통 내용
    1. numpy.shape = 형상 출력
    2. numpy.ndim = 차원 출력
    3. numpy.reshape(row ,col) = 행렬간 형상 변환

    dot product = 행렬값
    1. np.dot(A,B)
    2. A = 행렬, B = 행렬, A의 열과 B의 행이 일치하여야만 연산 가능
    3. 같지 않다면 reshape 혹은 transpose 등을 사용하여 형 변환을 한 후 행렬 곱 실행해야 함
    4. 행렬 사칙 연산의 한계 극복 = 기존의 행렬 사칙 연산은 행렬 크기가 동일
       64 * 64 . 64 * 256 . 256 * 512 . 512 * 64 . 64 * 10 = 64 * 10

    링크: https://www.youtube.com/watch?v=dnJ3JESmBkE&list=PLS8gIc2q83OjStGjdTF2LZtc0vefCAbnX&index=7&ab_channel=NeoWizard
    broadcast
    1. 크기가 다른 행렬간에 사칙연산을 할 수 있도록 하는 기능
       차원이 작은 쪽이 큰 쪽의 행 단위로 반복적으로 크기를 맞춤
    2. 행렬곱 연산에는 적용되지 않음, 오로지 행렬 사칙 연산에만 적용
       행렬 곱과 행렬 사칙연산은 다른 것
    
    transpose: 전치행렬
    1. 행과 열을 swap (변경)
    2. 벡터의 경우, 원본은 그대로 유지됨 - 계속 벡터
       행렬로 변환시키고자 한다면 위에서 기술한 reshape를 사용
'''

# 전치행렬
import numpy as np
#from numpy import np


matA = np.array([[1,2],[3,4]])

print(matA)

matB = matA.T # 전치행렬 transpose 명령어: .T
print("기존 행렬 A")
print(matA)
print("전치 행렬 B")
print(matB)

'''
    list처럼 행렬도 indexing, slicing 모두 사용 가능

    indexing
    1. 행렬 원소 접근 A[0, 0], A[2, 1] ...
       , 기준 좌측: 행, 우측: 열
    
    slicing
    1. 행렬 범위 지정 A[0: -1, 1: 2]
       행 0(처음 행) ~ -1(맨 끝 행)까지
       열 1(2열) ~ 2(3열)까지
       
    iterator
    1. C++, Java처럼 next() 메소드 사용
       자바: hasNext(): 다음이 존재? boolean
            next(): 다음 가져옴 Object
    2. 행단위 접근, 자동 증가 안되어 while과 사용
'''

'''
    concatenate
    1. 기존 행렬에 행 or 열 추가 (행 크기 or 열 크기 맞춰야 함)
    
    loadtxt()
    1. separator: 분리자 로 구별된 파일에서 데이터를 읽기 위한 함수
    2. delimiter = ',' : 분리자
    
    rand()
    1. vector or matrix 로 사용, 0과 1 사이 램덤으로 매칭
    2. 가중치, 바이어스 임의 설정에 사용
    
    sum(), exp(), log()
    1. 벡터는 값이 하나가 아니기 때문에 각각의 원소에 대해 모두 체크
    
    argmax()
    1. 최댓값이 있는 곳의 index 리턴
    
    argmin()
    1. 최솟값이 있는 곳의 index 리턴
    
    # axis = 0 : 열 단위로 찾겠다.
    # axis = 1 : 행 단위로 찾겠다.
    
    ones()
    1. 주어진 형상의 행렬을 모두 1로
    
    zeros()
    1. 주어진 형상의 행렬을 모두 0로
    
    matplotlib
    1. 입력 데이터의 분포와 모양을 먼저 그려보고, 데이터의 특성과 분포를 파악한 후 알고리즘 적용
    2. 데이터의 시각화를 위해 matplotlib 사용
    3. 일반적으로 line plot, scatter plot 등을 사용
'''

A = np.array([ [10,20,30], [40,50,60]]) # 2 * 3

row_add = np.array([70, 80, 90]).reshape(1, 3) # 1 * 3 으로 변환 A와 열 크기 동일

column_add = np.array([1000, 2000]).reshape(2, 1) # 2 * 1 으로 변환 A와 행 크기 동일

RA = np.concatenate((A,row_add), axis=0)
print(RA)

CA = np.concatenate((A,column_add), axis=1)
print(CA)

loaded_data = np.loadtxt('loaded_text.txt', delimiter=',', dtype=np.float32)
x_data = loaded_data[ :,0:-1]
t_data = loaded_data[ :,[-1]]

print("x_data.ndim = ", x_data, "x_data.shape = ", x_data.shape)
print("t_data.ndim = ", t_data, "t_data.shape = ", t_data.shape)