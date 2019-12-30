import uuid
from web.src.common.database import Database
import datetime


class Post(object):
    def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), _id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            '_id': self._id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'created_date': self.created_date
        }

    def save_to_mongo(self):
        Database.insert(collection='posts',
                        data=self.json())

    # need to get data from mongodb
    @classmethod
    def from_mongo (cls, id):
        post_data = Database.find(collection ='posts',
                                      query={'blog_id': id})
        # return post_data
        return [cls(**post) for post in post_data]
        # for each element in the data, save the name of the element to the object's element
        # return cls(blog_id=post_data['blog_id'],
        #            title=post_data['title'],
        #            content=post_data['content'],
        #            author=post_data['author'],
        #            created_date=post_data['created_date'],
        #            _id=post_data['_id']
        #            )

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection='posts', query={'blog_id': id})]
