import sqlite3

conn = sqlite3.connect('shallownowschool.db')
cursor = conn.cursor()
#lista dos valores
lista = [('Jose', 'rua projetada', '2011-05-21', '201371001001'), ('luiz', 'rua da luz', '2000-02-14', '201513710012')]

#executemany porque são varias consultas
cursor.executemany("""
    INSERT INTO tb_estudante(nome, endereco,
    nascimento, matricula)
    VALUES(?, ?, ?, ?);
""", lista)

conn.commit()
print('valores inseridos com sucesso')
conn.close()
