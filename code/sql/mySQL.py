import mysql.connector

def dbList(console = False):
    conexion1 = mysql.connector.connect(host = "localhost", user = "root", passwd = "")
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
    conexion1=mysql.connector.connect(host="localhost", user="root", passwd="")
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

def simpleQuery(query="", doc=False, dbName="test"):
    if doc != False:
        with open("./queries.txt", "r") as qDoc:
            query = qDoc.read()
    conexion1=mysql.connector.connect(host="localhost", user="root", passwd="", database=dbName)
    print(dbName + " " + query)
    
    cursor1=conexion1.cursor()
        

      #aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa#  
    try:
        if "insert" in query.lower():
            queryInsert = query.split("values")
            valuesCount = tuple(['%s' for i in queryInsert[1]])
            valuesCount = (f"Values {valuesCount}".replace("'", ""))
            values = queryInsert[1].split()
            cursor1.execute(queryInsert[0], values)

        else: cursor1.execute(query)
        cursor1.close()
        conexion1.close()
        return f"*Se ejecuto*: \"{query}\""
    except: 
        cursor1.close()
        conexion1.close()
        return "*Invalid query*"

    
def run():
    pass     
    
if __name__ == "__main__":
    run()

    
