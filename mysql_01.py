# https://realpython.com/python-mysql/
from mysql.connector import connect, Error

show_db_query = "SHOW DATABASES"
clientes_query = "select c.nombre_cliente , c.nombre_contacto , c.apellido_contacto from cliente c "
   
try:
    with connect(
        host="localhost",
        user='root',
        password='root',
        database="jardineria"

    ) as connection:
        with connection.cursor(dictionary = True) as cursor:
            cursor.execute(clientes_query)
            desc = cursor.description
            print(desc)
            result = cursor.fetchall()
            print(result)
            for fila in result:
                print(fila)
        
        
except Error as e:
    print(e)


