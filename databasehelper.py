import sqlite3

class DatabaseHelper(object):
    """
    A class containing methods that can be used to safely interface with
    a database
    """
    @staticmethod
    def execute(query):
        """
        A helper method for running queries and keeping the main code clean.

        :param query: The query to run
        :returns: The result of the query.
        """
        if query is None:
            return RuntimeError("The given query is empty.")

        if DatabaseHelper.__first_word(query) == "select":
            return DatabaseHelper.__execute_select_query(query)
        elif DatabaseHelper.__first_word(query) == "update":
            return DatabaseHelper.__execute_update_query(query)
        else:
            raise RuntimeError(f'Please check the query syntax for: {query}')

    @staticmethod
    def __execute_select_query(query):
        conn = sqlite3.connect(DatabaseHelper.__get_database_filepath())
        try:
            c = conn.cursor()
            c.execute(query)
            return c.fetchall()
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def __execute_update_query(query):
        conn = sqlite3.connect(DatabaseHelper.__get_database_filepath())
        try:
            c = conn.cursor()
            c.execute(query)
            conn.commit()
            return True
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def __first_word(query):
        return query.split()[0].lower()

    @staticmethod
    def __get_database_filepath():
        with open("db-location.txt", 'r') as f:
            return f.readlines()[0]

    def test():
        query = 'select n.flds '
        query += 'from cards c '
        query += 'join notes n on c.nid = n.id '
        query += 'where c.type = 2 '
        query += 'and c.did = 1543218842369'
        for row in DatabaseHelper.execute(query):
            print(row[0].split("\x1f")[4])

if __name__ == '__main__':
    DatabaseHelper.test()