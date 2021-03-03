import pyrebase

firebaseConfig={
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

# push data
userId = 'jF1s5Ch0hXfTc60l6y2jQhSkADV2'
fileName = '알파'


data = {'number': 5, 'checkKey' : 'false' }
# db.child(userId).child(fileName).push(data) # push new data의 발생
db.child(userId).child(fileName).set(data) # set -> 이걸로 다 밀어버림 발생 (제대로 넣어줘야 함)


'''
def realtimeDBTest():

    userId = 'jF1s5Ch0hXfTc60l6y2jQhSkADV2'
    fileName = "알파"

    return firebase.database().ref(userId+'/'+fileName+'/number').once('value').then(
        (snapshot) => {}
    )
print('fileNumber : ', realtimeDBTest())
'''

