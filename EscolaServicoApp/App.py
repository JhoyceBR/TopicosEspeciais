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

@app.route("/alunos", methods=['GET'])
def getAlunos():
    pass

@app.route("/alunos/<int:id>", methods=['GET'])
def getAlunos(id):
    pass

@app.route("/aluno", methods=['POST'])
def setAlunos():
    pass

@app.route("/curso", methods=['GET'])
def getCurso():
    pass

@app.route("/curso/<int:id>", methods=['GET'])
def getCurso(id):
    pass

@app.route("/curso", methods=['POST'])
def setCurso():
    pass

@app.route("/turmas", methods=['GET'])
def getTurmas():
    pass

@app.route("/turmas/<int:id>", methods=['GET'])
def getTurmas(id):
    pass

@app.route("/turmas", methods=['POST'])
def setTurmas():
    pass

@app.route("/disciplinas", methods="GET")
def getDisciplinas():
    pass

@app.route("/disciplinas/<int:id>", methods=['GET'])
def getDisciplinas(id):
    pass

@app.route("/disciplinas", methods=['POST'])
def setDisciplinas():
    pass

app.run()
