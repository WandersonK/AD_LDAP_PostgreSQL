from ldap3 import Server, Connection, ALL
from credentials import ldap_auth as cl

server_ldap = Server(cl.get('server_ldap'), get_info=ALL)
conn_ldap = Connection(server_ldap, cl.get('user_ldap'), cl.get('pass_ldap'), auto_bind=True)

conn_ldap.search(f'dc={cl.get("dc")},dc={cl.get("dc")}', '(&(objectclass=user)(!(objectclass=computer)))', attributes=['sAMAccountName','memberOf'])

gps_discard_ldap = ('CN=USB_Liberado', 'CN=USB_Bloqueado', 'CN=CD_Bloqueado', 'CN=CD_Liberado') #  Grupos a descartados
