import sqlite3

class DatabaseHelper(object):
    """
    A class containing methods that can be used to safely interface with
    a database
    """
    @staticmethod
    def placeholder():
        pass

    @staticmethod
    def select(path, query):
        """
        A helper method for running select queries

        :param path: The full filepath to a database
        :param query: The query to run
        :returns: The result of the query, as a list.
        """
        conn = sqlite3.connect(path)
        try:
            c = conn.cursor()
            c.execute(query)
            return c.fetchall()
        except Exception as e:
            raise e
        finally:
            conn.close()

if __name__ == '__main__':
    path = 'C:\\Users\\Arjun Patel\\AppData\\Roaming\\Anki2\\Arjun\\collection.anki2'
    query = 'select n.flds '
    query += 'from cards c '
    query += 'join notes n on c.nid = n.id '
    query += 'where c.type = 2 '
    query += 'and c.did = 1543218842369'
    for row in DatabaseHelper.select(path, query):
        print(row[0].split("\x1f")[4])