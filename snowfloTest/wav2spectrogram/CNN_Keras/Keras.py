'''
    1강: https://www.youtube.com/watch?v=cJpjAmRO_h8&t=39s&ab_channel=SKplanetTacademy

        pytorch, tensorflow, keras
                            인터페이스
          엔진       엔진

        api

    y = w * X + b
    
    종속변수 vs 독립변수: 원인을 놓고, 결과를 할 수 있는지.
        가중치 W는 알아서 설정을 할 것이지만, 원인 X를 가능한 많이 넣어줘야 함.

        dropout?
        - 대답을 잘하는 뉴런만 계속 사용하는데, 모든 뉴런이 학습을 사용하게 하기 위해서.
        over fitting?

    from keras.models import Sequential
    
    model = Sequential()  # 모델이 생김
    
    레고 3등분 = 딥러닝도 3등분
    머리          Network : 네트워크
    몸통          Object Function : 목표 함수 = 학습 목표
    다리          Optimizer : 최적화기 - 딥러닝 네트워크를 갱신
    
    3가지를 하나로 합치는 것 = 컴파일: 네트워크가 학습할 준비가 됬다!!
    
    모델의 3요소
    
        # 네트워크
        from keras.layers import Dense
    
        model.add(Dense(units=64, activation='relu', input_dim=100))  # 2개 -> 2층
        model.add(Dense(units=10, activation='softmax'))
        
            1. input X 를 바탕으로 예측값 Y' 를 계산
            2. objective function 에  Y 와 Y' 전달
        
        # 목표 함수 : loss function -> 낮게 하는 것을 목표
            1. 실제 정답 Y
            2. 내가 해답을 낸 답 Y'

            3. 1과 2의 차이를 계산하는 것이 중요함. detail 하게 설정
                             계산 결과를 optimizer 에게 -> network 갱신
        # 최적화기
            1. objective function 에서 들어온 오차를 바탕으로
                            network 갱신

        network -> objective function -> optimizer
            <------------------------------
                    서로 순환되는 관계
                    
        학습한 것은 파악완료, 하지 않은 것은 Random 값을 부름

    # 컴파일 - 네트워크를 학습할 준비가 됬다.
    model.compile(loss='categorical_crossentropy',
                  optimizer='sgd',
                  metrics=['accuracy'])  # metrics = 평가하는 항목
                  
    https://keras.io/applications/
        Xception (88 MB, 126)  # 용량, 층의 수
        ...
        
        mean_squared_error: 수치 예측 (회귀 문제)

        binary_crossentropy: 이중 분류
        
        categorical_crossentropy: 다중 분류
            -> 우리는 5 ~ 10 개의 명령어를 구별하기 때문에, 아마 이것 사용

    https://keras.io/optimizers/
        최적?
        
        좌 --- 목적지 --- 우
        
        속도, 방향이 중요        
'''


'''
    # 모델 구성하기
    from keras.models import Sequential

    # 모델 구성
    model = Sequential()  # 모델 생성  
    
    model.add(Dense(units=64, activation='relu', input_dim=100))  # 2개 -> 2층, 층 추가
    model.add(Dense(units=10, activation='softmax'))

    # 모델 엮기, 컴파일 - 학습 준비 완료
    model.compile(loss='categorical_crossentropy',
                  optimizer='sgd',
                  metrics=['accuracy'])  # metrics = 평가하는 항목  
                  
    # 모델 학습시키기 
    model.fit(X_train, Y_train, nb_epoch=5, batch_size=32)  # 필요한 데이터는 x, y
    
    # 평가 - 준비된 테스트셋으로 evaluate()
    
    # 예측 - predict()
'''

'''
    # 영상처리, 이미지 처리
       1. 픽셀: 1바이트 0 ~ 255
       
    # 데이터 준비
    (X_train, Y_train), (X_test, Y_test) = mnist.load_data()  # mnist: 아마존에서 줌
    X_train = X_train.reshape(60000, 784).astype('float32') / 225.0 # 60000개, 784바이트 28 * 28
    X_test = X_test.reshape(10000, 784).astype('float32') / 255.0  # 10000개, 784바이트 28 * 28
    
    784 바이트 6만개, 784 바이트 1만개 -> 1차원 배열
        reshape 로 개수 * 바이트 크기의 행렬로 변경함. 
        float32 로 정수 -> 실수, / 255.0 을 해줌 -> 0 ~ 1 사이의 수로 변경함. 데이터 정규화
        
        # 데이터를 정규화 해줘야 학습이 더 잘 됨.
        
    # one hot 인코딩?
    Y = 정답, 라벨값
    Y_train = np_utils.to_categorical(Y_train)
    Y_test = np_utils.to_categorical(Y_test)
    
    1 = 0 1 0 0 0 0 0 0 0 0
    7 = 0 0 0 0 0 0 1 0 0 0
'''

'''
    # 학습과정
    model.fit(x, y, batch_size=32, epochs=10)
    compile -> fit
    
    batch_size: 몇 번 풀고 update 를 할 것이냐
       update 를 한다 = network 를 갱신한다 = optimizer
       정답과 푼 답을 비교하는 과정 = object function == loss function
       
    메모리 용량, 학습 속도 등에 영향을 미침
    
    epoch: 반복횟수
        100 문항 1 번 = epoch 1
        100 문항 10번 = epoch 10
        
        훈련셋 : update o
        검증셋 : update x 
        
    one hot encoding: 따로따로 비교하려고 만든 것
    categorical_crossentropy: 따로따로 loss를 구하는 object_function
    
    다중 클래스: 모두 했을때 1 -> softmax (출력층), 성능이 가장 좋음 -> relu (은닉층) 
    
    total sample = data 개수 * epoch
    total network update = total sample / batch_size
    
    loss: 손실값, acc: 정확도
'''

'''
    # 채널
    1. 기하정보는 모두 동일함
    2. 색상정보가 모두 다르다
       Red
       Green
       Blue
       Alpha -> png 파일에서 형용, 투명도
'''

'''
    # MLP 다중 퍼셉트론 레이어
    준비 데이터 set: X, Y
    
    입력3, weight3*1, 출력1
    
    https://www.youtube.com/watch?v=36sjfxibME4&list=PL9mhQYIlKEheoq-M4EifTMPNWMw7poclK&index=3&ab_channel=SKplanetTacademy
    3:20 대 ???
    
    Dense(출력 뉴런 수, 입력 뉴런 수, 가중치 초기화 방법, 활성화 함수)
       출력 마다 입력에 weight = 곱연산 = weight = 출력 * 입력 
       
       hyper parameter tuning
'''

'''
    # CNN
    Conv2D(필터 수, 커널의 (행,열), 경계 처리 방법, input_shape(행,열,채널), 활성화 함수)
                                    padding
                                    
    feature map, 출력 이미지의 수 = 필터 수에 영향.
    
    컨볼루션 -> 컨볼루션 -> 맥스풀링
    
    img= width, height, channels
    
    -> flatten 1차원 벡터화
    
    https://www.youtube.com/watch?v=f5X0An5KLR4&list=PL9mhQYIlKEheoq-M4EifTMPNWMw7poclK&index=4&ab_channel=SKplanetTacademy
    ImageDataGenerator(rescale=1./255)
    
    fit vs fit_generator
    1. fit - 모두 로딩하고 시작
    
    2. fit_generator - python 구문의 generator
'''