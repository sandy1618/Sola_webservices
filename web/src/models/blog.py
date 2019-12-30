import uuid
import datetime

from web.src.common.database import Database
from web.src.models.post import  Post


class Blog(object):
    def __init__(self, author, title, description,author_id, _id=None): # mongdb gives an id called _id
        self.author = author
        self.title = title
        self.author_id = author_id
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self,title,content,date = datetime.datetime.utcnow()):

        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date
                    )  # string format to inter format in this setting. Y for four letters.
        post.save_to_mongo()

    def get_posts(self):
        return Post.from_mongo(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        return {
            'author': self.author,
            'title': self.title,
            'author_id':self.author_id,
            'description': self.description,
            '_id': self._id
        }


    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blogs',
                                      query={"_id": id})
        return  cls(**blog_data)
        # return cls(
        #     author=blog_data['author'],
        #     title=blog_data['title'],
        #     description=blog_data['description'],
        #     _id=blog_data['_id']   )
    @classmethod
    def find_by_author_id(cls,author_id):
        blogs = Database.find(collection='blogs',query={'author_id':author_id})
        return [cls(**blog) for blog in blogs]