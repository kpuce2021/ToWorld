from flask import Flask, render_template, request, jsonify
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename
from functools import wraps
from cnn_run import *
import sqlite3 as sql

app = Flask(__name__) #앱을 전역으로 선언
app.config['JSON_AS_ASCII'] = False

num = 0

@app.route('/', methods=["GET","POST"]) #파이썬 데코레이터: 이 주소에 아래의 함수를 매칭 return은 보통 string이나 html
def index():
    global num
   
    con = sql.connect('db/result.db', isolation_level=None)
    c = con.cursor()

    if request.method == "POST":
        file = request.files["file"]
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
    
if __name__ == '__main__':
    app.run(host='119.207.193.93',debug=True, threaded=True)

