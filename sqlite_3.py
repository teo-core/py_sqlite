# https://www.kylev.com/2009/05/22/python-decorators-and-database-idioms/


def dbwrap(func):
    """Wrap a function in an idomatic SQL transaction.  The wrapped function
    should take a cursor as its first argument; other arguments will be
    preserved.
    """
    def new_func(conn, *args, **kwargs):
        cursor = conn.cursor()
        try:
            cursor.execute("BEGIN")
            retval = func(cursor, *args, **kwargs)
            cursor.execute("COMMIT")
        except:
            cursor.execute("ROLLBACK")
            raise
        finally:
            cursor.close()

        return retval

    # Tidy up the help()-visible docstrings to be nice
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__

    return new_func


@dbwrap
def do_something(cursor, val1=1, val2=2):
    """Do that database thing."""
    cursor.execute("SELECT %s, %s", (val1, val2))
    return cursor.fetchall()


class SomeClass(object):
    def __init__(self):
        conn = MySQLdb.connect(db='test')
        self.instance_var = SomeClass.get_stuff(conn)
        print self.instance_var
        conn.close()

    @staticmethod
    @dbwrap
    def get_stuff(cursor):
        """Load something meaningful from the database."""
        cursor.execute("SELECT 'blah'")
        return cursor.fetchall()[0][0]


if '__main__' == __name__:
    conn = MySQLdb.connect(db='test')
    print do_something(conn)
    print do_something(conn, 3, 4)
    print do_something(conn, 5)
    print do_something(conn, val2=6)
    #help(do_something)

    s = SomeClass()
    #help(s)