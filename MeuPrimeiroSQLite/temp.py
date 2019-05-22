import sqlite3

# conecta aí parceiro
conn = sqlite3.connect('shallownowschool.db')

# define um cursor para pegar os dados
cursor = conn.cursor()

#inserir valores um de cada vez.
cursor.execute("""
    INSERT INTO tb_estudante(nome, endereco, nascimento, matricula)
    VALUES('maria do bairro', 'rua da paz', '2018-01-01', '201810010010');
""")

conn.commit()
print("inserido bem top com sucesso")
conn.close()
