
import mysql.connector


"""DATABASE CONNECTION"""

def connectMySQL(host="localhost", user="root", passwd=""):   
    conection = mysql.connector.connect(host = host, user = user, passwd = passwd)
    return conection


def SQLCheck()->bool:    
    try:
        connectMySQL()
        return True
    except:
        return False




def dbList(console = False):
    conexion1 = connectMySQL()
    cursor1 = conexion1.cursor()
    cursor1.execute("SHOW DATABASES")
    listDB = []
    for base in cursor1:
        listDB.append(base)
    conexion1.close()
    if console == True: print(listDB)
    dbNames = []
    for i in listDB:
        if i[0] in (
            "information_schema",
            "phpmyadmin",
            "test",
            "performance_schema",
            "mysql",
            ):
            continue
        dbNames.append(i[0])
    if len(dbNames) == 0: return ["No Databases Found"] 
    return dbNames

def create_drop(query=""):
    conexion1=connectMySQL()
    print(query)
    cursor1=conexion1.cursor()
    try:
        cursor1.execute(query)
        cursor1.close()
        conexion1.close()
        return f"*Se ejecuto*: \"{query}\""
    except: 
        cursor1.close()
        conexion1.close()
        return "*Invalid query*"


 
"""TEST""" 
    
def run():
    pass     
   
if __name__ == "__main__":
    run()

    
