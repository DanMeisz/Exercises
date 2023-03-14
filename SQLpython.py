import pyodbc

class SQL():
#initalize SQL class
    def __init__(self,driver,server,database,uid,pwd):
        self.driver=driver
        self.server=server
        self.database=database
        self.uid=uid
        self.pwd=pwd
        self.connection= None
        self.cursor= None
#connect to database and initalize cursor
    def connect(self):
        connection_string = (f"Driver={self.driver};"
            f"Server={self.server};"
            f"Database={self.database};"
            f"UID={self.uid};"
            f"PWD={self.pwd};")
        self.connection=pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()
#print if connection was successful
        print("Connected to SQL Server")
        
#if cursor or connection is active, close them
    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Disconnected from SQL Server")
#return the value of a query passed as an argument
    def run_query(self,query):
        self.cursor.execute(query)
        result=self.cursor.fetchall()
        return result
#commit the query passed as an argument
    def commit_change(self,query):
        self.cursor.execute(query)
        self.connection.commit()
#adds the duplicate column and sets it to 1 if language is duplicated(multiple occurences) and 0 if it's distinct     
    def update_rows(self):
        self.cursor.execute("ALTER TABLE languages ADD duplicate bit;")
        self.cursor.execute("SET duplicate = CASE WHEN (SELECT COUNT(*) FROM Languages L WHERE L.Language = Languages.Language) > 1 THEN 1 ELSE 0 END;")
        self.connection.commit()



#initalize connection
connection = SQL(driver="",server= " ",database ="",uid = "",pwd = "")
connection.connect()

try:
#print countries and languages line by line in the required format 
    query1 =connection.run_query("SELECT * FROM languages")
    for row in query1:
        print(f"Country: {row.Country} - Language {row.Language}")
#insert a new country and commit
    query2 =connection.commit_change("INSERT INTO languages (Country,Language) VALUES('Mongolia','Mongolian')")
    connection.update_rows()
    
#terminate the connection even if exception occurs during the runtime    
finally:
    connection.disconnect()