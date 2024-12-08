import mysql.connector
from flask import g, current_app

class db:
    @staticmethod
    def init_app(app):
        # This method is kept empty for now unless you want to extend it in the future.
        pass


    @staticmethod
    def get_connection():
        if "db_conn" not in g:
            g.db_conn = mysql.connector.connect(
                host=current_app.config['DB_HOST'],
                port=current_app.config['DB_PORT'],
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASSWORD'],
                database=current_app.config['DB_NAME'],
                auth_plugin='mysql_native_password'
            )
        return g.db_conn

    @staticmethod
    def close_connection():
        db_conn = g.pop("db_conn", None)
        if db_conn is not None:
            db_conn.close()
