https://www.giacomodebidda.com/posts/mvc-pattern-in-python-sqlite/

from sqlite_01 import create_connection
database = r"/home/teo/proyectos/BD_sqlite/mi_bd.sqlite"

class Tarea():
    __tupla_props = ()
    name = ''
    priority = 0
    project_id = 0
    status_id = 0
    begin_date = None
    end_date = None
    def __init__(self, 
                pname='', 
                ppriority=0,
                pproject_id=0, 
                pstatus_id=0, 
                pbegin_date=None, 
                pend_date=None) -> None:
        self.name = pname
        self.priority = ppriority
        self.project_id = pproject_id
        self.status_id = pstatus_id
        self.begin_date = pbegin_date
        self.end_date = pend_date

        self.__tupla_props = tuple(self.__dict__.values())

    def save(self, cnx):
        sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
            VALUES(?,?,?,?,?,?) '''
        cur = cnx.cursor()
        cur.execute(sql, self.__tupla_props)
        cnx.commit()

        return cur.lastrowid

def main():
    
   
    mi_tarea = Tarea('otrop',1,1,3,'2022-03-01','2022-03-30')
    cnx = create_connection(database)
    nuevo_id = mi_tarea.save(cnx)
    print(nuevo_id)

main()