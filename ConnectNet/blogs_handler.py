from flask import jsonify

import mysql.connector
from mysql.connector import Error

from db_handler import DB

from users_handler import User

def createBlog(userEmail,subject,desc):
        
        user = User()
        current_user = user.getUser(userEmail)
        user_id = current_user.get('id')
        print(user_id)
        connection = None
        cursor = None
        try:
            
            db = DB()
            
            print(db.gethost())
            
            connection = mysql.connector.connect(
            host= db.gethost(),
            user= db.getUser(),
            password= db.getPassword(),
            database= db.getDatabase()
            )

            
            cursor = connection.cursor()
            
            cursor.execute("INSERT INTO blogs (user_id, subject, description) VALUES (%s, %s, %s)",(user_id, subject, desc,))
            connection.commit()
            return jsonify({"message": "Blog created successfully!"}), 201
        
            
        
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
    
        finally:
            
            if cursor :
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
                print("MySQL connection closed.")

def fetchAllBlogs(userEmail):
        
        user = User()
        current_user = user.getUser(userEmail)
        user_id = current_user.get('id')
        print(user_id)
        connection = None
        cursor = None
        try:
            
            db = DB()
            
            print(db.gethost())
            
            connection = mysql.connector.connect(
            host= db.gethost(),
            user= db.getUser(),
            password= db.getPassword(),
            database= db.getDatabase()
            )

            cursor = connection.cursor(dictionary=True)  # Ensure this option is set
            cursor.execute("""
            SELECT 
                blogs.*, 
                users.name, 
                users.email 
            FROM 
                blogs 
            JOIN 
                users ON blogs.user_id = users.id 
            ORDER BY 
                blogs.time DESC
            """)
            blogs = cursor.fetchall()
            return blogs
        
            
        
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
    
        finally:
            
            if cursor :
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
                print("MySQL connection closed.")                