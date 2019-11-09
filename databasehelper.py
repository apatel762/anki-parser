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
        except sqlite3.OperationalError as oe:
            DatabaseHelper.log_sqlite_error_before_throwing_error()
            raise oe
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
        except sqlite3.OperationalError as oe:
            DatabaseHelper.log_sqlite_error_before_throwing_error()
            raise oe
        finally:
            conn.close()

    @staticmethod
    def log_sqlite_error_before_throwing_error():
        print("")
        print("ERROR!")
        print("There is a problem with the database.")
        print("")
        print("If running on Linux: make sure that the database filepath ")
        print("does not use '~' but instead uses '/home/user' (where user ")
        print("is your current user's name).")
        print("")
        print("Also, make sure that Anki is closed, or you'll get an ")
        print("exception saying the database is locked.")
        print("")

    @staticmethod
    def __first_word(query):
        return query.split()[0].lower()

    @staticmethod
    def __get_database_filepath():
        with open("db-location.txt", 'r') as file:
            filepath = file.readlines()[0]
            return filepath.rstrip("\n")
