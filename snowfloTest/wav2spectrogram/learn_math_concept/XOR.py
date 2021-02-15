'''
    1. and
    2. or
    3. nand
    4. xor

    입력 데이터 = x1, x2 로 2가지 이며, 출력 데이터 = 0, 1 인 training data 와 개념적으로 동일

    external function
    - sigmoid
    - numerical_derivative

    logicGate class
    - init
    - loss_func
    - error_val
    - train
    - predict

    usage
    - xdata
    - tdata
    - AND_obj = LogicGate("AND_GATE", xdata, tdata)
'''

import numpy as np

xdata = np.array([[0,0],[0,1],[1,0],[1,1]])
tdata = np.array([0,0,0,1])

# AND_obj = logicGate("AND_GATE", xdata, tdata)  # 위에서 설명한 logicGate class

'''
    xor
    
x1    nand  
               and 의 조합
x2    or

nand: regression -> classification
                                        and: regression -> classification
or: regression -> classification

이전 게이트의 출력 -> 다음 게이트의 입력 -> ... -> 최종 출력 (딥러닝의 기본적인 아이디어)
'''