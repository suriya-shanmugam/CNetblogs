import mysql.connector
from mysql.connector import Error

from db_handler import DB


class User :
    
    def create(self,name,email,password):
        
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
        
            # Check if user already exists
            check_user_query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(check_user_query, (email,))
            result = cursor.fetchone()
        
            if result:
                print(f"User '{name}' already exists.")
                return True

            query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, password))
            connection.commit()
            print(f"User {name} added successfully!")    
            return True
        
            
        
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
    
        finally:
            
            if cursor :
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
                print("MySQL connection closed.")    

    def getUser(self,email):
        
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

            
            cursor = connection.cursor(dictionary=True)
            check_user_query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(check_user_query, (email,))
            user = cursor.fetchone()
            return user
            
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
    
        finally:
            
            if cursor :
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
                print("MySQL connection closed.")

    
    '''def getallFollowers(self):

        users = self.getallUsers()
        for entry in users:
            entry['following'] = False
        print(users)
        return users'''

    def getallUsers(self):
        
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

            
            cursor = connection.cursor(dictionary=True)
            query = "SELECT  id,name, email FROM users"
            cursor.execute(query)
            users = cursor.fetchall()
            return users
            
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
    
        finally:
            
            if cursor :
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
                print("MySQL connection closed.")

    
    def getallFollowers(self,followedEmail):

        users = self.getallUsers()
        
        print(followedEmail)
        followed_user = self.getUser(followedEmail)
        
        followed_user_id = followed_user.get('id')
        print("currentUser - ",followed_user_id)
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

            cursor = connection.cursor(dictionary=True)
            query = """
                    SELECT u.id, u.name, u.email 
                    FROM users u
                    JOIN followers f ON u.id = f.follower_id
                    WHERE f.followed_id = %s
                    """
            cursor.execute(query, (followed_user_id,))
            followers = cursor.fetchall()
            print(followers)
            
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
    
        finally:
            
            if cursor :
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
                print("MySQL connection closed.")
        
        
        
        '''for entry in users:
            entry['following'] = False
        print(users)'''
        return followers
    
    def getalluserswithFollowers(self,followedEmail):
        

        users = self.getallUsers()
        print("Users - ", users)
        
        followers = self.getallFollowers(followedEmail)
        print("Followers - ",followers)
        
        for user in users :
            user['following'] = False
            print(user.get('id'))
            for follower in followers:
                print(follower.get('id'))
                if follower.get('id') == user.get('id'):
                    print("true")
                    user['following'] = True

        print(users)
        return users

    def addFollower(self,follower_id,followedEmail):
        
        
        #print(followedEmail)
        followed_user = self.getUser(followedEmail)
        
        followed_id = followed_user.get('id')
        print(followed_id)
        
        
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
            query = "INSERT INTO followers (follower_id, followed_id) VALUES (%s, %s)"
            cursor.execute(query, (follower_id, followed_id))
            connection.commit()
            print(f"User {follower_id} is now following User {followed_id}")
            return True
            
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
    
        finally:
            
            if cursor :
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
                print("MySQL connection closed.")

    def removeFollower(self,follower_id,followedEmail):
        
        
        #print(followedEmail)
        followed_user = self.getUser(followedEmail)
        
        followed_id = followed_user.get('id')
        print(followed_id)
        
        
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
            query = "DELETE FROM followers WHERE followed_id = %s AND follower_id = %s"
            cursor.execute(query, (followed_id, follower_id))
            connection.commit()
            return cursor.rowcount > 0  # Returns True if a row was deleted, False otherwise
            
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
    
        finally:
            
            if cursor :
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
                print("MySQL connection closed.")



