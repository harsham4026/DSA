import pyodbc

QUERY_SEPARATOR = ";"
connection = pyodbc.connect(
    "DRIVER={SQL Server Native Client 11.0};SERVER=server_name;DATABASE=db_name;Trusted_Connection=yes;UID=User;PWD=password")

cursor = connection.cursor()
with open('/path/to/sqlQueryFile', 'r') as sql_query_file:
    data = sql_query_file.read().split(QUERY_SEPARATOR)

for query in data:
    cursor.execute(query.strip())

    # for inserting the query type to another table in db
    # if you are planning to write to a table under the same schema use the same connection object else create another
    # connection object with different name with the schema you wanted to write. Here I am assuming that we will
    # write into the table under same schema
    if query.startswith("SELECT") or query.startswith("select"):
        cursor.execute("INSERT INTO TABLE (col1) values ('select')")
    elif query.startswith("UPDATE") or query.startswith("update"):
        cursor.execute("INSERT INTO TABLE (col1) values ('update')")
    elif query.startswith("DELETE") or query.startswith("delete"):
        cursor.execute("INSERT INTO TABLE (col1) values ('delete')")
    elif query.startswith("ALTER") or query.startswith("alter"):
        cursor.execute("INSERT INTO TABLE (col1) values ('alter')")

connection.close()
