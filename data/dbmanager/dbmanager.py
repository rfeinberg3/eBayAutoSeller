import pandas
import psycopg2
from psycopg2.extras import RealDictCursor

class DatabaseManager:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def create_db(self):
        conn = psycopg2.connect(dbname='postgres', user=self.user, password=self.password, host=self.host, port=self.port)
        conn.autocommit = True
        cur = conn.cursor()
        
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{self.dbname}'")
        exists = cur.fetchone()

        if exists == None:
            cur.execute(f"CREATE DATABASE {self.dbname};")
            print(f"Database '{self.dbname}' created.")
        else:
            print(f"Database '{self.dbname}' already exists.")
        
        cur.close()
        conn.close()

    def execute_sql_file(self, file_path):
        conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)
        cur = conn.cursor()

        with open(file_path, 'r') as sql_file:
            sql_script = sql_file.read()
            cur.execute(sql_script)
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"SQL script from {file_path} executed successfully.")

    def table_to_pandas(self, table_name):
        conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f"SELECT * FROM {table_name}")
            rows = cur.fetchall()
            
            # Convert rows to a list of dictionaries, then to df
            data = [dict(row) for row in rows]
            data = pandas.DataFrame(data)
            conn.close()
        return data