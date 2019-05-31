from flask import Flask
from flask import request
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_world():
    return ("Olá Mundo! Estou aprendendo Flask", 200)

@app.route("/alunos", methods=['GET'])
def getAlunos():
    conn = sqlite3.connect('escola.db')

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM TB_ALUNO;
    """)

    for linha in cursor.fetchall():
        print(linha)

    conn.close()

    return("Executado!", 200)


@app.route("/alunos/<int:id>", methods=['GET'])
def getAlunoByID(id):
    pass

@app.route("/alunos/cadastro", methods=['POST'])
def setAluno():
    print ("Cadastrando discente!")
    nome = request.form['nome']
    matricula = request.form['matricula']
    cpf = request.form['cpf']
    nascimento = request.form['nascimento']

    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TB_ALUNO(NOME, MATRICULA, CPF, NASCIMENTO)
        VALUES(?, ?, ?, ?)

    """, (nome, matricula, cpf, nascimento))
    conn.commit()
    conn.close()

    return ("Cadastro realizado com sucesso!", 200)


    '''
    conn = sqlite3.connect('escola.db')

    cursor = conn.cursor()

    cursor.execute("""

    """)
    '''



@app.route("/cursos", methods=['GET'])
def getCursos():
    conn = sqlite3.connect('escola.db')

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM TB_CURSO;
    """)

    for linha in cursor.fetchall():
        print(linha)

    conn.close()

    return("Executado!", 200)


@app.route("/cursos/<int:id>", methods=['GET'])
def getCursoByID(id):
    pass


@app.route("/turmas", methods=['GET'])
def getTurmas():
    conn = sqlite3.connect('escola.db')

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM TB_TURMA;
    """)

    for linha in cursor.fetchall():
        print(linha)

    conn.close()

    return("Executado!", 200)


@app.route("/turmas/<int:id>", methods=['GET'])
def getTurmaByID(id):
    pass

if(__name__ == '__main__'):
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
