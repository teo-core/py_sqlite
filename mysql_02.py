# https://realpython.com/python-mysql/
from mysql.connector import connect, Error
import sys

show_db_query = "SHOW DATABASES"
clientes_query = "select c.nombre_cliente , c.nombre_contacto , c.apellido_contacto from cliente c "

def conecta():
    try:
        cnx = connect(host="localhost",
        user='root',
        password='root',
        database="jardineria")
    except Exception as e:
        raise e
    return cnx

try:
    cnx = conecta()
except Exception as e:
    print(e.msg)
    sys.exit()

sql_select_Query = "select nombre_cliente from cliente"
cursor = cnx.cursor(dictionary=False)
cursor.execute(sql_select_Query)
# get all records
records = cursor.fetchall()
for fila in records:
    print(fila)