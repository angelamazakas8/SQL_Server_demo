import pypyodbc as odbc
import csv
import pandas as pd

DRIVER_NAME = 'SQL SERVER'
# in SQL Server, put in 'SELECT @@ServerName' as a query to find SERVER_NAME 
SERVER_NAME = ''
# put in your database's name
DATABASE_NAME = ''

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

conn = odbc.connect(connection_string)
print(conn)

cursor = conn.cursor()

query = "SELECT * FROM myhospital.hospital"
rows = cursor.execute(query)

# save "hospital" table as a .csv
with open(r'C:\Users\insertdestination.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([x[0] for x in cursor.description])  
    for row in rows:
        writer.writerow(row)

# save to pandas
df = pd.read_sql(query, conn)

# print data. This data can be used for ML algorithms
print(df)

# close the connection
cursor.close()
conn.close()

