import uuid
import datetime

from flask import session
from web.src.models.blog import Blog
from web.src.common.database import Database


class User(object):
    def __init__(self,email,password,_id = None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod # so if this is a class method, then we dont need to make instanc of the class we can directly use this method of the class
    def get_by_email(cls,email):
        data = Database.find_one(collection='users',query={'email': email})
        if data is not None:
            return cls(**data) # user oject being called and passed on with a class .
        else:
            return None

    @classmethod  # so if this is a class method, then we dont need to make instanc of the class we can directly use this method of the class
    def get_by_id(cls,_id):
        data = Database.find_one(collection='users', query={'_id':_id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email,password):
        user = User.get_by_email(email)
        if user is not None:
            # check password
            return user.password == password
        else:
            return False

    @classmethod
    def register(cls,email, password):
        user = cls.get_by_email(email)
        if user is None:
            # then user doesnt exist  , create new
            new_user = cls(email,password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # user exists
            return False


    @staticmethod
    def login(user_email):
        # login validity has already been set
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def new_blogs(self,title,description ):
        #author, title, description,author_id, _id=None)
        blog = Blog(author=self.email,
                    title = title,
                    description = description,
                    author_id=self._id
                    )
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id,title,content,date=datetime.datetime.utcnow()):
        #title,content,date = datetime.datetime.utcnow()):
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title = title,
                      content = content,
                      date=date)

    def get_blog(self):
        return Blog.find_by_author_id(self._id)

    def json(self):
        return {
            'email' : self.email,
            '_id':self._id,
            'password':self.password
        }
    def save_to_mongo(self):
        Database.insert('users',self.json())