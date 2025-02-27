import pyodbc

#Have to establish connection with db via connection string
db = f'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:account-ant.database.windows.net,1433;Database=account-ant-employee;Uid=workerAnt;Pwd=forTheColony01!!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
connect = pyodbc.connect(db)

#View all users
def view_users():
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Users")
    for row in cursor.fetchall(): 
        print(row)
    cursor.close()
    connect.close()
    
#Create new user/assign their role
def create_user(user_id, first_name, last_name, birth_date, email, hire_date, role, status):
    cursor = connect.cursor()
    query = "INSERT INTO Users (user_id, first_name, last_name, birth_date, email, hire_date, role, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (user_id, first_name, last_name, birth_date, email, hire_date, role, status))
    connect.commit()
    cursor.close()
    connect.close()

#Delete user 
def delete_user(user_id):
    cursor = connect.cursor()
    query = "DELETE FROM Users WHERE user_id = %s "
    cursor.execute(query, (user_id))
    connect.commit()
    cursor.close()
    connect.close()

#Change status or activate/deactivate
def change_status(status, user_id):
    cursor = connect.cursor()
    query = "UPDATE Users SET status = %s WHERE user_id = %s"
    cursor.execute(query, (status, user_id))
    connect.commit()
    cursor.close()
    connect.close()

#View past passwords
def view_expired_passwords():
    cursor = connect.cursor()
    cursor.execute("SELECT past_password FROM Passwords")
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    connect.close()

