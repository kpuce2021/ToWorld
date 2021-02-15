'''
    list: [ ]
    1. minus index: 뒤에서부터, 2. slice: 자르기
    3. list 내부 list 가능
    4. append: 원소 추가

    2-1. slicing: 콜론(:)을 이용하여 범위 지정
    2-2. a[0:1] 0 <= a < 1
    2-3. a[ :2] 0 <= a < 2
    2-4. a[4: ] 4 <= a < 끝
'''

listA = [10, 20, 30, 40, 50]
#         0   1   2   3   4

print("---------list---------")
print(listA[0:1])
print(listA[ :-2])
print(listA[2:3])

listA.append(60)
print(listA)

'''
    tuple: ( )
    1. read only list - 수정 불가
'''

tupleA = (10, 20, 30, 40, 50)

print("---------tuple---------")
print(tupleA)

'''
    dictionary: {key1: value1, key2: value2, key3: value3 ...}
    1. 다른 언어 hash, map과 구조 비슷
    2. 반드시 순서대로 들어가는 것이 아님
    3. key = 키, value = 값, items = 키와 값
'''

dictionaryA = {"Kano": 100, "anastasia": 1000, "sakura": 110}

print("A key == ", dictionaryA.keys())
print("A value == ", dictionaryA.values())
print("A items == ", dictionaryA.items())

'''
    String: ' ' or " "
    1. 문자열 내의 각각의 값 또한 문자열로 인식
    2. split()은 머신러닝 코드에서 문자열 데이터 전처리 
       split(,): ,를 기준으로 문자열 분리 -> 각 분리한 것을 리스트 반환
'''

'''
    type(data): 입력 데이터 타입 알려줌
    len(data): 입력 데이터의 길이 알려줌
    size(data): 모든 원소의 개수 알려줌  
    
    list(data) = 입력 데이터 리스트 반환
    str(data) = 입력 데이터 문자열 반환
    int(data) = 입력 데이터 정수 반환
'''

ifa = -1

if ifa > 0:
    print("ifa == ", ifa)
elif ifa == 0:
    print("ifa == ", ifa)
else:
    print("ifa == ", ifa)

'''
    for
    1. for variable in range()
    2. for variable in list
'''

print("for by range")
for data in range(0,10,2): # 시작, 끝, 증가수
    print("data = ", data)

print("for by tuple")
for data in tupleA:
    print(data)

'''
    list comprehension
    1. list 내에 for 문으로 특정 조건에 맞는 데이터를 list로 저장
'''

list_comprehension = [x**2 for x in range(5)]
# x^2 =  원소로 사용, for x in range(5) = 5번 반복
print(list_comprehension)

'''
    break, continue: 동일
'''

'''
    파이썬 함수
    1. def 함수명 (파라미터, 파라미터, ...):
    2. 파라미터에 데이터 타입 기술하지 않음 - 동일한 함수로 다양한 입력을 받을 수 있음.
       제네릭? (자바)
    3. return 값 1개 이상으로 반환 가능
'''

def multi_ret_func(x):

    return x+x, x+x+x, x+x+x+x

x1, x2, x3 = multi_ret_func(1)
print(x1, x2, x3)

c1, c2, c3 = multi_ret_func('c')
print(c1, c2, c3)

def double_ret_func(x):

    return x+x, x+x+x

d1 = double_ret_func(1) # 자동으로 tuple형으로 변환
print(d1)

'''
    default parameter
    1. 입력 파라미터가 들어오지 않을 경우, 이 파라미터를 사용 (미리 초기화)
       클래스, 생성자의 default 생성자의 느낌이라고 생각하면 됨
'''

def default_parameter(x = 2):
    return x**3

two = default_parameter()
three = default_parameter(3)

print(two, three)

'''
    mutable vs immutable
    1. 변함: list, dict, numpy
    2. 안 변함: 숫자, 문자, tuple 
       "숫자, 문자가 안 변한다는 것 -> 중요!!"
       
    lambda
    1. 한 줄로 함수를 작성하는 방법, 익명 함수 or 람다 표현식으로 불림
    2. 다른 함수의 파라미터로써 넣을 때 주로 사용
    3. 머신 러닝의 수치 미분, 활성화 함수 등을 표현할 때 사용
    
    함수명 = lamda 파라미터1, 파라미터2, ... : 대체되는 표현식
                                           = C언어의 #define의 느낌
    1. 입력된 파라미터를 모두 사용할 필요는 없음                                       
    2. 차후에 사용할 수학적 표현을 사용하는데 사용
'''

f = lambda x : x + 100

ff = lambda x : x + 50

print("lamda function")
for i in range(3):
    print(f(i)) # return i + 100, parameter = i

def lamda_parameter_func(x):

    return ff(x)*2

print(lamda_parameter_func(3))

print("lamda example")
def hello():
    print("hello Abe Nana")

def test_lamda(s, t):
    print("parameter1 == ", s, " parameter2 == ", t)

s = 100
t = 200

fx = lambda x, y : hello()
fy = lambda x, y : test_lamda(s, t)

fx(500,1000) # fx, fy 자체가 print라, 이를 또 다시 print하면 none 출력
fy(300, 600)

'''
    링크: https://www.youtube.com/watch?v=5Xy5Ju7hYo4&list=PLS8gIc2q83OjStGjdTF2LZtc0vefCAbnX&index=5&ab_channel=NeoWizard
    만약 재생목록이 왔을 경우: 5번째 강의
    
    class
    1. 선언: class 클래스이름:
    2. 생성자: __init__(self, name):
       self = 자바, C++의 this
    3. 파이썬 내부 멤버 변수, 메소드 = public
       기본적으로는 멤버 변수를 선언하지 않음
    
    4. 클래스 변수
       하지만 멤버 변수를 선언하는 경우 = 클래스 변수 = 자바의 static 변수?
       class 변수는 class 이름을 통해 접근, 객체 이름 접근 불가
    5. 클래스 메소드
       @classmethod 키워드를 통해 사용
       
       e.g
       @classmethod
       def getCount(cls):
           return cls.count
           
    6. 접근 지정자
       __를 사용하면 public이 아닌 private로 선언, default = public
    7. self
       외부함수와 클래스 내부함수의 이름이 동일할 경우, 
       단순히 외부 함수의 이름을 사용하면 외부 함수 호출
       self.함수 이름을 사용하면 클래스 내부 함수 호출
    
    exception
    1. try:, except:, finally:
       try , catch  , finally - 자바
       
    with
    1. 명시적으로 리소스 close()를 해주지 않아도 자동으로 close() 해주는 기능
    2. with 블록을 벗어나는 순간 자동으로 close
       e.g
    
       with open("경로", "w") as f:
          f.write("I'll try to be a good programmer")
          
    3. 기본 동작 open() -> read() or write() -> close()   
'''