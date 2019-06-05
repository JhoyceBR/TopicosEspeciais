from flask import Flask
from flask import request
import sqlite3

#acesso em localhost:5000

app = Flask(__name__)

@app.route("/")
def hello_flask():
    return("tudo começa agora")

@app.route("/escolas", methods=['GET'])
def getEscolas():
    return("")
    pass

@app.route("/escolas/<int:id>", methods=['GET'])
def getEscola(id): 
    pass 

@app.route("/escola", methods=['POST'])
def setEscola():
    pass

app.run()
