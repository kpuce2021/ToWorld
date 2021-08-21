from flask import Flask, request
from werkzeug.utils import secure_filename
from flaskTest.flaskBaseFolder.cnn_run import *
import sqlite3 as sql

app = Flask(__name__) #앱을 전역으로 선언
app.config['JSON_AS_ASCII'] = False

num = 0

@app.route('/predict', methods=["GET","POST"]) #파이썬 데코레이터: 이 주소에 아래의 함수를 매칭 return은 보통 string이나 html
def predict():
    global num
   
    con = sql.connect('db/result.db', isolation_level=None)
    c = con.cursor()

    if request.method == "POST":
        file = request.files["file"]
        print(file)
        email = request.form["user_email"]
        filename = secure_filename(file.filename)
        file.save("operation/"+ filename)
        wav2spec(filename)
        pre_denoise(filename)
        result_text = check_model(filename)
        print(result_text)

        c.execute("SELECT COUNT(*) FROM result_table;")
        ingb = c.fetchone()
        num = ingb[0]

        c.execute("INSERT INTO result_table(id,email,result) values(?,?,?);",(ingb[0], email, result_text))
        
    c.execute("SELECT result FROM result_table where id=?;",(num,))
   
    return { 
        "result" : str(c.fetchone()[0])
    }

@app.route('/convolution', methods=["GET","POST"]) #파이썬 데코레이터: 이 주소에 아래의 함수를 매칭 return은 보통 string이나 html
def convolution():
    global num2
    
    con = sql.connect('db/result.db', isolation_level=None)
    c = con.cursor()

    if request.method == "POST":
        file = request.files["file"]
        email = request.form["user_email"]

        # if 가져온 user_email의 존재 유무 체크(table 명의 존재 유무)
        # 1. 존재 -> 기존 테이블에 입력된 문장의 갯수를 1 올리고 파일 저장
        #         -> 만약 학습할 문장이 50개가 쌓였다 하면 convolution 1회 실행 

        # 2. 없음 -> 테이블 생성 후 사용자명의 디렉토리를 생성 후 그 곳에 + primary 이름 개수 + 음성 파일 저장 + 템플릿 모델 생성
        
        filename = secure_filename(file.filename)
        file.save("operation/"+ filename)
        wav2spec(filename)
        pre_denoise(filename)
        
        # 전처리가 완료된 시점

        c.execute("SELECT COUNT(*) FROM result_table;")
        ingb = c.fetchone()
        num = ingb[0]

        c.execute("INSERT INTO result_table(id,email,result) values(?,?,?);",(ingb[0], email, result_text))
        
    c.execute("SELECT result FROM result_table where id=?;",(num,))
   
    return { 
        "result" : str(c.fetchone()[0])
    }
    
if __name__ == '__main__':
    app.run(host='210.99.255.178',debug=True, threaded=True)