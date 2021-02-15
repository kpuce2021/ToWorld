'''
    머신러닝: 인공지능을 구현하는 하나의 방법
    1. 데이터를 이용하여 특성과 패턴을 파악 -> 미지의 데이터에 대한 그것의 미래 결과 (값, 분포)를 예측
       = regression: 회귀
    2. training data로 학습, 미지의 데이터 test data로 검증
       = 특성과 상관관계 파악
        
    지도학습
    1. 회귀
    2. 분류
    비지도학습
    1. 군집화
    
    regression
    1. training data의 상관 관계를 파악 -> 그래프
    2. 가중치 w, 바이어스 b를 찾는 것이 학습
       기울기    y절편
    3. 오차 error: 정답 t와 예측값 y의 차이 = loss function
       크다면 w와 b가 잘못됨, 작다면 w와 b가 잘 된 것이고 미래값 예측이 정확함
       오차의 계산: (t - y)^2
       -> 양수 + 음수의 합으로 0이 될 가능성 배제. ^2이기 때문에 값이 커져 오차방지에 큰 도움
                             n
       loss function = (1/n) Σ  [t_i - (Wx_i + b)]^2 = 모든 데이터에 대한 평균 오차값
                            i=1          함수값

                            x와 t는 training data에서 입력값과 결과값으로 주어지는 데이터이므로
                            변수는 w와 b 2가지가 됨.
    Error 값이 작다면 뒤에 값을 예측한 것의 오차도 작을 것임.
    
    gradient decent algorithm: 경사하강법
    0. 손실함수 모양 파악: regression 의 경우 포물선의 형태로 생성
       계산을 위해 bias = 0 으로 가정, weight 만 변화
    1. 임의의 가중치 w를 선택, 미분값이 작아지는 방향으로 진행하여 loss function 의 최솟값을 찾는 방법 = 경사하강법
    2. 양수일 경우 감소, 음수일 경우 증가

                ΘE(W,b)
    3. w = w - α ------ , α = 학습율   W에 대한 편미분
                  ΘW

                ΘE(W,b)
    4. b = b - α ------ , α = 학습율   b에 대한 편미분
                  Θb

    5. input -> 손실함수 계산 -> 손실함수 값 -> 최소값? - yes -> 종료
                update W, b => repeat < - no -
'''

# linear regression
'''
    순서
    1. 입력 x와 정답 t를 분리
       slicing 혹은 list comprehension 등을 이용하여 x와 t를 numpy 데이터형으로 분리
    2. y = Wx + b
       W와 b는 numpy.random.rand 를 이용하여 0과 1사이로 정의
    3. regression 손실함수
       regression - 3. loss function 참조
    4. 학습율 α
       learning_rate = 1e-3 or 1e-4 or 1e-5 ...
    5. 가중치 W, 바이어스 b
       loss function 을 lambda 혹은 def 로 정의한 후, W와 b를 구함
       
    X * W + b = Y
    입력 x, 정답 t, 가중치 W 모두 행렬로 나타낸 후, 행렬 곱을 이용
    
    x_i*W + b
'''

import numpy as np

# 학습 데이터
x_data = np.array([1,2,3,4,5]).reshape(5,1)  # 5*1
t_data = np.array([2,3,4,5,6]).reshape(5,1)  # 5*1
# raw_data = [[1,2],[2,3],[3,4],[4,5],[5,6]] -> 이런식이라면 어떻게 처리할지?
print("x_data.shape = ", x_data.shape, ", t_data.shape = ", t_data.shape)

# 임의의 직선 y = Wx + b 정의
W = np.random.rand(1,1)  # random 으로 초기화
b = np.random.rand(1)  # random 으로 초기화
print("W = ", W, "W.shape = ", W.shape, "b = ", b, "b.shape = ", b.shape)

# 손실함수 E(W,b) 정의
def loss_func(x, t):
    y = np.dot(x, W) + b  # np.dot? = numpy array 를 곱할 때 사용 W*x

    return (np.sum( (t-y)**2 )) / (len(x))

# 수치 미분 함수
def numerical_derivative(f, x):  # 함수명, 입력값
    # 함수 f는 def, lambda 등으로 정의된 함수
    # x는 미분 값을 알고자하는 입력 값

    delta_x = 1e-4  # 10^(-4) 정도는 프로그래밍에서 0에 수렴한다고 알려짐
    grad = np.zeros_like(x)

    it = np.nditer(x, flags=['multi_index'], op_flags=['readwrite'])

    while not it.finished:
        idx = it.multi_index
        tmp_val = x[idx]
        x[idx] = float(tmp_val) + delta_x
        fx1 = f(x)

        x[idx] = tmp_val - delta_x
        fx2 = f(x)
        grad[idx] = (fx1 - fx2) / (2*delta_x)

        x[idx] = tmp_val
        it.iternext()

    return grad

# 손실함수 값 계산 함수
def error_val(x, t):
    y = np.dot(x, W) + b  # np.dot? = numpy array 를 곱할 때 사용 W*x

    return (np.sum( (t-y)**2 )) / (len(x))

# 결과 예측 함수
def predict(x):
    y = np.dot(x, W) + b

    return y

# 학습율 a
learning_rate = 1e-2  # 발산하는 경우, 1e-3, 1e-6 등으로 변경

# 함수
f = lambda x : loss_func(x_data, t_data)  # 손실 함수
print("Initial error value = ", error_val(x_data, t_data), "Initial W = ", W, "\n", ", b = ", b )

for step in range(8001):
# https://www.youtube.com/watch?v=Aw-E-jw3WaE&list=PLS8gIc2q83OjStGjdTF2LZtc0vefCAbnX&index=15&ab_channel=NeoWizard
    W -= learning_rate * numerical_derivative(f, W)  # why?

    b -= learning_rate * numerical_derivative(f, b)  # why?

# debug code
    if (step % 400 == 0):
        print("step = ", step, "error value = ", error_val(x_data, t_data), "W = ", W, "b = ", b)

print(predict(43))

'''
    1. 입력 데이터 수에 따라서 가중치 결정
       각각 가중치가 설정됨
       w1 x + w2 y + w3 z + ... + b
    2. multi code 는 일단 생략
'''

'''
    1. Classification
       Training Data 특성과 관계 등을 파악 한 후에
       미지의 입력 데이터에 대해서 결과가 어떤 종류의 값으로 분류 될 수 있는지를 예측
       e.g) 스팸, 암 ...
    2. Logistic Regression
       Training Data 특성과 분포를 나타내는 최적의 직선
       그 직선을 기준으로 데이터를 위(1) or 아래(0) 등으로 분류 -> 정확도가 높은 알고리즘
       ---> Deep Learning 에 있어 기본 Component 로 사용 
       
    3. Sigmoid: 출력이 0 or 1 -> 0과 1만 나오는 Sigmoid 사용 가능
    
    input -> Regression -> Classification -> output
                Wx + b          sigmoid (확률)
                
    4. 결과가 0 or 1 이므로 새로운 loss function 이 필요함.
       cross-entropy 를 이용
                  n
       E(W,b) = - Σ  { t_i log(y_i) + (1 - t_i)log(1-y_i)}
                 i=1
       
       - cross-entropy 를 유도
       
          0일 확률 vs 1일 확률
             p         1-p
       
       다수의 입력 x에 대해 정답 t가 발생할 확률: 우도 함수 L (가능도 함수)
                 n                n
       L(W,b) =  Π p(C=t_i|x_i) = Π (y_i)^(t_i) * (1-y_i)^(1-t_i)
                i=1              i=1
                
       우도 함수 = 가능도 함수 = 확률질량함수
       https://m.blog.naver.com/mykepzzang/221568285099
       0 <= p <= 1
       확률질량함수: 고정된 p(모수) -> 시행횟수 -> 확률
       우도함수: 고정된 시행횟수 -> p(모수) -> 가능도
       ---> 최대 우도 추정법: 고정된 시행 횟수에 모수 p를 대입해 가장 높은 값이 데이터를 가장 잘 설명함.
       * 주의: 우도 함수 != 확률 함수, 이유: 다 더해도 1이 아님
       
       이미 아는 모수 -> 확률함수 -> 확률
       관측된 데이터 (데이터 셋) -> 우도함수 -> 주어진 데이터를 가장 잘 표현하는 모수
       
       곱셈 형태의 우도 함수에서 -> 양변 로그 -> cross-entropy 생성
       
       결론: W, b를 구하는 것이 목적임.
       손실함수 내부의 delta: 1e-7 -> log 의 무한대 발산 방지
       
       multi의 경우
       9 * 2 = 9개의 데이터 2개의 input, 2 * 1 = 2개의 input 에대한 W
       
       (9 * 2) * (2 * 1) = 9 * 1 :: 2개의 가중치가 반영된 9개의 결과값 = 정답과 비교  
'''