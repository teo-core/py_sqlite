# Ref: https://www.programcreek.com/python

#1.- Creación de una base de datos sqlite desde Python
#2.- Creación de una tabla
#3.- Inserción de registros
#4.- Selección de registros
#5.- Modificación de registros
#6.- Borrado de registros
#7.- Eliminación de base de datos
# ---------------------------------------------------------------

#1.- Creación de una base de datos sqlite desde Python

import sqlite3
from sqlite3 import Error
database = r"/home/teo/proyectos/BD_sqlite/mi_bd.sqlite"

def crea_conexion(db_file):
    """ Crear una nueva conexión a BD sqlite """
    cnx = None
    try:
        #cnx = sqlite3.connect(db_file)
        cnx = sqlite3.connect(':memory:')

        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if cnx:
            cnx.close()




#2.- Creación de una tabla
tabla_projects = """
-- projects table
CREATE TABLE IF NOT EXISTS projects (
	id integer PRIMARY KEY,
	name text NOT NULL,
	begin_date text,
	end_date text
);"""

tabla_tareas = """-- tasks table
CREATE TABLE IF NOT EXISTS tasks (
	id integer PRIMARY KEY,
	name text NOT NULL,
	priority integer,
	project_id integer NOT NULL,
	status_id integer NOT NULL,
	begin_date text NOT NULL,
	end_date text NOT NULL,
	FOREIGN KEY (project_id) REFERENCES projects (id)
);"""

# if __name__ == '__main__':
#     crea_conexion(database)


def create_connection(db_file):
    """ Crea una conexión a la BD especificada por db_file
    :param db_file: archivo de BD
    :return: Objeto connection o None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ crea una tabla a partir de la cadena sql
    :param conn: Objeto conexión
    :param create_table_sql: Instrucción CREATE TABLE
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
   

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, tabla_projects)

        # create tasks table
        create_table(conn, tabla_tareas)
    else:
        print("Error! No se puede crear la conexión a la base de datos.")


#main()

#3.- Inserción de registros

def create_project(conn, project):
    """
    Inserta una nueva fila en la tabla projects
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def create_task(conn, task):
    """
    Crea una nueva tarea
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid

def main_ins():
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new project
        project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
        project_id = create_project(conn, project)

        # tasks
        task_1 = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
        task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')

        # create tasks
        create_task(conn, task_1)
        create_task(conn, task_2)

#main_ins()

# 4.- Selección de registros

"""
To query data in an SQLite database from Python, you use these steps:

    First, establish a connection to the SQLite database by creating a Connection object.
    Next, create a Cursor object using the cursor method of the Connection object.
    Then, execute a  SELECT statement.
    After that, call the fetchall() method of the cursor object to fetch the data.
    Finally, loop the cursor and process each row individually.
"""
def select_all_tasks(conn):
    """
    Muestra todas las tareas
    :param conn: Objeto conexión
    :return:
    """
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks")
    desc = cur.description
    print(desc)
    rows = cur.fetchall()

    for row in rows:
        print(row)

def select_task_by_priority(conn, priority):
    """
    Tareas por prioridad
    :param conn: Objeto conexión
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))

    rows = cur.fetchall()

    for row in rows:
        print(row)

def main_sel():
    
    # crea conexión
    conn = create_connection(database)
    with conn:
        print("1. Consulta de tareas por prioridad:")
        select_task_by_priority(conn, 1)

        print("2. Consulta todas las tareas")
        select_all_tasks(conn) 

main_sel()

"""
To update data in a table from a Python program, you follow these steps:

    First, create a database connection to the SQLite database using the connect() function. 
    Once the database connection created, you can access the database using the Connection object.
    Second, create a Cursor object by calling the cursor() method of the Connection object.
    Third, execute the UPDATE statement by calling the execute() method of the Cursor object.

In this example we will update the priority, begin date, and end date of a specific task in the tasks table.
"""       
def update_task(conn, task):
    """
    Actualizar los campos priority, begin_date, and end date de una tarea
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tasks
              SET priority = ? ,
                  begin_date = ? ,
                  end_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

def main_upd():

    # create a database connection
    conn = create_connection(database)
    with conn:
        update_task(conn, (2, '2015-01-04', '2015-01-06', 2))

#main_upd()

#6.- Borrado de registros

"""
In order to delete data in the SQLite database from a Python program, you use the following steps:

    First, establish a connection the SQLite database by creating a Connection object using the connect() function.
    Second, to execute a DELETE statement, you need to create a Cursor object using the cursor() method of the Connection object.
    Third, execute the  DELETE statement using the execute() method of the Cursor object. In case you want to pass the arguments to the statement, you use a question mark ( ?) for each argument.
"""

def delete_task(conn, id):
    """
    Borra una tarea a partir de su id
    :param conn:  Conexiópn a la bd
    :param id: id de la tarea
    :return:
    """
    sql = 'DELETE FROM tasks WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def delete_all_tasks(conn):
    """
    Borra todas las tareas de la tabla
    :param conn: Conexión a la bd
    :return:
    """
    sql = 'DELETE FROM tasks'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def main_del():

    # create a database connection
    conn = create_connection(database)
    with conn:
        delete_task(conn, 2);
        # delete_all_tasks(conn);

#main_del()