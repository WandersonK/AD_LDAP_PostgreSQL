from credentials import db_auth as cpg
import psycopg2
import connect_ldap

"""
CÓDIGOS DE STATUS DO LDAP PARA OS USUÁRIOS
    514	Conta desabilitada
    546	Conta desabilitada, senha não requerida
    66050	Conta desabilitada, senha não expira
    66082	Conta desabilitada, Senha não expira e não é requerida

    512	Conta habilitada
    544	Conta habilitada, senha não requerida
    66048	Conta habilitada, senha não expira
    66080	Conta habilitada, Senha não expira e não é requerida
"""

# Recebendo dados do AD via LDAP
dados_ldap = connect_ldap.conn_ldap.entries

# Instanciando duas listas para armazenar usuários do banco e AD
lista_usuarios_db = list()
lista_usuarios_ldap = list()

# Iniciando uma conexão com o banco
connection_pg = psycopg2.connect(
    host=cpg.get('host_pg'), 
    port=cpg.get('port_pg'), 
    dbname=cpg.get('database_pg'), 
    user=cpg.get('user_pg'), 
    password=cpg.get('pass_pg')
)

cur = connection_pg.cursor()

sql_users = f'SELECT login FROM {cpg.get("schema")}.sec_users;'

cur.execute(sql_users)
res_users = cur.fetchall()

# Populando uma lista com usuários do banco para agilizar no processamento do código
for r_user in res_users:
    lista_usuarios_db.append(r_user[0])

# Populando uma lista com usuários do AD para agilizar no processamento do código
for dado_individual in dados_ldap:
    lista_usuarios_ldap.append(str(dado_individual.sAMAccountName))

# Verifica se o usuário do Banco está no LDAP, e se não estiver, exclui
for user_db in lista_usuarios_db:
    if user_db not in lista_usuarios_ldap:
        
        sql_delete_usuario = f"DELETE FROM {cpg.get('schema')}.sec_users WHERE login = '{user_db}';"
        
        cur.execute(sql_delete_usuario)
        connection_pg.commit()

connection_pg.close()
