import pyrebase

'''
    Building wheel for pycryptodome (setup.py) ... error

    ERROR: Command errored out with exit status 1

    https://stackoverflow.com/questions/53461316/pyrebase-install-on-windows-python-3-7-fails

    1. jws 직접 설치 및 encoding utf8
    2. setup.py 직접 구동
    3. pyrebase4로 설치
    4. 모듈이름과 코드이름 동일시 하지 않을 것
'''

firebaseConfig = {
    'apiKey': "AIzaSyA-WnQXEGePs3e1fr_dl3WBMyoXe9BMvDs",
    'authDomain': "kpu-capstone---toworld.firebaseapp.com",
    'databaseURL': "https://kpu-capstone---toworld-default-rtdb.firebaseio.com",
    'projectId': "kpu-capstone---toworld",
    'storageBucket': "kpu-capstone---toworld.appspot.com",
    'messagingSenderId': "837067207822",
    'appId': "1:837067207822:web:a906a4af8a62dc99bac5df",
    'measurementId': "G-RK098Q1GW1"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

data={'age':40,'address':'New York','employed':True,'name':'John Smith'}
db.child('people').child('person').push(data)