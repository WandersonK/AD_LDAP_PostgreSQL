from credentials import db_auth as cpg
import psycopg
import connect_ldap

def comp_pgldap(username_ldap, groupuser_ldap):
    # data_insert = ''
    verify = 1
    connection_pg = psycopg.connect(
        host=cpg.get('host_pg'), 
        port=cpg.get('port_pg'), 
        dbname=cpg.get('database_pg'), 
        user=cpg.get('user_pg'), 
        password=cpg.get('pass_pg')
    )
    
    cur = connection_pg.cursor()
    
    sql_users = f'SELECT login, active FROM {cpg.get("schema")}.sec_users;'
    sql_groups = f'SELECT description, group_id FROM {cpg.get("schema")}.sec_groups;'
    sql_users_groups = f'SELECT login, group_id FROM {cpg.get("schema")}.sec_users_groups;'
    
    cur.execute(sql_users)
    res_users = cur.fetchall()
    
    cur.execute(sql_groups)
    res_groups = cur.fetchall()
    
    cur.execute(sql_users_groups)
    res_users_groups = cur.fetchall()
    
    for r_user in res_users:
        if username_ldap in r_user and r_user[1] == 'Y':
            
            for r_group in res_groups:
                if groupuser_ldap in r_group:
                    
                    for r_user_group in res_users_groups:
                        # data_insert = f'{username_ldap}, {r_group[1]}'
                        sql_insert = f"INSERT INTO {cpg.get('schema')}.sec_users_groups (login, group_id) VALUES ('{username_ldap}', {r_group[1]})"
                        verify = 0
                        if username_ldap == r_user_group[0] and r_group[1] == r_user_group[1]:
                            verify = 1
                            break
                        
            if verify == 0:
                # print(data_insert)
                cur.execute(sql_insert)
                connection_pg.commit()

    connection_pg.close()

for i1 in connect_ldap.conn_ldap.entries:
    user_name = i1.sAMAccountName
    
    for i2 in i1.memberOf:
        grupos = i2.split(',')
        
        for i3 in grupos:
            if i3.startswith('CN=') and not i3.startswith(connect_ldap.gps_discard_ldap):
                group_user = i3.split('=')[1]
                comp_pgldap(user_name, group_user)
