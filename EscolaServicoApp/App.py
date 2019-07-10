from flask import Flask
from flask import request
from flask import jsonify
import sqlite3

#acesso em localhost:5000

app = Flask(__name__)

@app.route("/escolas", methods=['GET'])
def getEscolas():
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
    print ("Cadastrando escola!")
    nome = request.form['nome']
    logradouro = request.form['logradouro']
    cidade = request.form['cidade']

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_escola(nome, logradouro, cidade)
        VALUES(?, ?, ?);

    """, (nome, logradouro, cidade))
    conn.commit()
    conn.close()

    return ("Cadastro realizado com sucesso!", 200)

# o get só recebe, não envia json. Apenas o post(inserir e atualizar dados) e o put(inserir) podem
# receber json.

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
def getAlunos(id):
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
    print ("Cadastrando discente!")
    nome = request.form['nome']
    matricula = request.form['matricula']
    cpf = request.form['cpf']
    nascimento = request.form['nascimento']

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_aluno(nome, matricula, cpf, nascimento)
        VALUES(?, ?, ?, ?);

    """, (nome, matricula, cpf, nascimento))
    conn.commit()
    conn.close()

    return ("Cadastro realizado com sucesso!", 200)

@app.route("/cursos", methods=['GET'])
def getCurso():
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
        FROM tb_curso WHERE id = ?;
    """, (id_curso, ))

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
    print ("Cadastrando curso!")
    nome = request.form['nome']
    turno = request.form['turno']

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_curso(nome, turno)
        VALUES(?, ?);
    """, (nome, turno))

    conn.commit()
    conn.close()

    return ("Cadastro realizado com sucesso!", 200)

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
def getTurmas(id):
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
    print ("Cadastrando turma!")
    nome = request.form['nome']
    turno = request.form['curso']

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_turma(nome, curso)
        VALUES(?, ?);

    """, (nome, curso))
    conn.commit()
    conn.close()

    return ("Cadastro realizado com sucesso!", 200)


@app.route("/disciplinas", methods=["GET"])
def getDisciplinas():
    conn = sqlite3.connect('ifpb.db')

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tb_disciplina;
    """)

    for linha in cursor.fetchall():
        print(linha)

    conn.close()

    return("Executado!", 200)



@app.route("/disciplinas/<int:id>", methods=['GET'])
def getDisciplinas(id):
    conn = sqlite3.connect('ifpb.db')

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tb_disciplina WHERE id = ?;
    """, (id_disciplina, ))

    for linha in cursor.fetchall():
        print(linha)

    conn.close()

    return("Executado!", 200)

@app.route("/disciplina", methods=['POST'])
def setDisciplinas():
    print ("Cadastrando disciplina!")
    nome = request.form['nome']

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_disciplina(nome)
        VALUES(?);

    """, (nome))
    conn.commit()
    conn.close()

    return ("Cadastro realizado com sucesso!", 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
