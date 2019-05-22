import sqlite3

# conecta aí parceiro
conn = sqlite3.connect('shallownowschool.db')

# define um cursor para pegar os dados
cursor = conn.cursor()
#cursor.execute("""
#    CREATE TABLE tb_estudante(
#        id INTEGER PRIMARY KEY AUTOINCREMENT,
#        nome VARCHAR(30) NOT NULL,
#        endereco TEXT NOT NULL,
#        nascimento DATE NOT NULL,
#        matricula VARCHAR(12) NOT NULL
#    );
#""")
cursor.execute("""
    SELECT * FROM tb_estudante;
""")

for linha in cursor.fetchall():
    print(linha[1], " #étrouxa")
    #para exibir so os nomes das pessoas: print(linha[1])
conn.close()
