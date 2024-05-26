from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash,request


class User:
    db_name = 'belt_db'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password=data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def createUser(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s,%(last_name)s, %(email)s, %(password)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def getAllUsers(cls):
        query = "SELECT id, first_name, last_name, email FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        if results:
            for eachUser in results:
                users.append(eachUser)
        return users
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users where id = %(id)s;"
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users where email = %(email)s;"
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM USERS WHERE id= %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    

    @classmethod
    def update_user(cls, data):
        query = "UPDATE users set first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_user(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'userEmail')
            is_valid = False
        if len(data['first_name']) < 3:
            flash("First name should be at least 3 characters!", 'userFirst')
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name should be at least 3 characters!", 'userLast')
            is_valid = False
        if len(data['password']) < 8:
            flash("Password should be at least 8 characters!", 'userPass')
            is_valid = False
        if data['password'] != data['confirmPassword']:
            flash("Passwords should match!", 'userConfirmPass')
            is_valid = False
        return is_valid
    
