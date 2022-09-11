from flask_mysqldb import MySQL

db = MySQL()

class ConexionDB:
    def fetch(self,query):
        cursor = db.connection.cursor()
        cursor.execute(query)
        datos = cursor.fetchall()
        return datos

    def save(aelf,query):
        cursor = db.connection.cursor()
        cursor.execute(query)
        db.connection.commit()