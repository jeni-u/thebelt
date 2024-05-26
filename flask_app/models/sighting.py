from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash,request
from flask_app.models.user import User

class Sighting:
    db="belt_db"
    def __init__(self,data):
        self.id=data['id']
        self.location = data['location']
        self.what_happened=data['what_happened']
        self.date_of_sighting=data['date_of_sighting']
        self.nr_of_sas=data['nr_of_sas']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def createSighting(cls, data):
        query = '''
            INSERT INTO sightings (location, what_happened, date_of_sighting, nr_of_sas, user_id)
            VALUES (%(location)s, %(what_happened)s, %(date_of_sighting)s, %(nr_of_sas)s, %(user_id)s)
            '''
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            user_query = "SELECT * FROM users WHERE id = %(user_id)s"
            user_data = {'user_id': data['user_id']}
            user = connectToMySQL(cls.db).query_db(user_query, user_data)
        if user:
            return result, user[0]
        return None, None
    
    @classmethod
    def getAllSightings(cls):
        query = "SELECT * FROM sightings;"
        results = connectToMySQL(cls.db).query_db(query)
        sightings = []
        if results:
            for sight in results:
                sightings.append(sight)
        return sightings
    
    @classmethod
    def get_sighting_by_id(cls, sighting_id):
        query = "SELECT * FROM sightings WHERE id = %(sighting_id)s;"
        data = {'sighting_id': sighting_id}
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return result[0]
        return None
    
    @classmethod
    def delete_sighting(cls, data):
        query = "DELETE FROM sightings WHERE id= %(sighting_id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    

    @classmethod
    def update_sighting(cls, data):
        query = "UPDATE sightings set location = %(location)s, what_happened = %(what_happened)s, date_of_sighting=%(date_of_sighting)s ,nr_of_sas = %(nr_of_sas)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_user_id_by_sighting_id(cls, sighting_id):
        query = "SELECT user_id FROM sightings WHERE id = %(sighting_id)s;"
        data = {'sighting_id': sighting_id}
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return result[0]['user_id']
        return None
    
    @classmethod
    def get_user_first_name_by_id(cls, user_id):
        query = "SELECT first_name FROM users WHERE id = %(user_id)s;"
        data = {'user_id': user_id}
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return result[0]['first_name']
        return None
    

    @staticmethod
    def validate_sighting(data):
        is_valid = True
        if len(data['location']) < 3:
            flash("Location should be at least 3 characters!", 'location')
            is_valid = False
        if len(data['what_happened']) < 3:
            flash("Description of what happened cannot be empty!", 'what_happened')
            is_valid = False
        if not data['date_of_sighting']:
            flash("You need to give a date!", 'date_of_sighting')
            is_valid = False
        nr_of_sas = data.get('nr_of_sas')
        if not nr_of_sas or not str(nr_of_sas).isdigit() or int(nr_of_sas) <= 0:
            flash("Give a valid number of sasquatches!", 'nr_of_sas')
            is_valid = False

        return is_valid
    
    @classmethod
    def is_skeptic(cls, data):
        query = 'SELECT * FROM scepticks WHERE user_id = %(user_id)s AND sighting_id = %(sighting_id)s;'
        result = connectToMySQL(cls.db).query_db(query, data)
        return len(result) > 0

    @classmethod
    def skeptic(cls, data):
        query = 'INSERT INTO scepticks (user_id, sighting_id) VALUES (%(user_id)s, %(sighting_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def remove_skeptic(cls, data):
        query = 'DELETE FROM scepticks WHERE sighting_id = %(sighting_id)s AND user_id = %(user_id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    
    

    
    @classmethod
    def get_skeptics_info(cls, sighting_id):
        query = """
            SELECT users.first_name, users.last_name
            FROM scepticks 
            LEFT JOIN users ON scepticks.user_id = users.id 
            WHERE scepticks.sighting_id = %(sighting_id)s;
        """
        data = {'sighting_id': sighting_id}
        results = connectToMySQL(cls.db).query_db(query, data)
        return results 
    

    @classmethod
    def get_skeptic_count(cls, sighting_id):
        query = "SELECT COUNT(*) as skeptic_count FROM scepticks WHERE sighting_id = %(sighting_id)s;"
        data = {'sighting_id': sighting_id}
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return result[0]['skeptic_count']
        return 0

    @classmethod
    def remove_all_skeptics(cls, sighting_id):
        query = "DELETE FROM scepticks WHERE sighting_id = %(sighting_id)s;"
        data = {'sighting_id': sighting_id}
        return connectToMySQL(cls.db).query_db(query, data)



