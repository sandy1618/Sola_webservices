__author__ = "sandy"

from src.models.blog import Blog
from src.database import Database







# Database.initialize()
# blog = Blog(
#     author='sandy',
#     title='sample',
#     description='sameple desc')
# blog.new_post()
# blog.save_to_mongo()
# from_database = Blog.from_mongo(blog.id)
# print(blog.get_posts())

# POST
# posts = Post(blog_id='123',
#              title='Another great post',
#              content='This is sample ocntect',
#              author='sandy'
#              )
# posts.save_to_mongo()

# received_post = Post.from_mongo('12bbc968733843d3af31b3e33cc33bb9')
# print (received_post)
