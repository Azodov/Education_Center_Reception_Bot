import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            phone varchar(255),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)


    def create_table_course(self):
        sql = """
        CREATE TABLE Course (
            Name varchar(255) NOT NULL,
            description varchar(255) NOT NULL
            );
"""
        self.execute(sql, commit=True)


    def create_table_user_course(self):
        sql = """
        CREATE TABLE Orders (
            Name varchar(255) NOT NULL,
            number varchar(255) NOT NULL,
            course_name varchar(255) NOT NULL,
            test_result varchar(255)
            );
"""
        self.execute(sql, commit=True)


    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, phone: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(id, Name, phone) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, phone), commit=True)

    def add_course(self, name: str, description: str):
        # SQL_EXAMPLE = "INSERT INTO Course(Name, email) VALUES(1, 'John', '
        sql = """
        INSERT INTO Course(Name, description) VALUES(?, ?)
        """
        self.execute(sql, parameters=(name, description), commit=True)

    def add_user_course(self, name: str, number: str, course_name: str, test_result: str):
        sql = """
        INSERT INTO Orders(Name, number, course_name, test_result) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(name, number, course_name, test_result), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_all_course(self):
        sql = """
            SELECT * FROM Course
            """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_last_orders(self):
        sql = """
        SELECT * FROM Orders ORDER BY ROWID DESC LIMIT 10
        """
        return self.execute(sql, fetchall=True)

    def select_course(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Course WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def delete_course(self, name):
        sql = f"""
        DELETE FROM Course WHERE Name=?
        """
        self.execute(sql, parameters=(name,), commit=True)



def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")