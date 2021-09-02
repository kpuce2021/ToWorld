from flask import Flask, request  # 대문자: class
from flask import Response, make_response

from flaskTest.flaskBaseFolder import webapp

# 초기 선언
app = Flask(__name__)  
app.config['JSON_AS_ASCII'] = False

# =================================================================================

@app.route("/")
def helloworld():
    return "Hello Flask World!"

@app.route("/snowflo")
def snowflo():
    # custom_res = Response("snowfloResponse", 200, {'saebom': 'joa'})
    return make_response(webapp.snowfloRes())

@app.route("/saddummy")
def saddummy():
    return "saddummy"

# =================================================================================
from flaskTest.flaskBaseFolder.client import *
from flaskTest.flaskBaseFolder.cnn_run import *

from flask import Flask, request  # 대문자: class
from werkzeug.utils import secure_filename
import sqlite3 as sql

result_text = ""

@app.route('/predict', methods=["GET","POST"]) #파이썬 데코레이터: 이 주소에 아래의 함수를 매칭 return은 보통 string이나 html
def predict():
    global result_text

    if request.method == "POST":
        file = request.files["file"]
        print(file)
        email = request.form["user_email"]
        filename = secure_filename(file.filename)
        file.save("operation/" + filename)

        # cnn_run
        wav2spec(filename)
        pre_denoise(filename)
        result_text = check_model(filename)
        print(result_text)

    return {
        "result" : "predict"+result_text
    }


import os

@app.route('/convolution', methods=["GET", "POST"])  # 파이썬 데코레이터: 이 주소에 아래의 함수를 매칭 return은 보통 string이나 html
def convolution():
    global result_text

    con = sql.connect('db/result.db', isolation_level=None)
    c = con.cursor()

    if request.method == "POST":
        path = ""                           # file save path (every)

        # check
        file = request.files["file"]        # file
        print(file)

        email = request.form["user_email"]  # email
        answer = request.form["answer"]     # answer
        print(email +" "+ answer)

        # if 가져온 user_email의 존재 유무 체크(table 명의 존재 유무)
        c.execute("SELECT COUNT(*) FROM result_table WHERE email=? AND result=?;", (email, answer))
        # 0 NoN NoN

        isThere = c.fetchone()[0]

        if(isThere > 0):                # 이미 존재
            path = "D:/#2021_CAPSTONE/_DataSet/model/user/" + email + "/" + answer

            if(isThere % 5 == 0):       # % [데이터 개수] --> 조절하면 됨. 50개 하려면 49로
                print("학습 시작 {}".format(isThere))       # 이전 데이터 사용하지 않을 방법을 찾아야 함.
                result_text = "학습중 입니다."
        else:                           # 기존에 존재하지 않음 == 0
            path = "D:/#2021_CAPSTONE/_DataSet/model/user/" + email + "/" + answer
            os.makedirs(path)       # 폴더 여러개 생성

        c.execute("INSERT INTO result_table(id, email, result) VALUES (?, ?, ?);", (isThere + 1, email, answer))

        filename = answer + str(isThere+1) + ".wav"
        print(filename)

        file.save(path + "/" + filename)

    return {
        "result" : "convolution: " + result_text
    }

# startFlask에서 부르는 app
if __name__ == '__main__': 
    app.run(host='0.0.0.0',debug=True, threaded=True)

