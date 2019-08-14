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

endereco_schema = {
    'requered': ['logradouro', 'complemento', 'bairro', 'cep', 'numero'],
    'properties': {
        'logradouro': {'type':'string'},
        'complemento': {'type': 'string'},
        'bairro': {'type': 'string'},
        'cep': {'type': 'string'},
        'numero': {'type': 'integer'}

    }
}

curso_schema = {
    'requered': ['nome', 'fk_id_turno'],
    'properties': {
        'nome': {'type': 'string'},
        'turno': {'type': 'string'},
        'fk_id_turno': {'type': 'integer'}
    }

}

turno_schema = {
    'requered': ['nome'],
    'properties': {
        'nome': {'type': 'string'}
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

campus_schema = {
    'requered': ['sigla', 'cidade'],
    'properties': {
        'sigla': {'type': 'string'},
        'cidade': {'type': 'string'}
    }

}

turma_schema = {
    'requered': ['nome', 'fk_id_curso'],
    'properties': {
        'nome': {'type': 'string'},
        'fk_id_curso': {'type': 'integer'}
    }

}

disciplina_schema = {
    'requered': ['nome', 'fk_id_professor'],
    'properties': {
        'nome': {'type': 'string'},
        'fk_id_professor': {'type': 'integer'}
    }

}

professor_schema = {
    'requered': ['nome', 'fk_id_endereco'],
    'properties': {
        'nome': {'type': 'string'},
        'fk_id_endereco': {'type': 'integer'}
    }
}

Nome_DB = "EscolaApp_versao2.db"

@app.route("/alunos", methods=['GET'])
def getAlunos(): #testado ok
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
def getAluno(id): # testado ok
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
def setAlunos(): # testado ok
    logger.info("Cadastrando aluno.")
    aluno = request.get_json()
    nome = aluno['nome']
    matricula = aluno['matricula']
    cpf = aluno['cpf']
    nascimento = aluno['nascimento']
    id_endereco = aluno['fk_id_endereco']
    id_curso = aluno['fk_id_curso']

    conn = sqlite3.connect(Nome_DB)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_aluno(nome, matricula, cpf, nascimento, fk_id_endereco, fk_id_curso)
        VALUES(?, ?, ?, ?, ?, ?);
    """, (nome, matricula, cpf, nascimento, id_endereco, id_curso))
    conn.commit()
    conn.close()

    id = cursor.lastrowid
    aluno['id_aluno'] = id

    return (jsonify(aluno))


@app.route("/aluno/<int:id>", methods=['PUT'])
def updateAluno(id):
    # Receber o JSON.
    aluno = request.get_json()
    nome = aluno['nome']
    matricula = aluno['matricula']
    cpf = aluno['cpf']
    nascimento = aluno['nascimento']
    id_endereco = aluno['fk_id_endereco']
    id_curso = aluno['fk_id_curso']

    # Buscar o aluno pelo "id".
    conn = sqlite3.connect(Nome_DB)
    cursor = conn.cursor()

    # Executar a consulta de pesquisa.​​
    cursor.execute("""
        SELECT * FROM tb_aluno WHERE id_aluno = ?;
    """, (id, ))

    data = cursor.fetchone()

    if data is not None:
        # Atualizar os dados caso o aluno seja encontrado através do "id".
        cursor.execute("""
            UPDATE tb_aluno
            SET nome=?, matricula=?, cpf=?, nascimento=?, fk_id_endereco=?, fk_id_curso=?
            WHERE id_aluno = ?;
        """, (nome, matricula, cpf, nascimento, id_endereco, id_curso, id))
        conn.commit()
    else:
        print("Inserindo")
        # Inserir novo registro.
        cursor.execute("""
            INSERT INTO tb_aluno(nome, matricula, cpf, nascimento, fk_id_endereco, fk_id_curso)
            VALUES(?, ?, ?, ?, ?, ?);
        """, (nome, matricula, cpf, nascimento, id_endereco, id_curso))
        conn.commit()
        # Identificador do último registro inserido.
        id = cursor.lastrowid
        aluno["id_aluno"] = id

    conn.close()

    #Retornar o JSON do aluno atualizado.
    return jsonify(aluno)


@app.route("/enderecos", methods=['GET'])
def getEnderecos(): # testado ok
    logger.info("Listanto endereco.")
    try:
        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_endereco;
        """)

        #alterações
        enderecos = []
        for linha in cursor.fetchall():
            endereco = {
                "id_endereco":linha[0],
                "logradouro":linha[1],
                "complemento":linha[2],
                "bairro":linha[3],
                "cep":linha[4],
                "numero": linha[5]
            }
            enderecos.append(endereco)
        logger.info(enderecos)
        conn.close()
    except sqlite3.Error:
        return("Ocorreu um erro.")
    return jsonify(enderecos)

@app.route("/enderecos/<int:id>", methods=['GET'])
def getEndereco(id): # testado ok
    try:
        logger.info("Listanto endereco pelo id: %s."%(id))
        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_endereco WHERE id_endereco = ?;
        """, (id, ))

        linha = cursor.fetchone()
        endereco = {
            "id_endereco":linha[0],
            "logradouro":linha[1],
            "complemento":linha[2],
            "bairro":linha[3],
            "cep":linha[4],
            "numero": linha[5]
        }

        conn.close()
    except sqlite3.Error:
        return("Ocorreu um erro.")
    return jsonify(endereco)

@app.route("/endereco", methods=['POST'])
@schema.validate(endereco_schema) # testado ok
def setEndereco():
    logger.info("Cadastrando endereco.")
    try:
        endereco = request.get_json()
        logradouro = endereco['logradouro']
        complemento = endereco['complemento']
        bairro = endereco['bairro']
        cep = endereco['cep']
        numero = endereco['numero']

        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tb_endereco(logradouro, complemento, bairro, cep, numero)
            VALUES(?, ?, ?, ?, ?);
        """, (logradouro, complemento, bairro, cep, numero))
        conn.commit()
        conn.close()

        id = cursor.lastrowid
        endereco['id_endereco'] = id
    except sqlite3.Error:
        return("Ocorreu um erro.")

    return jsonify(endereco)

@app.route("/endereco/<int:id>", methods=['PUT'])
def updateEndereco(id):
    # Receber o JSON.
    endereco = request.get_json()
    logradouro = endereco['logradouro']
    complemento = endereco['complemento']
    bairro = endereco['bairro']
    cep = endereco['cep']
    numero = endereco['numero']


    # Buscar o aluno pelo "id".
    conn = sqlite3.connect(Nome_DB)
    cursor = conn.cursor()

    # Executar a consulta de pesquisa.​​
    cursor.execute("""
        SELECT * FROM tb_endereco WHERE id_endereco = ?;
    """, (id, ))

    data = cursor.fetchone()

    if data is not None:
        # Atualizar os dados caso o aluno seja encontrado através do "id".
        cursor.execute("""
            UPDATE tb_endereco
            SET logradouro=?, complemento=?, bairro=?, cep=?, numero=?
            WHERE id_endereco = ?;
        """, (logradouro, complemento, bairro, cep, numero, id))
        conn.commit()
    else:
        print("Inserindo")
        # Inserir novo registro.
        cursor.execute("""
            INSERT INTO tb_endereco(logradouro, complemento, bairro, cep, numero)
            VALUES(?, ?, ?, ?, ?);
        """, (logradouro, complemento, bairro, cep, numero))
        conn.commit()
        # Identificador do último registro inserido.
        id = cursor.lastrowid
        endereco["id_endereco"] = id

    conn.close()

    #Retornar o JSON do aluno atualizado.
    return jsonify(endereco)



@app.route("/cursos", methods=['GET'])
def getCursos(): #testado ok
    logger.info("Listanto cursos.")
    try:
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
                "turno":linha[2],
                "id_turno": linha[3]
            }
            cursos.append(curso)

        conn.close()
    except(sqlite3.Error):
        logger.error("Ocorreu um erro.")

    return jsonify(cursos)


@app.route("/cursos/<int:id>", methods=['GET'])
def getCurso(id): #testado ok
    logger.info("Listanto curso pelo id: %s"%(id))
    try:
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
            "turno":linha[2],
            "id_turno":linha[3] #aqui
        }
        conn.close()
    except(sqlite3.Error):
        logger.error("Ocorreu um erro.")
    return jsonify(curso)

@app.route("/curso", methods=['POST'])
@schema.validate(curso_schema)
def setCurso(): #testado ok
    logger.info("Cadastrando curso.")
    try:
        curso = request.get_json()
        nome = curso['nome']
        turno = curso['turno'] #retirar turno do bd
        id_turno = curso['fk_id_turno']

        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tb_curso(nome, turno, fk_id_turno)
            VALUES(?,?, ?);
        """, (nome, turno, id_turno))

        conn.commit()
        conn.close()

        id = cursor.lastrowid
        curso["id_curso"] = id
    except sqlite3.Error:
        return("Ocorreu um erro.")

    return(jsonify(curso))

@app.route("/curso/<int:id>", methods=['PUT'])
def updateCurso(id):
    # Receber o JSON.
    curso = request.get_json()
    nome = curso['nome']
    turno = curso['turno']
    id_turno = curso['fk_id_turno']

    # Buscar o aluno pelo "id".
    conn = sqlite3.connect(Nome_DB)
    cursor = conn.cursor()

    # Executar a consulta de pesquisa.​​
    cursor.execute("""
        SELECT * FROM tb_curso WHERE id_curso = ?;
    """, (id, ))

    data = cursor.fetchone()

    if data is not None:
        # Atualizar os dados caso o aluno seja encontrado através do "id".
        cursor.execute("""
            UPDATE tb_curso
            SET nome=?, turno=?, fk_id_turno=?
            WHERE id_curso = ?;
        """, (nome, turno, id_turno, id))
        conn.commit()
    else:
        print("Inserindo")
        # Inserir novo registro.
        cursor.execute("""
            INSERT INTO tb_curso(nome, turno, fk_id_turno)
            VALUES(?, ?, ?);
        """, (nome, turno, id_turno))
        conn.commit()
        # Identificador do último registro inserido.
        id = cursor.lastrowid
        curso["id_curso"] = id

    conn.close()

    #Retornar o JSON do aluno atualizado.
    return jsonify(curso)



@app.route("/turnos")
def getTurnos(): # testado ok
    logger.info("Listando turno.")

    try:
        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM tb_turno;
        """)

        turnos = []
        for linha in cursor.fetchall():
            turno = {
                "id_turno":linha[0],
                "nome": linha[1]
            }
            turnos.append(turno)
        logger.info(turnos)

        conn.close()
    except(sqlite3.Error):
        logger.error("Ocorreu um erro.")
    return jsonify(turnos)

@app.route("/turnos/<int:id>", methods=['GET'])
def getTurno(id): # testado ok
    logger.info("Listanto turno pelo id: %s"%(id))
    try:
        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_turno WHERE id_turno = ?;
        """, (id, ))

        linha = cursor.fetchone()
        turno = {
            "id_turno":linha[0],
            "nome":linha[1]
        }
        conn.close()
    except(sqlite3.Error):
        logger.error("Ocorreu um erro.")
    return jsonify(turno)


@app.route("/turno", methods=['POST'])
@schema.validate(turno_schema) # testado ok
def setTurno():
    try:
        turno = request.get_json()
        nome = turno['nome']

        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tb_turno(nome)
            VALUES(?);
        """, (nome, ))
        conn.commit()
        conn.close()

        id = cursor.lastrowid
        turno["id_turno"] = id
    except(sqlite3.Error):
        logger.error("Ocorreu um erro.")
    return jsonify(turno)


@app.route("/turno/<int:id>", methods=['PUT'])
def updateTurno(id):
    # Receber o JSON.
    turno = request.get_json()
    nome = turno['nome']

    # Buscar o aluno pelo "id".
    conn = sqlite3.connect(Nome_DB)
    cursor = conn.cursor()

    # Executar a consulta de pesquisa.​​
    cursor.execute("""
        SELECT * FROM tb_turno WHERE id_turno = ?;
    """, (id, ))

    data = cursor.fetchone()

    if data is not None:
        # Atualizar os dados caso o aluno seja encontrado através do "id".
        cursor.execute("""
            UPDATE tb_turno
            SET nome=?
            WHERE id_turno = ?;
        """, (nome, id))
        conn.commit()
    else:
        print("Inserindo")
        # Inserir novo registro.
        cursor.execute("""
            INSERT INTO tb_turno(nome)
            VALUES(?);
        """, (nome))
        conn.commit()
        # Identificador do último registro inserido.
        id = cursor.lastrowid
        turno["id_turno"] = id

    conn.close()

    #Retornar o JSON do aluno atualizado.
    return jsonify(turno)



@app.route("/escolas", methods=['GET'])
def getEscolas(): # testado ok
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
def getEscola(id): # testado ok
    logger.info("Listanto escola pelo id: %s"%(id))
    try:
        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_escola WHERE id_escola = ?;
        """, (id, ))

        linha = cursor.fetchone()
        escola = {
            "id_escola":linha[0],
            "nome":linha[1],
            "id_endereco":linha[2],
            "id_campus":linha[3]
        }
        conn.close()
    except(sqlite3.Error):
        logger.error("Ocorreu um erro.")
    return jsonify(escola)


@app.route("/escola", methods=['POST'])
@schema.validate(escola_schema)
def setEscolas(): # testado ok
    logger.info("Cadastrando escola.")
    escola = request.get_json()
    nome = escola['nome']
    id_endereco = escola['fk_id_endereco']
    id_campus = escola['fk_id_campus']

    conn = sqlite3.connect(Nome_DB)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_escola(nome, fk_id_endereco, fk_id_campus)
        VALUES(?, ?, ?);
    """, (nome, id_endereco, id_campus))
    conn.commit()
    conn.close()

    id = cursor.lastrowid
    escola['id_escola'] = id

    return (jsonify(escola))


@app.route("/escola/<int:id>", methods=['PUT'])
def updateEscola(id):
    # Receber o JSON.
    escola = request.get_json()
    nome = escola['nome']
    id_endereco = escola['fk_id_endereco']
    id_campus = escola['fk_id_campus']

    conn = sqlite3.connect(Nome_DB)
    cursor = conn.cursor()

    # Executar a consulta de pesquisa.​​
    cursor.execute("""
        SELECT * FROM tb_escola WHERE id_escola = ?;
    """, (id, ))

    data = cursor.fetchone()

    if data is not None:

        cursor.execute("""
            UPDATE tb_escola
            SET nome=?, fk_id_endereco=?, fk_id_campus=?
            WHERE id_escola = ?;
        """, (nome, id_endereco, id_campus, id))
        conn.commit()
    else:
        print("Inserindo")
        # Inserir novo registro.
        cursor.execute("""
            INSERT INTO tb_escola(nome, fk_id_endereco, fk_id_campus)
            VALUES(?, ?, ?);
        """, (nome, id_endereco, id_campus))
        conn.commit()
        # Identificador do último registro inserido.
        id = cursor.lastrowid
        escola["id_escola"] = id

    conn.close()

    #Retornar o JSON do aluno atualizado.
    return jsonify(escola)


@app.route("/campi")
def getCampi(): # testado ok
    logger.info("Listando campi.")

    try:
        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM tb_campus;
        """)

        campi = []
        for linha in cursor.fetchall():
            campus = {
                "id_campus":linha[0],
                "sigla": linha[1],
                "cidade": linha[2]
            }
            campi.append(campus)
        logger.info(campi)

        conn.close()
    except(sqlite3.Error):
        logger.error("Ocorreu um erro.")
    return jsonify(campi)

#####continuar updates

@app.route("/campi/<int:id>", methods=['GET'])
def getCampus(id): # testado ok
    logger.info("Listanto campus pelo id: %s"%(id))
    try:
        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_campus WHERE id_campus = ?;
        """, (id, ))

        linha = cursor.fetchone()
        campus = {
            "id_campus":linha[0],
            "sigla":linha[1],
            "cidade":linha[2]
        }
        conn.close()
    except(sqlite3.Error):
        logger.error("Ocorreu um erro.")
    return jsonify(campus)

@app.route("/campus", methods=['POST'])
@schema.validate(campus_schema)
def setCampus(): # testado ok
    try:
        campus = request.get_json()
        sigla = campus['sigla']
        cidade = campus['cidade']

        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tb_campus(sigla, cidade)
            VALUES(?, ?);
        """, (sigla, cidade))
        conn.commit()
        conn.close()

        id = cursor.lastrowid
        campus["id_campus"] = id
    except(sqlite3.Error):
        logger.error("Ocorreu um erro.")
    return jsonify(campus)


@app.route("/turmas", methods=['GET'])
def getTurmas(): # testado ok
    logger.info("Listanto turmas.")
    try:
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
                "id_curso":linha[2]
            }
            turmas.append(turma)
        conn.close()
    except(sqlite3.Error):
        logger.error("Ocorreu um erro.")
    return jsonify(turmas)



@app.route("/turmas/<int:id>", methods=['GET'])
def getTurma(id): #testado ok
    logger.info("Listanto turma pelo id.")
    try:
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
            "id_curso":linha[2]
        }

        conn.close()
    except(sqlite3.Error):
        logger.error("Ocorreu um erro")
    return jsonify(turma)

@app.route("/turma", methods=['POST'])
@schema.validate(turma_schema)
def setTurma(): # testado ok
    try:
        turma = request.get_json()
        nome = turma['nome']
        id_curso = turma['fk_id_curso']

        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tb_turma(nome, fk_id_curso)
            VALUES(?, ?);
        """, (nome, id_curso))
        conn.commit()
        conn.close()

        id = cursor.lastrowid
        turma["id_turma"] = id
    except(sqlite3.Error):
        logger.error("Ocorreu um erro.")
    return jsonify(turma)


@app.route("/disciplinas", methods=["GET"])
def getDisciplinas(): # testado ok
    logger.info("Listanto disciplinas.")
    try:
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
                "nome":linha[1],
                "id_professor": linha[2]
            }
            disciplinas.append(disciplina)
        conn.close()
    except(sqlite3.Error):
        logger.error("Ocorreu um erro.")
    return jsonify(disciplinas)



@app.route("/disciplinas/<int:id>", methods=['GET'])
def getDisciplina(id): # testado ok
    try:
        logger.info("Listanto disciplina pelo id: %s."%(id))
        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_disciplina WHERE id_disciplina = ?;
        """, (id, ))

        linha = cursor.fetchone()
        disciplina = {
            "id_disciplina":linha[0],
            "nome":linha[1],
            "fk_id_professor": linha[2]
        }

        conn.close()
    except sqlite3.Error:
        return("Ocorreu um erro.")
    return jsonify(disciplina)

@app.route("/disciplina", methods=['POST'])
@schema.validate(disciplina_schema) # testado ok
def setDisciplina():
    try:
        disciplina = request.get_json()
        nome = disciplina['nome']
        id_professor = disciplina['fk_id_professor']

        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tb_disciplina(nome, fk_id_professor)
            VALUES(?, ?);
        """, (nome, id_professor))
        conn.commit()
        conn.close()

        id = cursor.lastrowid
        disciplina["id_disciplina"] = id
    except(sqlite3.Error):
        logger.error("Ocorreu um erro.")
    return jsonify(disciplina)

@app.route("/professores", methods=['GET'])
def getProfessores(): # testado ok
    logger.info("Listanto professores.")
    try:
        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_professor;
        """)

        #alterações
        professores = []
        for linha in cursor.fetchall():
            professor = {
                "id_professor":linha[0],
                "nome":linha[1],
                "fk_id_endereco": linha[2]
            }
            professores.append(professor)
        logger.info(professores)
        conn.close()
    except sqlite3.Error:
        return("Ocorreu um erro.")
    return jsonify(professores)


@app.route("/professores/<int:id>", methods=['GET'])
def getProfessor(id): # testado ok
    try:
        logger.info("Listanto professor pelo id: %s."%(id))
        conn = sqlite3.connect(Nome_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_professor WHERE id_professor = ?;
        """, (id, ))

        linha = cursor.fetchone()
        professor = {
            "id_professor":linha[0],
            "nome":linha[1],
            "fk_id_endereco": linha[2]
        }

        conn.close()
    except sqlite3.Error:
        return("Ocorreu um erro.")
    return jsonify(professor)

@app.route("/professor", methods=['POST'])
@schema.validate(professor_schema)
def setProfessor(): # testado ok
    logger.info("Cadastrando professor.")
    professor = request.get_json()
    nome = professor['nome']
    id_endereco = professor['fk_id_endereco']

    conn = sqlite3.connect(Nome_DB)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_professor(nome, fk_id_endereco)
        VALUES(?, ?);
    """, (nome,id_endereco))
    conn.commit()
    conn.close()

    id = cursor.lastrowid
    professor['id_professor'] = id

    return (jsonify(professor))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
