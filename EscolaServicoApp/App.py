from flask import Flask
from flask import request
from flask import jsonify
import logging # nativo
import sqlite3 # nativo

# inicia a aplicação
app = Flask(__name__)

# loggin
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("escolaapp.log")
handler.setFormatter(formatter)

logger = app.logger
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@app.route("/escolas", methods=['GET'])
def getEscolas():
    logger.info("Listanto escolas.")
    conn = sqlite3.connect('ifpb.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tb_escola;
    """)

    escolas = []
    for linha in cursor.fetchall():
        escola = {
            "id_escola":linha[0],
            "nome":linha[1],
            "logradouro":linha[2],
            "cidade":linha[3]
        }
        escolas.append(escola)

    conn.close()

    return jsonify(escolas)


@app.route("/escolas/<int:id>", methods=['GET'])
def getEscola(id):
    conn = sqlite3.connect('ifpb.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tb_escola WHERE id_escola = ?;
    """, (id, ))
    linha = cursor.fechone()
    escola = {
        "id_escola":linha[0],
        "nome":linha[1],
        "logradouro":linha[2],
        "cidade":linha[3]
    }

    conn.close()

    return(jsonify(escola))

@app.route("/escola", methods=['POST'])
def setEscola():
    escola = request.get_json()
    nome = escola['nome'] # valor indicado no dicionário
    logradouro = escola['logradouro']
    cidade = escola['cidade']

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_escola(nome, logradouro, cidade)
        VALUES(?, ?, ?);
    """, (nome, logradouro, cidade))
    conn.commit()
    conn.close()

    id = cursor.lastrowid
    escola['id_escola'] = id

    return jsonify(escola)


@app.route("/alunos", methods=['GET'])
def getAlunos():
    conn = sqlite3.connect('ifpb.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tb_aluno;
    """)

    #alterações
    alunos = []
    for linha in cursor.fetchall():
        aluno = {
            "id_aluno":linha[0],
            "nome":linha[1],
            "matricula":linha[2],
            "cpf":linha[3],
            "nascimento":linha[4]
        }
        alunos.append(aluno)

    conn.close()

    return jsonify(alunos)


@app.route("/alunos/<int:id>", methods=['GET'])
def getAluno(id):
    conn = sqlite3.connect('ifpb.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tb_aluno WHERE id_aluno = ?;
    """, (id, ))

    linha = cursor.fetchone()
    aluno = {
        "id_aluno":linha[0],
        "nome":linha[1],
        "matricula":linha[2],
        "cpf":linha[3],
        "nascimento":linha[4]
    }

    conn.close()

    return jsonify(aluno)

@app.route("/aluno", methods=['POST'])
def setAlunos():
    aluno = request.get_json() # recupera json completo - dicionario
    nome = aluno['nome']
    matricula = aluno['matricula']
    cpf = aluno['cpf']
    nascimento = aluno['nascimento']

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_aluno(nome, matricula, cpf, nascimento)
        VALUES(?, ?, ?, ?);
    """, (nome, matricula, cpf, nascimento))
    conn.commit()
    conn.close()

    id = cursor.lastrowid
    aluno['id_aluno'] = id

    return (jsonify(aluno))

@app.route("/cursos", methods=['GET'])
def getCursos():
    conn = sqlite3.connect('ifpb.db')

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tb_curso;
    """)
    cursos = []
    for linha in cursor.fetchall():
        curso = {
            "id_curso":linha[0],
            "nome":linha[1],
            "turno":linha[2]
        }
        cursos.append(curso)

    conn.close()

    return jsonify(cursos)


@app.route("/cursos/<int:id>", methods=['GET'])
def getCurso(id):
    conn = sqlite3.connect('ifpb.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tb_curso WHERE id_curso = ?;
    """, (id, ))

    linha = cursor.fetchone()
    curso = {
        "id_curso":linha[0],
        "nome":linha[1],
        "turno":linha[2]
    }
    conn.close()

    return jsonify(curso)

@app.route("/curso", methods=['POST'])
def setCurso():

    curso = request.get_json()
    nome = curso['nome']
    turno = curso['turno']

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_curso(nome, turno)
        VALUES(?, ?);
    """, (nome, turno))

    conn.commit()
    conn.close()

    id = cursor.lastrowid
    curso["id_curso"] = id

    return(jsonify(curso))

@app.route("/turmas", methods=['GET'])
def getTurmas():
    conn = sqlite3.connect('ifpb.db')

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tb_turma;
    """)
    turmas = []
    for linha in cursor.fetchall():
        turma = {
            "id_turma":linha[0],
            "nome":linha[1],
            "curso":linha[2]
        }
        turmas.append(turma)
    conn.close()

    return jsonify(turmas)



@app.route("/turmas/<int:id>", methods=['GET'])
def getTurma(id):
    conn = sqlite3.connect('ifpb.db')

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tb_turma WHERE id = ?;
    """, (id_turma, ))

    linha = cursor.fetchone()
    turma = {
        "id_turma":linha[0],
        "nome":linha[1],
        "curso":linha[2]
    }

    conn.close()

    return jsonify(turma)

@app.route("/turma", methods=['POST'])
def setTurmas():

    turma = request.get_json()
    nome = turma['nome']
    turno = turma['curso']

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_turma(nome, curso)
        VALUES(?, ?);
    """, (nome, curso))
    conn.commit()
    conn.close()

    id = cursor.lastrowid
    turma["id_turma"] = id

    return (jsonify(turma))


@app.route("/disciplinas", methods=["GET"])
def getDisciplinas():
    conn = sqlite3.connect('ifpb.db')

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tb_disciplina;
    """)
    disciplinas = []
    for linha in cursor.fetchall():
        disciplina = {
            "id_disciplina":linha[0],
            "nome":linha[1]
        }
        disciplinas.append(disciplina)
    conn.close()

    return jsonify(disciplinas)



@app.route("/disciplinas/<int:id>", methods=['GET'])
def getDisciplina(id):
    conn = sqlite3.connect('ifpb.db')

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tb_disciplina WHERE id = ?;
    """, (id_disciplina, ))

    linha = cursor.fechone()
    disciplina = {
        "id_disciplina":linha[0],
        "nome":linha[1]
    }

    conn.close()

    return jsonify(disciplina)

@app.route("/disciplina", methods=['POST'])
def setDisciplinas():
    disciplina = request.get_json()
    nome = disciplina['nome']

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_disciplina(nome)
        VALUES(?);
    """, (nome))
    conn.commit()
    conn.close()

    id = cursor.lastrowid
    disciplina["id_disciplina"] = id
    return (jsonify(disciplina))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
