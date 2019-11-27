# helloTest.py
# at the end point / call method hello which returns "hello world"
#Test first Push
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  return 'Hello World!'

if __name__ == '__main__':
  app.run(host='0.0.0.0')
  #hola hola