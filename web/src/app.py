from flask import Flask, render_template, request, session, make_response

from web.src.common.database import Database
from web.src.models.blog import Blog
from web.src.models.post import Post
from web.src.models.user import User

app = Flask(__name__)  # this app starts with name = main , creating app obj

# setting a secure secret key for cookie
app.secret_key = "sandy"


# define the routing
@app.route('/')  # this / is the end point
def home():
    return 'home'

# define the routing
@app.route('/login')  # this / is the end point
def login():
    return render_template('login.html')

# define the routing
@app.route('/register')  # this / is the end point
def register():
    return render_template('register.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


# define a new endpoint
@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    if User.login_valid(email, password):
        User.login(email) # sessions are already added when you are loggin in

    return render_template('profile.html', email=session['email'])  # passing this template the email variable

@app.route('/auth/register', methods = ['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    User.register(email,password) # session are already added for users

    return render_template('profile.html', email = session['email'])

@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id = None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])
    blogs = user.get_blog()
    return render_template('user_blogs.html', blogs=blogs, email=user.email)

#something regarding posts
@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()
    return render_template('posts.html', posts=posts, blog_title = blog.title, blog_id=blog._id)

#trying to post new blog post !
@app.route('/blogs/new', methods = ['POST','GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])

        new_blog = Blog(user.email,title,description,user._id)
        new_blog.save_to_mongo()

        return make_response(user_blogs(user._id))

@app.route('/posts/new/<string:blog_id>', methods = ['POST','GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id,title,content,user.email)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))

# running main
if __name__ == '__main__':
    app.run(port=1234, debug=True)
