# from flask import Flask
from flask import Flask, request, render_template
import sqlite3
import io
import csv
app = Flask(__name__)
con = sqlite3.connect('cloud.db')
con.execute('CREATE TABLE if not exists equake(time VARCHAR(100),latitude DECIMAL,longitude DECIMAL,depth DECIMAL,mag DECIMAL,magType VARCHAR(100),nst SMALLINT,gap DECIMAL,dmin DECIMAL,rms DECIMAL,net VARCHAR(100),id VARCHAR(100),updated VARCHAR(100),place VARCHAR(100),type VARCHAR(100),horizontalError DECIMAL,depthError DECIMAL,magError DECIMAL,magNst SMALLINT,status VARCHAR(100),locationSource VARCHAR(100),magSource VARCHAR(100))')
@app.route('/')
def my_form():
     return render_template('home.html')

@app.route('/upload', methods=['POST', 'GET'])
def insert_table():
    if request.method == 'POST':
        con = sqlite3.connect('cloud.db')
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
                cur.execute(
                    "INSERT INTO equake(time, latitude, longitude, depth, mag, magType, nst, gap, dmin, rms,net, id,updated, place,type,horizontalError, depthError, magError, magNst,status, locationSource,magSource) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",row)
                print(1)
                con.commit()
                msg = "Record successfully added"
                print(msg)
            except Exception as e:
                print(e)
                con.rollback()
        return render_template('home.html')

@app.route('/getrecords', methods=['POST', 'GET'])
def get_records():
    if request.method == 'POST':
        con = sqlite3.connect("cloud.db")
        cur = con.cursor()
        cur.execute('''SELECT * from equake ''')
        rv = cur.fetchall()
        print(rv)
        return render_template("index.html", msg=rv)

# def hello_world():
#   return 'Hello, World!\n This looks just amazing within 5 minutes'

if __name__ == '__main__':
    app.debug=='true'
    app.run()
