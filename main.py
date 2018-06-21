# from flask import Flask
from flask import Flask, request, render_template
import sqlite3
import io
import csv
app = Flask(__name__)
tem = sqlite3.connect('cloud.db')
tem.execute('CREATE TABLE if not exists equake(time VARCHAR(100),latitude DECIMAL,longitude DECIMAL,depth DECIMAL,mag DECIMAL,magType VARCHAR(100),nst SMALLINT,gap DECIMAL,dmin DECIMAL,rms DECIMAL,id VARCHAR(100),place VARCHAR(100),depthError DECIMAL,magError DECIMAL,magNst SMALLINT,locationSource VARCHAR(100))')
tem.execute('create table if not exists titanic(pclass decimal, survived decimal, name varchar(50), sex varchar(10), age decimal, sibsp decimal, parch decimal, ticket varchar(10), fare decimal, cabin varchar(20), embarked varchar(10), boat decimal, body decimal, homedest varchar(50))')
@app.route('/')
def my_form():
     return render_template('home.html')

@app.route('/upload', methods=['POST', 'GET'])
def insert_table():
    if request.method == 'POST':
        tem = sqlite3.connect('cloud.db')
        cur = con.cursor()
        f = request.files['data_file']
        if not f:
            return "No file"
        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        next(csv_input)
        for row in csv_input:
            print(row)
            try:
                print("Inside try")
                cur.execute("INSERT INTO titanic(pclass, survived, name,sex,age,sibsp,parch,ticket,fare,cabin,embarked,boat,body,homedest) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",row)
                print(1)
                tem.commit()
                msg = "Record successfully added"
                print(msg)
            except Exception as e:
                print(e)
                tem.rollback()
        return render_template('home.html')

# @app.route('/getrecords', methods=['POST', 'GET'])
# def get_records():
#     if request.method == 'POST':
#         tem = sqlite3.connect("cloud.db")
#         cur = con.cursor()
#         text2 = request.form['b']
#         text3 = request.form['c']
#         cur.execute('''SELECT COUNT(mag) from equake where (mag between ? and ?)''',(text2,text3,))
#         rv = cur.fetchall()
#         print(rv)
#         return render_template("index.html", msg=rv)

@app.route('/showrecords', methods=['POST', 'GET'])
def get_records():
    if request.method == 'POST':
        tem = sqlite3.connect("cloud.db")
        cur = con.cursor()
        text4 = request.form['d']
        text5 = request.form['e']
        cur.execute('''SELECT * from titanic where (age between ? and ?)''',(text4,text5,))
        x = cur.fetchall()
        print(x)
        return render_template("demo.html", temp=x)

# def hello_world():
#   return 'Hello, World!\n This looks just amazing within 5 minutes'

if __name__ == '__main__':
    app.debug=='true'
    app.run()
