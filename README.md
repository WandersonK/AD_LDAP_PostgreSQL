# AD para POSTGRES

Este código tem por objetivo inserir em um banco Postgres, os usuários e grupos cadastrados no AD, via LDAP.

Primeiramente, deve-se criar um arquivo (credentials.py) com as credenciais necessárias, seguindo o modelo a seguir:

```
# credentials.py

db_auth = {
    'host_pg' : 'localhost', # Host do seu banco
    'port_pg' : '5432', # Porta do seu banco
    'database_pg' : 'teste', # Nome do seu banco
    'user_pg' : '*****************', # Usuário do seu banco
    'pass_pg' : '*****************', # Senha do seu banco
    'schema' : '*****************' # Schema do seu banco
    
}

ldap_auth = {
    'server_ldap' : '*****************', # Nome do seu servidor AD
    'user_ldap' : '*****************', # Um usuário admin do AD
    'pass_ldap' : '*****************', # Senha do usuário
    'dc' : '*****************' # DC do seu domínio
}
```

Pacotes necessário:

* pip install psycopg2
* pip install ldap3
