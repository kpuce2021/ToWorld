# 1차 시도

from firebase_admin import credentials, db
import firebase_admin
'''
# fb_app = firebase.FirebaseApplication('https://kpu2021mk3-220df-default-rtdb.asia-southeast1.firebasedatabase.app/', None)
# result = fb_app.get('/users', None)
# print(result)

cred_data = {
  "type": "service_account",
  "project_id": "kpu2021mk3-220df",
  "private_key_id": "76edf741d664815f9f738f88cfffa07d8bf398f3",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCZDUpoOkWyi+Y3\nliTvycZATGjskKiZ3Ab4OFEcVGn5uoAUZO2AOFJwyN4DhjUqEiwYfN3OyxNxXND7\nOgxVeUlKs0UA7kzLnGzlsK6xGNkrKucsxeotmkAAA20eMdAebFnsRTfHkwXAfVVU\nYzOTar/2kBheVLA2zEGBevTeo2IBV0cSBbInW0VezKa1y3oUaFj5TfcBkzqaVxBH\n8ifS7w3dn+sREnXkF66DvxV8CuhJ5n+ZF21SvZw8P26Bvu2G16p9IrIjRxMQD3Or\nfDCVj9GUHntosH9Y0CtIeyzKfQDTwzEHLi6Nfxxt2/2nD5fBs4pZv/ZobLUDX18r\nxohRQf6lAgMBAAECggEAQVc+O+8c0FQPrg2IqWKAI/U7GjvL7xvTUedhIXIcaEQp\n6AsKpiHleEcZGXITgmmNr8qnO2DRZSVWBttKZrdIBf8w52vVF1wp1YmvmuXb2SUQ\n2rmH934R8q+Dx09G5aYmYctPPAHVg88+Pa+4VihN2eq8rJEFRe+/y5J9tgsUjTNX\nmqJeZRNNnT6cv8ptrrVj5RBJniu84ZxJmW6TwNL7DNE+K6TT+ep1QLNX8bDbIw6K\nJXDQg+YAhwigQ2EZezbiXJuY8+AdBGP830NT6+XbGcbT9Gn45V6BPIAYIPkuTLYn\nWwxW1PNRVpJeUGwSQJiD89jibmbjr+mzgsv0mcj05QKBgQDITZEWPFx4mWV6FQLu\nbSgpFttsztpknVl5+LZb3IBmTbO6BH0xXWlEMn6SqKJSJLfVDU5coD7/jiHFYM9Z\ngGXRHVqx1UxOZ6+X0ARrVb2Royy48sWkget9EvO/XCwaT3VRlmBhkbmEbLD56QdQ\nWvRjXcf75WK7e0idLWDR7h7FJwKBgQDDnDAWJ3WcoSGnohlsudxP9ZZDZLZ740To\nRB/MATQyuN1sj1nTT0/4aTyy6EM4evkXvS0La6TA2UFg4eZuBgU+7ni0YDuO72Kn\n/pB5GnAEtZKPKkJQbbH+opTc1lhyTE3DLOESNSX7wX0ZCR7dB56CnYkw8ziCZ3Br\n0S8tLjE1UwKBgAwhbnT7SNpg591h4mCQKct7P+SyDlXjlaSmZFzh2MDZWdYdKXvQ\n3Wws5q95GQOCh8OWX7WKWuZdNDxg5Y3VEdV9Qp3cfheNffvitDHP6oAkcrPst/2D\nhMB5YluneGBLiZ5cTg/6pFKZxooMC85ZA830wwTFWppiF/603dU455InAoGAYv3R\n4ARMIt3weDMyhrFwaw6v4p8/MmcLYjfHl6gsUFb5x4ysOqHyqJYpX6jnC9g/4uGb\nwCHTmLzZtzvbL2bglL5+W1owCd/fn4DWgFL+yYNSDh2mvakl4OVKTJA05nLzD4jQ\nxjQbatK6ikbxVY4bi6JJ4XnU6TmLzSRpqYWs5X0CgYA4/ii/T4IjLdf9028DljLu\nTR+tsmnEiMY5MuX0jFkmoR+8TrPykcBVVDphUqX6qwJM9Gxb/NZ39PyVGteFbBXJ\nNJSzKgpBpP0uXJIms46pIWVuqmB6oNDSc2g8sb4LtnHMIhH3Z4YyevYaH471/8BD\nI+pN+55JaAmPpCq7Mi82+A==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-dx5mj@kpu2021mk3-220df.iam.gserviceaccount.com",
  "client_id": "100841435919917486623",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-dx5mj%40kpu2021mk3-220df.iam.gserviceaccount.com"
}

# print(cred_data)

cred = credentials.Certificate(cred_data)
firebase_admin.initialize_app(cred, {
	'databaseURL' : 'https://kpu2021mk3-220df-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference()
ref.push({'light2' : {
	'status' : 0
}})


# https://tre2man.tistory.com/196
# https://blog.naver.com/cosmosjs/221733163025

# https://www.linkedin.com/pulse/using-firebase-realtime-db-python-chandan-singh

# kpu2021mk3-220df-firebase-adminsdk-dx5mj-76edf741d6.json
'''

# 2차 시도
from firebase import firebase
fb_app = firebase.FirebaseApplication('https://kpu2021mk3-220df-default-rtdb.asia-southeast1.firebasedatabase.app/', None)
result = fb_app.get('/saddummy@gmail',None)
print(result)

new_saddummy_data = {
    'checkKey': 'true',
    'result': '굿모닝'
}

result = fb_app.put("/saddummy@gmail", "result", new_saddummy_data)
print(result)






