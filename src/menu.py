from src.database import Database
from src.models.blog import Blog
class menu(object):
    def __init__(self):

        self.user = input("Enter you author name:")#ask user for author name
        self.user_blog = None
        if self._user_has_account():
            print("Welcome back {}:".format(self.user))# #check if they have got an account
        else :# inf not prompt for a new one
            self._prompt_user_for_account()
    def _user_has_account(self):
        blog = Database.find_one('blogs',{'author':self.user})
        if blog is not None:
            self.user_blog = Blog.from_mongo(blog['id'])
            return True
        else :
            return False
    def _prompt_user_for_account(self):
        title = input('Enter blog title:')
        description = input('Enter blog description')
        blog = Blog(author = self.user,
                    title = title,
                    description = description
                    )
        blog.save_to_mongo()
        self.user_blog = blog
    def run_menu(self):
        #user read or write blogs? ask
        read_or_write = input('Do you want to read (R) or Write (W)')
        if read_or_write == 'R': # list blogs, allow to pick one, display posts
            self._list_blogs()
            self._view_blog()
        elif read_or_write == 'W': # prompt to write a post
            self.user_blog.new_post()
        else:
            print('Thank you for blogging')


    def _list_blogs(self):
        blogs = Database.find(collection='blogs',
                              query={})
        for blog in blogs:
            print(
                "ID:{}, Title: {}, Author:{}".format(blog['id'],blog['title'],blog['author'])
                            )

    def _view_blog(self):
        blog_to_see = input("Enter ID of blog")
        blog = Blog.from_mongo(blog_to_see)
        posts = blog.get_posts()
        for post in posts:
            print("Date:{}, title:{}\n\n{}".format(post['created_date'],post['title'],post['content']))
