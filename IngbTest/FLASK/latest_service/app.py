from flask import Flask, request  # 대문자: class
from flask import make_response
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

@app.route('/predict', methods=["GET","POST"])
def predict():
    global result_text

    if request.method == "POST":
        file = request.files["file"]
        print(file)
        email = request.form["user_email"]
        filename = secure_filename(file.filename)
        file.save("operation/"+ email + "/" + filename)

        wav2spec(filename, email)
        pre_denoise(filename, email)
        result_text = check_model(filename, email)

    return {
        "result" : result_text
    }

@app.route('/con', methods=["GET", "POST"])
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
        file.save("operation/"+ email +"/" + filename)
        
        # result Count
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


@app.route('/pre_con', methods=["GET", "POST"])
def con_predict():
    global result_text
    global email
    global dic_list

    con = sql.connect('db/result.db', isolation_level=None)
    c = con.cursor()

    if request.method == "POST":
      
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
    
@app.route('/progress', methods=["GET", "POST"])
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

        # 처음 사용자 템플릿 구성
        if(isEmail == 0):
            c.execute("insert into cnn_table values(50,?,'오늘날씨어때'),(50,?,'내일날씨어때'),(50,?,'굿모닝'),(50,?,'출근길교통상황어때'),(50,?,'음악추천해줘'),(50,?,'상호한테전화해줘'),(50,?,'유튜브에서동빈나틀어줘')",(email,email,email,email,email,email,email))
            copy_tree("./shutil_template", "temp/" + email)
            oper_path = "operation/" + email
            os.makedirs(oper_path)

        c.execute("SELECT COUNT(*) FROM cnn_table WHERE email =(?);",(email,))
        count = c.fetchone()[0]
        count = str(count)

        print(count)

    return {
        "result": count
    }

if __name__ == '__main__': 
    app.run(host='192.168.219.100',debug=True, threaded=True)