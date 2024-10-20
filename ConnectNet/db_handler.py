from flask import current_app
import mysql.connector
from mysql.connector import Error

class DB :
   
    def __init__(self):
        self._host = current_app.config['MYSQL_HOST']
        self._user= current_app.config['MYSQL_USER']
        self._password= current_app.config['MYSQL_PASSWORD']
        self._database= current_app.config['MYSQL_DB']

    def gethost(self) :
        return self._host
    def getUser(self) :
        return self._user
    def getPassword(self) :
        return self._password
    def getDatabase(self) :
        return self._database
    
    def initialsetup(self) :
        
        cursor = None
        connection = None
        try:
        # Replace with your actual database connection details
            connection = mysql.connector.connect(
            host= self._host,
            user=self._user,
            password=self._password,
            database=self._database
            )
        
            cursor = connection.cursor()
        
            #SQL query to create the Users table if it doesn't exist
            create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """

            cursor.execute(create_users_table)

            # Create blogs table
            create_blogs_table = """
                CREATE TABLE IF NOT EXISTS blogs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                subject VARCHAR(255) NOT NULL,
                description TEXT,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
            cursor.execute(create_blogs_table)
            print("Blogs table created successfully")

            create_followers_table = """
            CREATE TABLE IF NOT EXISTS followers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            follower_id INT NOT NULL,
            followed_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (follower_id) REFERENCES users(id),
            FOREIGN KEY (followed_id) REFERENCES users(id),
            UNIQUE KEY unique_follow (follower_id, followed_id)
            )
            """
            cursor.execute(create_followers_table)
            print("Followers table created successfully")

            # Commit the changes
            connection.commit()
            print("Users table created successfully (or already exists).")
            return True
        
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
        finally:
            
            if cursor:
                cursor.close()
            
            if connection and connection.is_connected():
                connection.close()
            print("MySQL connection closed.")
   
      