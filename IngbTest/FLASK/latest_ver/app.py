from flask import Flask, request  # 대문자: class
from flask import make_response
from cnn_run import *
from werkzeug.utils import secure_filename
import sqlite3 as sql
import json
import os

app = Flask(__name__)  
app.config['JSON_AS_ASCII'] = False

result_text = ""
email = "asd123@naver.com"
count = "0"
dic_list = [{'result': "hello","count":"1"}]

@app.route('/predict', methods=["GET","POST"])
def predict():
    global result_text
    con = sql.connect('db/result.db', isolation_level=None)
    c = con.cursor()

    if request.method == "POST":
        file = request.files["file"]
        print(file)
        email = request.form["user_email"]
        filename = secure_filename(file.filename)
        file.save("operation/"+ email + "/" + filename)

        wav2spec(filename, email)
        pre_denoise(filename, email)
        result_id = check_model(filename, email).item()
        print(result_id)

        c.execute("SELECT result FROM cnn_table WHERE email=? AND num=?;", (email, result_id+1)) # 만약 가장 큰 값의 숫잘 리턴받을거야
        result_text = c.fetchone()[0]

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
        c.execute("SELECT MAX(id) FROM cnn_table WHERE email=? AND result=?;", (email, answer)) # INPUT: 이메일, 결과 -> id의 가장 큰 값 파일생성을 위해 사용
        id_count = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM cnn_table WHERE email=? AND result=?;", (email, answer)) # isThere 파일의 존재 유무 체크 ID_Count로 하면 처음 템플릿 ID를 0으로 내놨기 때문에 템플릿 학습하면 하나 추가 학습됨
        isThere = c.fetchone()[0]

        c.execute("SELECT MAX(num) FROM cnn_table WHERE email=?;", (email,)) # 데이터베이스 num중 가장 큰거 파일 정렬에 사용
        file_num = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM cnn_table WHERE email=?;", (email,)) # 전체 파일 수 CNN_ 돌릴 때 사용
        cnn_count = c.fetchone()[0]

        print("isThere:",isThere)

        if((isThere == None) or (isThere == 0)):
            isThere = 0 
            c.execute("INSERT INTO cnn_table(id, email, result, num) VALUES (?, ?, ?, ?);", (isThere + 1, email, answer, file_num + 1))
            wav2spec(filename, email)
            cnn_pre_denoise(filename, id_count, isThere, email, answer, file_num+ 1, cnn_count)
        else:
            c.execute("SELECT num FROM cnn_table WHERE email=? and result=?;", (email, answer)) # 만약 가장 큰 값의 숫잘 리턴받을거야
            number = c.fetchone()[0]

            c.execute("INSERT INTO cnn_table(id, email, result) VALUES (?, ?, ?);", (id_count + 1, email, answer))
            wav2spec(filename,email)
            cnn_pre_denoise(filename, id_count, isThere, email, answer, number, cnn_count)
        
        c.execute("SELECT COUNT(DISTINCT result) FROM cnn_table;")
        count = c.fetchone()[0]

        c.execute("SELECT result FROM cnn_table where email=(?) group by result;",(email,))
        list_result = c.fetchall()

        c.execute("SELECT MAX(id) from cnn_table where email=(?) group by result;",(email,))
        list_count = c.fetchall()

        dic_list = []
        for i in range(count):
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

        c.execute("SELECT COUNT(DISTINCT result) FROM cnn_table;")
        count = c.fetchone()[0]

        c.execute("SELECT result FROM cnn_table where email=(?) group by result;",(email,))
        list_result = c.fetchall()

        c.execute("SELECT MAX(id) from cnn_table where email=(?) group by result;",(email,))
        list_count = c.fetchall()

        dic_list = []
        for i in range(count):
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
            c.execute("insert into cnn_table values(0,?,'상호한테전화해줘',1),(0,?,'굿모닝',2),(0,?,'출근길교통상황어때',3),(0,?,'음악추천해줘',4),(0,?,'오늘날씨어때',5),(0,?,'내일날씨어때',6),(0,?,'유튜브에서동빈나틀어줘',7)",(email,email,email,email,email,email,email))
            copy_tree("./shutil_template", "temp/" + email) # 수정하였음
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
    app.run(host='192.168.219.101',debug=True, threaded=True)