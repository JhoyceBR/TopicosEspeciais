import sqlite3

conn = sqlite3.connect('escola.db')

cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE TB_ALUNO(
        ID_ALUNO INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        NOME VARCHAR(45) NOT NULL,
        MATRICULA VARCHAR(12) NOT NULL,
        CPF VARCHAR(11) NOT NULL,
        NASCIMENTO DATE NOT NULL
    );
""")

print("Tabela Aluno criada com sucesso!")

cursor.execute("""
    CREATE TABLE TB_CURSO(
        ID_CURSO INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        NOME VARCHAR(45) NOT NULL,
        TURNO VARCHAR(1) NOT NULL
    );
""")

print("Tabela Curso criada com sucesso!")

cursor.execute("""
    CREATE TABLE TB_TURMA(
        ID_TURMA INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        FK_ID_CURSO INTEGER NOT NULL
    );
""")

print("Tabela Turma criada com sucesso!")
print("Tablelas criadas com sucesso!")

conn.close()
