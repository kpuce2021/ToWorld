'''
    일반적 신경망

    한 개의 입력층 -> 여러 은닉층 -> 최종 출력층 -> 손실함수
        손실함수가 최소가 되도록 weight, bias 업데이트
    
    CNN 신경망

    일반적 신경망과 동일하지만,
    은닉층이 '여러 컨볼루션층과 완전 연결층' 으로 변경

    컨볼루션층
    conv, relu, pooling
    
    conv = 가중치의 집합체인 다양한 필터와 컨볼루션 연산을 통해 입력데이터의 특징을 추출
    입력 데이터 A1 * filter1 + b2 -> 입력 데이터 A1 특징 추출
       - 입력 데이터 특징 추출
       입력 데이터: 4 * 4, 필터 3 * 3
       컨볼루션 연산: 필터를 일정간격(스트라이드)로 이동해 가며, 
                    입력데이터와 필터에서 대응하는 원소끼리 곱한 후 그 값들을 모두 더해주는 연산
                    
                    1. 필터내 모든 데이터와 매칭되는 값을 곱하고 모두 더함
                    2. 스트라이드(필터 이동 간격)으로 이동 -> 1을 수행
                    
                    1 -> 2 를 결과가 나올 때까지 반복함. 
                    input 크기, filter 크기, stride 를 잘 파악하여 "크기"를 잘 알아야 함

                    relu
                    0보다 크면 그대로, 0보다 작으면 0으로

                    pooling
                    max, min, average 중 하나를 사용, 대부분 max pooling 을 사용
    
    
    activated function - e.g relu
    0보다 크면 그대로, 0보다 작으면 0으로
    
    
    pooling
    입력 정보를 최댓값, 최소값, 평균값 등으로 압축하여 데이터 연산량을 줄여주는 역할
       - max pooling: 가장 큰 값
       - min pooling: 가장 작은 값
       - average pooling: 평균 
       
    padding
    컨볼루션 연산을 수행하기 전에 input 데이터 주변을 특정 값으로 채우는 것 e.g 0으로
       - 컨볼루션 연산을 지속적으로 하다보면, 크기가 너무 작아짐.
       - 이를 방지하기 위해 padding 을 적용 -> 원본 데이터와 동일한 크기를 얻을 수 있음.

    실제 연산
    입력 데이터: (H, W), 필터: (FH, FW), 패딩: P, 스트라이드: S

    출력 데이터: OH = (H + 2P - FH) / (S) + 1
               OW = (W + 2P - FW) / (S) + 1
               
    filter 를 통해 데이터의 특징을 추출하는 원리
       = 필터라는 것은 가중치(weight) 집합체
       = 딥러닝 목표는 최종적으로 손실함수가 최소가 되도록 가중치를 업데이트
       = 필터를 업데이트 한다는 말은 가중치를 업데이트 한다는 말과 동일

       - 가로 필터, 대각선 필터, 세로 필터
           111       001        001
           000       010        001
           000       100        001
           
       - 스트라이드, 패딩, 바이어스
       - 필터 수 만큼 pooling 값이 나옴.
          각각의 pooling 값을 비교 -> 데이터 안에 필터의 특징(성분)이 많이 포함되어 있는 것을 의미 (클수록)
          
       - 결과: 대각선 필터 > 가로 필터 = 세로 필터
       
       컨볼루션층1           -> 컨볼루션층2 -> 컨볼루션층3 -> 완전연결층        -> 출력층
       tf.nn.conv2d()                                   3차원 -> 1차원       입력받은 값을 0 ~ 1 사이로
       tf.nn.relu()                                     평탄화 작업          총합은 항상 1
       tf.nn.max_pool()                                 tf.reshape()       tf.nn.softmax()

       tf.nn.conv2d(input, filter, strides, padding, ...)

           input = [batch, in_height, in_width, in_channels]
           input = [100, 28, 28, 1] : 100개의 batch 로 묶은 28 * 28 크기의 흑백 이미지
    
           filter = [filter_height, filter_width, in_channels, out_channels]
           filter = [3, 3, 1, 32] : 3 * 3 input channel 이 1개, 필터 개수가 32개
           
           in_channels = input data 의 "채널"? 수
              - 데이터가 들어오는 통로, 입력 채널 1 = 데이터 통로 1, 입력 채널 32 = 데이터 통로 32
              
           strides = [1,1,1,1]
                   = [batch, height, width, depth] ???
              - 컨볼루션 적용을 위해 1칸씩 필터를 이동함
    
           padding = 'VALID' : 연산 공식에 따라 축소된 데이터 출력
           padding = 'SAME' : 입력 데이터와 크기가 같도록 자동으로 0으로 패딩

       tf.nn.max_pool(value, ksize, strides, padding, ...)
       
           value = [batch, height, width, channels] : 일반적으로 relu 를 통과한 출력결과

           ksize = [1, height, width, 1]
           ksize = [1, 2, 2, 1] : 2 * 2 데잍터 중에서 가장 큰 값 1개를 찾아 반환하는 역할
                                    2칸씩 이동
                                    [1, 3, 3, 1] : 3칸씩 이동

           strides = [1, 2, 2, 1] : 2칸씩 이동
                   = [batch, height, width, depth] ???

           padding = 최댓값을 뽑기에는 데이터가 부족한 경우, 주변을 0 등으로 채움
                   = 7 * 7 이 왔을 때, 2 * 2 로 검색한다면 부족
                   = padding = 'SAME' 으로 가능

    1. 입력 데이터, 정답 데이터 분리
        one_hot encoding???

        train image shape = (55000, 784) : 55000 개의 데이터, 784 픽셀
        train label shape = (55000, 10) : one_hot encoding 으로 저장된 10개 라벨
        
    2. 학습율, 반복횟수, 한 번에 입력으로 주어지는 개수
         a    epochs           batch_size

       입력과 정답을 위한 플레이스홀더 정의
       tf.placeholder(tf.float32, [None, 784])
       tf.placeholder(tf.float32, [None, 10])

       입력 데이터 reshape: 784 pixels = 28 * 28 
          28 * 28 * 1 : 28 * 28 을 가지는 흑백 이미지 "1: 흑백"
          A1 = X_img = tf.reshape(x, [-1, 28, 28, 1])
          
    3. 필터와 바이어스
       F2 = 필터, b2 = 바이어스
       stddev = 표준편차

       (28 * 28 * 1) * (1 * 32) -> 28 * 28 * 32
       padding = 'SAME' : 동일값 유지

       A1 * F2 = input 과 filter 컨볼루션 연산
               = C2
               C2 + b2 = 컨볼루션 연산 + bias
                       = -> relu로 보내면 = Z2

       Z2 -> pooling (max, min, average)
       
    4. 완전연결층: 4 * 4 크기를 가진, 128 개의 activation map -> 평탄화
       tf.reshape(A4, [-1, 128 * 4 * 4])
       input: A4 (이전 max_pooling 값 128 * 4 * 4) # 2048 개의 노드

       1 * 2048

    5. 출력층: [128 * 4 * 4, 10] stddev = 표준편차
       가중치 W와 바이어스 b를 정의
       
       (1 * 2048) * (2048 * 10) = 2048 개의 노드가 10 개의 라벨링과 연결
       Z5: tf.matmul(A4_flat, W5) + b5 = 선형회귀 값

       -> tf.nn.softmax(Z5) = 0 ~ 1 사이값, 총 합 = 1

    6. 손실함수
       - 경사하강법을 이용했지만 성능 개선을 위해 AdamOptimizer 을 사용
'''