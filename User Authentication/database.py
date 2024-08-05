import sqlite3
conn = sqlite3.connect("Users.db",check_same_thread=False)

c = conn.cursor()
class UserClass:
  def __init__(self):
      pass
  def create_table(self):
      with conn:
        c.execute('''CREATE TABLE IF NOT EXISTS users(
        First_Name TEXT, 
        Last_Name TEXT,
        Phone_Number INTEGER ,
        Email VARCHAR(200) PRIMARY KEY, 
        Password TEXT,
        User_Type TEXT)''')
    
  def insert_user(self,first_name,last_name,phone_number,email,password,user_type):
      with conn:
        c.execute("INSERT INTO users(First_Name, Last_Name,Phone_Number, Email, Password,User_Type) VALUES(?,?,?,?,?,?)",
                  (first_name,last_name,phone_number,email,password,user_type))
  
  def delete_User(self,email):
      with conn:
        c.execute(f"DELETE FROM users WHERE Email = '{email}'")
  
  def existing_User(self,email):
      c.execute(f"SELECT * FROM users WHERE Email = '{email}'")
      if c.fetchone() is None:
        return False
      else:
        return True

  def get_user(self,email):
    c.execute(f"SELECT Password FROM users WHERE Email = '{email}'")
    result = c.fetchone()
    if result:
        return result[0]
    else:
        return None

  def get_user_details(self,email):
        c.execute(f"SELECT * FROM users WHERE Email = '{email}'")
        result = c.fetchone()
        return result

  def get_user_type(self,email):
      c.execute(f"SELECT User_Type FROM users WHERE Email = '{email}'")
      return c.fetchone()[0]
  def all_user(self):  
    c.execute("SELECT Email,First_Name FROM users WHERE User_Type = 'User'")
    result = c.fetchall()
    leng = len(result)  
    return [result,leng]  

c.execute("SELECT * FROM users") 
print(c.fetchall())