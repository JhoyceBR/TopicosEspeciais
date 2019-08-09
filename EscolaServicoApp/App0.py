from flask import Flask
from flask import request
from flask import jsonify
from flask_json_schema import JsonSchema, JsonValidationError
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

# validação
schema = JsonSchema()
schema.init_app(app)

endereco_schema = {
    'requered': ['logradouro', 'complemento', 'bairro', 'cep', 'numero'],
    'properties': {
        'logradouro': {'type':''},
        'complemento': {'type': ''},
        'bairro': {'type': ''},
        'cep': {'type': ''},
        'numero': {'type': ''}

    }
}

escola_schema = {
    'requered': ['nome', 'fk_id_endereco', 'fk_id_campus'],
    'properties': {
        'nome': {'type': 'string'},
        'fk_id_endereco': {'type': 'integer'},
        'fk_id_campus': {'type': 'integer'}
    }

}

aluno_schema = {
    'requered': ['nome','matricula','cpf', 'nascimento', 'fk_id_endereco', 'fk_id_curso'],
    'properties': {
        'nome': {'type': 'string'},
        'matricula': {'type': 'string'},
        'cpf': {'type': 'string'},
        'nascimento': {'type': 'string'},
        'fk_id_endereco': {'type': 'integer'},
        'fk_id_curso': {'type': 'integer'}

    }

}

professor_schema = {
    'requered': ['nome', 'fk_id_endereco'],
    'properties': {
        'nome': {'type': 'string'},
        'fk_id_endereco': {'type': 'integer'}
    }
}

disciplina_schema = {
    'requered': ['nome', 'fk_id_professor'],
    'properties': {
        'nome': {'type': 'string'},
        'fk_id_professor': {'type': 'integer'}
    }

}

campus_schema = {
    'requered': ['sigla', 'cidade'],
    'properties': {
        'sigla': {'type': 'string'},
        'cidade': {'type': 'string'}
    }

}

turno_schema = {
    'requered': ['nome'],
    'properties': {
        'nome': {'type': 'string'}
    }

}

curso_schema = {
    'requered': ['nome', 'turno', 'fk_id_turno'],
    'properties': {
        'nome': {'type': 'string'},
        'turno': {'type': 'string'},
        'fk_id_turno': {'type': 'integer'}
    }

}

turma_schema = {
    'requered': ['nome', 'fk_id_curso'],
    'properties': {
        'nome': {'type': 'string'},
        'fk_id_curso': {'type': 'integer'}
    }

}

Nome_DB = "EscolaApp_versao2.db"

@app.route("/endereco", methods=['GET'])
def getEnderecos():
    logger.infor("Listando Endereços.")
    try:
        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_endereco;
        """)

        enderecos = []
        for linha in cursor.fetchall():
            endereco = {
                "id_endereco": linha[0],
                "logradouro": linha[1],
                "complemento": linha[2],
                "bairro": linha[3],
                "cep": linha[4],
                "numero": linha[5]
            }
            enderecos.append(endereco)
        logger.infor(enderecos)
        conn.close()

    except(sqlite3.Error):
        logger.error("Ocorreu um erro.")

    return jsonify(enderecos)

@app.route("/enderecos/<int:id>", methods=['GET'])
def getEndereco(id):
    logger.info("Listando endereços por id: %s"%(id))
    try:
        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_endereco
            WHERE id_endereco = ?;
        """, (id, ))

        linha = cursor.fechone()
        endereco = {
            "id_endereco": linha[0],
            "logradouro": linha[1],
            "complemento": linha[2],
            "bairro": linha[3],
            "cep": linha[4],
            "numero": linha[5]
        }

        conn.close()
    except sqlite3.Error:
        return("Ocorreu um erro.")

    return(jsonify(endereco))

@app.route("/endereco", methods=['POST'])
@schema.validate(endereco_schema)
def setEndereco():
    logger.info("Cadastrando endereco.")
    try:
        enderecoJson = request.get_json()
        logradouro = enderecoJson['logradouro'],
        complemento = enderecoJson['complemento'],
        bairro = enderecoJson['bairro'],
        cep = enderecoJson['cep'],
        numero = enderecoJson['numero']
        endereco = Endereco(logradouro,complemento, bairro, cep, numero)


        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tb_endereco(logradouro, complemento, bairro, cep, numero)
            VALUES(?, ?, ?, ?, ?);
        """, (logradouro, complemento, bairro, cep, numero))
        conn.commit()
        conn.close()

        id = cursor.lastrowid
        escola['id_endereco'] = id
    except sqlite3.Error:
        return("Ocorreu um erro.")

    return jsonify(endereco)


@app.route("/escolas", methods=['GET'])
def getEscolas():
    logger.info("Listanto escolas.")
    try:
        conn = sqlite3.connect(Nome_DB)
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
                "id_fk_endereco": linha[2],
                "id_fk_campus":linha[3]
            }
            escolas.append(escola)
        logger.info(escolas)

        conn.close()
    except sqlite3.Error:
        return("Ocorreu um erro.")

    return jsonify(escolas)


@app.route("/escolas/<int:id>", methods=['GET'])
def getEscola(id):
    logger.info("Listanto escola pelo id: %s" %(id))
    try:
        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_escola WHERE id_escola = ?;
        """, (id, ))
        linha = cursor.fechone()
        escola = {
            "id_escola":linha[0],
            "nome":linha[1],
            "id_fk_endereco":linha[2],
            "fk_id_campus":linha[3]
        }

        conn.close()
    except sqlite3.Error:
        return("Ocorreu um erro.")

    return(jsonify(escola))


@app.route("/escola", methods=['POST'])
@schema.validate(escola_schema)
def setEscola():
    logger.info("Cadastrando escola.")
    try:
        escolaJson = request.get_json()
        nome = escolaJson['nome']
        id_fk_endereco = escolaJson['id_fk_endereco']
        id_fk_campus = escolaJson['id_fk_campus']
        escola = Escola(nome, id_fk_endereco, id_fk_campus)

        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tb_escola(nome, id_fk_endereco, id_fk_campus)
            VALUES(?, ?, ?);
        """, (nome, id_fk_endereco, id_fk_campus))
        conn.commit()
        conn.close()

        id = cursor.lastrowid
        escola['id_escola'] = id
    except sqlite3.Error:
        return("Ocorreu um erro.")

    return jsonify(escola)


@app.route("/alunos", methods=['GET'])
def getAlunos():
    logger.info("Listanto alunos.")
    try:
        conn = sqlite3.connect(Nome_DB)
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
                "nascimento":linha[4],
                "fk_id_endereco": linha[5],
                "fk_id_curso": linha[6]
            }
            alunos.append(aluno)
        logger.info(alunos)
        conn.close()
    except sqlite3.Error:
        return("Ocorreu um erro.")
    return jsonify(alunos)


@app.route("/alunos/<int:id>", methods=['GET'])
# colocar o try!
def getAluno(id):
    try:
        logger.info("Listanto aluno pelo id: %s."%(id))
        conn = sqlite3.connect(Nome_DB)
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
            "nascimento":linha[4],
            "fk_id_endereco": linha[5],
            "fk_id_curso": linha[6]
        }

        conn.close()
    except sqlite3.Error:
        return("Ocorreu um erro.")
    return jsonify(aluno)

@app.route("/aluno", methods=['POST'])
@schema.validate(aluno_schema)
def setAlunos():
    logger.info("Cadastrando aluno.")
    alunoJson = request.get_json()
    nome = alunoJson['nome']
    matricula = alunoJson['matricula']
    cpf = alunoJson['cpf']
    nascimento = alunoJson['nascimento']
    aluno = Aluno(nome, matricula, cpf, nascimento, fk_id_endereco, fk_id_curso)

    conn = sqlite3.connect(Nome_DB)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_aluno(nome, matricula, cpf, nascimento, fk_id_endereco, fk_id_curso)
        VALUES(?, ?, ?, ?, ?, ?);
    """, (nome, matricula, cpf, nascimento, fk_id_endereco, fk_id_curso))
    conn.commit()
    conn.close()

    id = cursor.lastrowid
    aluno['id_aluno'] = id

    return (jsonify(aluno))

@app.route("/cursos", methods=['GET'])
def getCursos():
    logger.info("Listanto cursos.")
    conn = sqlite3.connect(Nome_DB)
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
    logger.info("Listanto curso pelo id.")
    conn = sqlite3.connect(Nome_DB)
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
    logger.info("Cadastrando curso.")
    try:
        curso = request.get_json()
        nome = curso['nome']
        turno = curso['turno']

        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tb_curso(nome, turno)
            VALUES(?, ?);
        """, (nome, turno))

        conn.commit()
        conn.close()

        id = cursor.lastrowid
        curso["id_curso"] = id
    except sqlite3.Error:
        return("Ocorreu um erro.")

    return(jsonify(curso))

@app.route("/turmas", methods=['GET'])
def getTurmas():
    logger.info("Listanto turmas.")
    conn = sqlite3.connect(Nome_DB)

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
    logger.info("Listanto turma pelo id.")
    conn = sqlite3.connect(Nome_DB)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tb_turma WHERE id_turma = ?;
    """, (id, ))

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
    logger.info("Cadastrando turma.")
    turma = request.get_json()
    nome = turma['nome']
    curso = turma['curso']

    conn = sqlite3.connect(Nome_DB)
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
    logger.info("Listanto disciplinas.")
    conn = sqlite3.connect(Nome_DB)

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
    logger.info("Listanto disciplinas pelo id.")
    try:
        conn = sqlite3.connect(Nome_DB)

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_disciplina WHERE id_disciplina = ?;
        """, (id, ))

        linha = cursor.fechone()
        disciplina = {
            "id_disciplina":linha[0],
            "nome":linha[1]
        }

        conn.close()
    except sqlite3.Error:
        return("Ocorreu um erro.")

    return jsonify(disciplina)

####ver aqui
@app.route("/disciplina", methods=['POST'])
def setDisciplinas():
    logger.info("Cadastrando disciplina.")
    try:
        disciplina = request.get_json()
        nome = disciplina['nome']

        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tb_disciplina(nome)
            VALUES(?);
        """, (nome))
        conn.commit()
        conn.close()

        id = cursor.lastrowid
        disciplina["id_disciplina"] = id
    except sqlite3.Error:
        return("Ocorreu um erro.")
    return (jsonify(disciplina))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
