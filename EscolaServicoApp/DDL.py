import sqlite3

conn = sqlite3.connect('ifpb.db')

cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE tb_escola(
        id_escola INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(45) NOT NULL,
        logradouro VARCHAR(70) NOT NULL,
        cidade VARCHAR(45) NOT NULL
    );
""")
print("Tabela escola criada com sucesso!")

cursor.execute("""
    CREATE TABLE tb_aluno(
        id_aluno INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(45) NOT NULL,
        matricula VARCHAR(12) NOT NULL,
        cpf VARCHAR(11) NOT NULL,
        nascimento DATE NOT NULL
    );
""")
print("Tabela aluno criada com sucesso!")

cursor.execute("""
    CREATE TABLE tb_curso(
        id_curso INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(45) NOT NULL,
        turno VARCHAR(10) NOT NULL
    );
""")
print("Tabela curso criada com sucesso!")

cursor.execute("""
    CREATE TABLE tb_turma(
        id_turma INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(45) NOT NULL,
        curso VARCHAR(45) NOT NULL
    );
""")
print("Tabela turma criada com sucesso!")

cursor.execute("""
    CREATE TABLE tb_disciplina(
        id_disciplina INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(45)
    );
""")
print("Tabela disciplina criada com sucesso!")


conn.close()
