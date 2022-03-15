import sqlite3
database = r"/home/teo/proyectos/BD_sqlite/mi_bd.sqlite"
db_bk = r"/home/teo/proyectos/BD_sqlite/mi_bk.sqlite"


def progress(status, remaining, total):
    print(f'Copied {total-remaining} of {total} pages...')

con = sqlite3.connect(database)
bck = sqlite3.connect(db_bk)
with bck:
    con.backup(bck, pages=1, progress=progress)
bck.close()
con.close()