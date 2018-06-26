# from flask import Flask
from flask import Flask, request, render_template
import sqlite3
import io
import csv
import redis

app = Flask(__name__)
tem = sqlite3.connect('cloud.db')
tem.execute('CREATE TABLE if not exists equake(time VARCHAR(100),latitude DECIMAL,longitude DECIMAL,depth DECIMAL,mag DECIMAL,magType VARCHAR(100),nst SMALLINT,gap DECIMAL,dmin DECIMAL,rms DECIMAL,id VARCHAR(100),place VARCHAR(100),depthError DECIMAL,magError DECIMAL,magNst SMALLINT,locationSource VARCHAR(100))')
tem.execute('create table if not exists titanic(pclass decimal, survived decimal, name varchar(50), sex varchar(10), age decimal, sibsp decimal, parch decimal, ticket varchar(10), fare decimal, cabin varchar(20), embarked varchar(10), boat decimal, body decimal, homedest varchar(50))')
tem.execute('CREATE TABLE if not exists quake(time VARCHAR(100),latitude DECIMAL,longitude DECIMAL,depth DECIMAL,mag DECIMAL,magType VARCHAR(100),nst SMALLINT,gap DECIMAL,dmin DECIMAL,rms DECIMAL,net Varchar(100),id VARCHAR(100),updated Varchar(100), place VARCHAR(100),type Varchar(100),horizontalError DECIMAL,depthError DECIMAL,magError DECIMAL,magNst SMALLINT,status Varchar(100),locationSource VARCHAR(100),magSource Varchar(100))')

myHostname = "msr01.redis.cache.windows.net"
myPassword = "plvUVeT6WAsHvOOuI6w7GQYVk4dk2qjfbJzel233VRE="
r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True,decode_responses=True)
result = r.ping()
print("Ping returned : " + str(result))

@app.route('/')
def my_form():
    result = r.set("Message", "Hello!, The cache is working with Python!")
    print("SET Message returned : " + str(result))

    result = r.get("Message")
    print("GET Message returned : " + result)
    return render_template('home.html')

@app.route('/upload', methods=['POST', 'GET'])
def insert_table():
    if request.method == 'POST':
        tem = sqlite3.connect('cloud.db')
        cur = tem.cursor()
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
                cur.execute("INSERT INTO quake(time, latitude, longitude, depth, mag, magType, nst, gap, dmin, rms, net, id, updated, place, type, horizonatalError, depthError, magError, magNst, status, locationSource, magSource) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",row)
                print(1)
                tem.commit()
                msg = "Record successfully added"
                print(msg)
            except Exception as e:
                print(e)
                tem.rollback()
        return render_template('home.html')

@app.route('/getrecords', methods=['POST', 'GET'])
def get_records():
    if request.method == 'POST':
        tem = sqlite3.connect("cloud.db")
        cur = tem.cursor()
        text2 = request.form['b']
        text3 = request.form['c']
        # cur.execute('''SELECT * from quake where (mag between ? and ?)''',(text2,text3,))
        # y = cur.fetchall()
        # print(y)
        # r.set('Query3',y)
        tempo=r.get('Query3')
        print(tempo)
        y=tempo
        print(y)
        return render_template("index.html", trial=y)

# @app.route('/showrecords', methods=['POST', 'GET'])
# def get_records():
#     if request.method == 'POST':
#         tem = sqlite3.connect("cloud.db")
#         cur = tem.cursor()
#         text4 = request.form['d']
#         text5 = request.form['e']
#         cur.execute('''SELECT * from titanic where (age between ? and ?)''',(text4,text5,))
        # cur.execute('''select * from titanic where sex='male' group by pclass''')
        # x = cur.fetchall()
        # print(x)
        # r.set('Query1',x)
        #
        # # tempo=r.get('Query1')
        # # x=tempo
        # print(x)
        # return render_template("demo.html", temp=x)

def hello_world():
  return 'Hello, World!\n This looks just amazing within 5 minutes'

if __name__ == '__main__':
    app.debug=='true'
    app.run()
