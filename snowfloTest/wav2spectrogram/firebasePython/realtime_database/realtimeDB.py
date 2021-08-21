import pyrebase

# windows - korea pyrebase install - https://m.blog.naver.com/vvv1ct0r/220930787642
# 주의사항: anaconda cmd 에서 실행할 것 --> 실패

# https://jacegem.gitbooks.io/today-i-learned/content/doc/install-pyrebae-windows.html  --> 성공

# UnicodeDecodeError 'cp949' codec can't decode .... illegal multibyte sequence
# 에러 해결방안? --> 안 해봄
# 출처: https://daewonyoon.tistory.com/296 [알락블록]

firebaseConfig={
    "apiKey": "AIzaSyAsKDHA2A34HvEmIVRGwo2QD7vUYPv6r8o",
    "authDomain": "kpu2021mk3-220df.firebaseapp.com",
    "databaseURL": "https://kpu2021mk3-220df-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "kpu2021mk3-220df",
    "storageBucket": "kpu2021mk3-220df.appspot.com",
    "messagingSenderId": "783105378158",
    "appId": "1:783105378158:web:69fbd578d1062e0626237f",
    "measurementId": "G-Y6BRDGK41G"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()


# auth = firebase.auth()
# storage = firebase.storage()

# push data
# user_data = {"userId":"g175151@gmail", "result":"결과"}
# db.push(user_data)

# create your own key

userEmail = "saddummy@gmail"
result_data = {"checkKey":"true", "result":"결과"}
db.child(userEmail).child("result").set(result_data)



# userId = 'jF1s5Ch0hXfTc60l6y2jQhSkADV2'
# fileName = '알파'
#
# data = {'number': 5, 'checkKey' : 'false' }
# # db.child(userId).child(fileName).push(data) # push new data의 발생
# db.child(userId).child(fileName).set(data) # set -> 이걸로 다 밀어버림 발생 (제대로 넣어줘야 함)

'''
def realtimeDBTest():

    userId = 'jF1s5Ch0hXfTc60l6y2jQhSkADV2'
    fileName = "알파"

    return firebase.database().ref(userId+'/'+fileName+'/number').once('value').then(
        (snapshot) => {}
    )
print('fileNumber : ', realtimeDBTest())
'''

