# from flask import Flask
from flask import Flask, request, render_template
import sqlite3
app = Flask(__name__)
conn = sqlite3.connect('cloud.db')
conn.execute('CREATE TABLE if not exists equake(time VARCHAR(100),latitude DECIMAL,longitude DECIMAL,depth DECIMAL,mag DECIMAL,magType VARCHAR(100),nst SMALLINT,gap DECIMAL,dmin DECIMAL,rms DECIMAL,net VARCHAR(100),id VARCHAR(100),updated VARCHAR(100),place VARCHAR(100),type VARCHAR(100),horizontalError DECIMAL,depthError DECIMAL,magError DECIMAL,magNst SMALLINT,status VARCHAR(100),locationSource VARCHAR(100),magSource VARCHAR(100))')
@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/getrecords', methods=['POST', 'GET'])
def get_records():
    if request.method == 'POST':
        a= conn.execute('''SELECT * from equake''')
        rv = a.fetchall()
        print(rv)
        # return render_template("index.html", msg=rv)

# def hello_world():
#   return 'Hello, World!\n This looks just amazing within 5 minutes'

if __name__ == '__main__':
  app.run()
