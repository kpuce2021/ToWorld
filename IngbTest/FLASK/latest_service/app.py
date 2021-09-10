from flask import Flask, request  # 대문자: class
from flask import Response, make_response
from cnn_run import *
from werkzeug.utils import secure_filename
import sqlite3 as sql
import json
import os

# 초기 선언
app = Flask(__name__)  
app.config['JSON_AS_ASCII'] = False


result_text = ""
email = "asd123@naver.com"
count = "0"
dic_list = [{'result': "hello","count":"1"}]

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
        "result" : "predict:"+result_text
    }

@app.route('/con', methods=["GET", "POST"])  # 파이썬 데코레이터: 이 주소에 아래의 함수를 매칭 return은 보통 string이나 html
def convolution():
    global result_text
    global email
    global dic_list

    con = sql.connect('db/result.db', isolation_level=None)
    c = con.cursor()

    if request.method == "POST":
        # check
        file = request.files["file"]        # file
        filename = secure_filename(file.filename)
        email = request.form["user_email"]  # email
        answer = request.form["answer"]
        file.save("operation/" + filename)
        
        # if 가져온 user_email의 존재 유무 체크(table 명의 존재 유무)
        c.execute("SELECT MAX(id) FROM cnn_table WHERE email=? AND result=?;", (email, answer)) # 만약 가장 큰 값의 숫잘 리턴받을거야

        isThere = c.fetchone()[0]

        if(isThere == None):
            isThere = 0 

        wav2spec(filename)
        cnn_pre_denoise(filename,isThere,email,answer) # 여기서 specaug 까지 모두 해줌 잠시 모델 완성될 때까지 닫아두고 

        c.execute("INSERT INTO cnn_table(id, email, result) VALUES (?, ?, ?);", (isThere + 1, email, answer))

        c.execute("SELECT COUNT(DISTINCT result) FROM cnn_table;")
        count = c.fetchone()[0]

        c.execute("SELECT result FROM cnn_table where email=(?) group by result;",(email,))
        list_result = c.fetchall()

        c.execute("SELECT MAX(id) from cnn_table where email=(?) group by result;",(email,))
        list_count = c.fetchall()

        dic_list = []
        for i in range(count-1):
            dic_list.append(dict(zip(['result','count'],[str(list_result[i][0]),str(list_count[i][0])])))
    
    return json.dumps(dic_list)


@app.route('/pre_con', methods=["GET", "POST"])  # 파이썬 데코레이터: 이 주소에 아래의 함수를 매칭 return은 보통 string이나 html
def con_predict():
    global result_text
    global email
    global dic_list

    con = sql.connect('db/result.db', isolation_level=None)
    c = con.cursor()

    if request.method == "POST":
        # check
        email = request.form["user_email"]  # email

        # c.execute("select COUNT(*) from cnn_table where email=(?);", (email,))

        # isEmail = c.fetchone()[0]

        # if(isEmail == 0):
        #     c.execute("insert into cnn_table values(50,?,'오늘날씨어때'),(50,?,'내일날씨어때'),(50,?,'굿모닝')",(email,email,email))
        #     copy_tree("./shutil_template", "temp/" + email)

        c.execute("SELECT COUNT(DISTINCT result) FROM cnn_table;")
        count = c.fetchone()[0]

        c.execute("SELECT result FROM cnn_table where email=(?) group by result;",(email,))
        list_result = c.fetchall()

        c.execute("SELECT MAX(id) from cnn_table where email=(?) group by result;",(email,))
        list_count = c.fetchall()

        dic_list = []
        for i in range(count-1):
            dic_list.append(dict(zip(['result','count'],[str(list_result[i][0]),str(list_count[i][0])])))
    
    return json.dumps(dic_list)
    

@app.route('/progress', methods=["GET", "POST"])  # 파이썬 데코레이터: 이 주소에 아래의 함수를 매칭 return은 보통 string이나 html
def progress():
    global email
    global count

    con = sql.connect('db/result.db', isolation_level=None)
    c = con.cursor()

    if request.method == "POST":
       
        email = request.form["user_email"]  # email
     
        print(email)
        c.execute("select COUNT(*) from cnn_table where email=(?);", (email,))

        isEmail = c.fetchone()[0]

        if(isEmail == 0):
            c.execute("insert into cnn_table values(50,?,'오늘날씨어때'),(50,?,'내일날씨어때'),(50,?,'굿모닝')",(email,email,email))
            copy_tree("./shutil_template", "temp/" + email)

        c.execute("SELECT COUNT(*) FROM cnn_table WHERE email =(?);",(email,))
        count = c.fetchone()[0]
        count = str(count)

        print(count)

    return {
        "result": count
    }

    # startFlask에서 부르는 app
if __name__ == '__main__': 
    app.run(host='192.168.219.100',debug=True, threaded=True)