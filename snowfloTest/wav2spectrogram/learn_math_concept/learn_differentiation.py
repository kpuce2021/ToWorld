'''
    미분
    1. 순간 변화율, 한 점에서 접점 기울기 -> why? 뭘 얻게
    lim 'x 변화량 -> 0' "(함수값 변화량) / (x 변화량)"
    2. 입력 x가 아주 조금 변하면, 함수 값은 얼마나 변하는가?
       = 함수 f(x)는 x의 변화에 얼마나 민감한가?
    3. 딥 러닝에 사용되는 미분
       f(x) = 상수 -> f'(x) = 0
       f(x) = ax^n -> f'(x) = n * ax^(n-1)
       f(x) = e^x -> f'(x) = e^x
       f(x) = ln(x) -> f'(x) = 1/x
       f(x) = e^(-x) -> f'(x) = -e^(-x) :: 체인룰
    편미분
    1. 입력 변수가 하나 이상인 다변수 함수에서,
    미분하고자 하는 변수 하나를 제외한 나머지 변수들은 상수로 취급하고, 해당 변수 미분
       = 변수가 여러 개 일지라도 1개만 변수로 취급함.
    2.  θf(x,y) / θx -> x에 대해서만 미분
    체인룰 (연쇄법칙)
    1. 합성함수가 이 chain rule 에 속함
       f(x) = e^(3x^2)
          3x^2 = t -> e^t

          Θf   Θt    Θ(e^t)   Θ(3x^2)
          -- * --  =   ---   *   ---    =   e^t * 6x
          Θt   Θx      Θt        Θt

       f(x) = e^(-x)
          -x = t -> e^t
          t = -x -> -1
          -1 * e^t, t = -x -> -e^(-x)
          
    ---> 가중치 업데이트, 오차 역전파에 사용
'''

'''
    수치미분: 수학공식을 쓰지 않고, C/파이썬 등을 이용하여, 주어진 입력 값이 미세하게 변할 때,
            함수 값 f는 얼마나 변하는지를 계산하는 것
            
            1. 미분하려는 함수 정의
            2. 극한 개념을 구현하기 위해 Δx는 작은 값으로 설정
            3. 분자/분모 구현         
'''

import numpy as np

# 입력 변수가 1개인 수치미분
def numerical_derivative(f, x):  # 함수명, 입력값
    # 함수 f는 def, lambda 등으로 정의된 함수
    # x는 미분 값을 알고자하는 입력 값

    delta_x = 1e-4  # 10^(-4) 정도는 프로그래밍에서 0에 수렴한다고 알려짐

    return (f(x + delta_x) - f(x - delta_x)) / (2 * delta_x)
    # return 값을 (f(x + delta_x) - f(x)) / delta_x 로 하지 않는 이유
    # delta_x의 경우보다 2 * delta_x의 경우가 좀 더 오차가 적음
    # 위의 두 식이 같을 수 있는 이유: return 값을 도함수로 풀면,
    # (f(x + delta_x) - f(x)) / delta_x 와 일치함.

# 입력 함수
def func1(x):
    return x**2

print("3에서 x**2의 미분값: ", numerical_derivative(func1,3))
# f = func1
# f(x + delta_x) = (func1(3 + delta_x) - func1(3 - delta_x)) / 2 * delta_x

def func2(x):
    return 3*x*(np.exp(x))
    # 3x * np.exp(x)
    #       e^x
    # 3xe^x

print("2에서 3xe^x의 미분값: ", numerical_derivative(func2, 2))

# 다변수 함수 수치미분
# 입력 변수에 맞춰 각각 수치미분을 수행,
# 단 입력 변수는 서로 독립적이어서 수치미분 또한 변수의 개수만큼 개별적 수행

def multi_numerical_derivative(f, x):  # f: 다변수 함수, x: 모든 변수를 포함한 numpy
                                    # 함수의 입력 변수 수에 따라 numpy의 크기가 변함
    delta_x = 1e-4
    grad = np.zeros_like(x) 
    # 수치미분 값을 저장하는 변수 grad, np.zeros_like를 이용해 numpy 크기만큼 받되, 모두 0으로 초기화

    # print("debug 1. initial input variable = ", x)  # numpy형으로 입력
    # print("debug 2. initial input grad = ", grad)  # 0으로 초기화
    # print("========================================================")

    it = np.nditer(x, flags=['multi_index'], op_flags=['readwrite']) #, op_flags=['readwrite'])
    # 이터레이이터
    # numpy.nditer: https://kosb.tistory.com/42
    # https://numpy.org/doc/stable/reference/generated/numpy.nditer.html
    # 첫 번째 원소를 가리키므로 while 문을 통해 끝가지 접근이 가능케 함
    while not it.finished:  # 존재하는만큼 (끝까지)
        idx = it.multi_index  # numpy index 번호

        # print("debug 3. idx =", idx, " x[idx] = ", x[idx])
        # 3. idx가 빈 튜플로 나옴 -> 입력을 numpy가 아닌 일반 tuple로 했음...
        tmp_val = x[idx]  # numpy 타입은 mutable 이므로 원래 값 보관
                          # mutable 타입은 반드시 원본 값을 보관하는 임시 변수 선언

        # 편미분: (f(x + delta_x) - f(x - delta_x)) / (2 * delta_x)
        #              1                   2               3
        x[idx] = float(tmp_val) + delta_x
        fx1 = f(x)  # f(x+delta_x) 1

        x[idx] = float(tmp_val) - delta_x
        fx2 = f(x)  # f(x-delta_x) 2
        grad[idx] = (fx1-fx2) / (2*delta_x)  # (1 - 2) / (3)

        # print("debug 4. grad[idx]", grad[idx])
        # print("debug 5. grad = ", grad)
        # print("========================================================")

        x[idx] = tmp_val
        it.iternext()

    return grad  # numpy 형식

# numpy 파트 + iterator 공부 + lambda 공부
# 중간중간 print() 함수를 이용하여, debug를 한다면, 현재 어떤 값이 입력되고 나오는지 확인 가능

# 구체적 예시
def func3(input_obj):  # input_obj = vector나 matrix를 나타내는 numpy 객체
                       # 수치미분에서 받는 2번째 파라미터가 numpy형이기 때문
    # 2변수 함수이므로 2개
    x = input_obj[0]  # x가 첫번째
    y = input_obj[1]  # y는 두번째
    z = input_obj[2]
    w = input_obj[3]
    return (2*x + 3*x*y + np.power(y,3) + w*x + x*y*z + 3*w)

input = np.array([1.0, 2.0, 3.0, 4.0])  # 입력 numpy = np.array(), ([1.0], [2.0])
print("2*x + 3*x*y + y**3의 미분값: ", multi_numerical_derivative(func3, input))

'''
    버그가 나면, 프로그램의 흐름을 다시 한 번 살펴보자.
'''