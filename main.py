from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'poop?'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return str(self.username)


@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'signup', 'individual', 
        'index', 'home', 'OneBlog', 'user_page', 'UserPosts']
    if 'user' not in session and request.endpoint not in allowed_routes:
            return redirect('/login')


@app.route("/")
def index():
    return redirect("/UserPage")


@app.route("/blog")
def home():
    blogs = Blog.query.all()
    welcome = "Not logged in"
    if 'user' in session:
        welcome = "Logged in as: " + session['user']

    return render_template('home.html', title='BLOGZ!', 
        blogs= blogs, welcome= welcome)


@app.route("/newpost", methods= ['POST', 'GET'])
def AddBlog():
    error = {"title_blank": "", "body_blank": ""}
    new_body = ""
    new_title = ""

    welcome = "Logged in as: " + session['user']
    existing_user = User.query.filter_by(username=session['user']).first()

    if request.method == 'POST':
        new_title = request.form["title"]
        new_body = request.form["body"]

        if new_title == "":
            error["title_blank"] = "Enter a title for your blog"
        if new_body == "":
            error["body_blank"] = "Enter some text for your blog's body"

        if error["title_blank"] == "" and error["body_blank"] == "":
            new_blog = Blog(new_title, new_body, existing_user)
            db.session.add(new_blog)
            db.session.commit()
            author = User.query.filter_by(id= new_blog.owner_id).first()
            return redirect("/individual?blog_title="+new_title)

    return render_template('add.html', title= "Add a blog post", 
        add_body= new_body, add_title= new_title,
        title_blank= error["title_blank"], body_blank= error["body_blank"],
        welcome= welcome)


@app.route("/individual")
def OneBlog():
    welcome = "Not logged in"
    if 'user' in session:
        welcome = "Logged in as: " + session['user']

    title = request.args.get('blog_title')
    if title:
        existing_blog = Blog.query.filter_by(title= title).first()
        author = User.query.filter_by(id= existing_blog.owner_id).first()
        return render_template("individual.html", 
            title= existing_blog.title, body= existing_blog.body,
            author= author.username, welcome= welcome)


@app.route("/UserPage")
def UserPosts():
    welcome = "Not logged in"
    if 'user' in session:
        welcome = "Logged in as: " + session['user']

    user = request.args.get('user_link')
    if user:
        existing_user = User.query.filter_by(username= user).first()
        user_posts = existing_user.blogs
        return render_template("singleUser.html", welcome= welcome,
            title= user+"'s posts", blogs= user_posts)

    user_list = User.query.all()
    return render_template("AllUsers.html", title= "All Users",
        welcome= welcome, user_list= user_list)


@app.route("/signup", methods=['POST', 'GET'])
#def display_form():
 #   return render_template('signup.html', username='', username_error='', password='', password_error='',
  #  verify_password='', verify_password_error='')
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        existing_user = User.query.filter_by(username=username).first()
        #email = request.form['email']
        username_error = ''
        password_error = ''
        verify_password_error = ''
        #email_error = ''

        if len(username) < 3: #or len(username) > 20:
            username_error = 'Username must be more than 2 characters'
            username = ''
            password = ''
            verify_password = ''
        #elif ' ' in username:
        #   username_error = 'Username cannot contain spaces'
        #  username = ''
        # password = ''
        # verify_password = ''
        else:
            username = username

        if len(password) < 3:# or len(password) > 20:
            password_error = 'Password must be more than 2 characters'
            password = ''
            verify_password = ''
        else:
            password = password

        if password != verify_password:
            verify_password_error = 'Passwords do not match!'
            verify_password = ''
            password = ''

        if existing_user:
            username_error = "Username already exists!"
            
        if not username_error and not password_error and not verify_password_error and not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = new_user.username
            return redirect("/newpost")
        else:
            return render_template('SugnUp.html',username=username, password=password, username_error=username_error, 
            password_error=password_error, verify_password=verify_password, verify_password_error=verify_password_error)
    return render_template("SugnUp.html", title= "Signup To Be A Blogger")
        

@app.route("/login", methods=['POST', 'GET'])
def login():
    error = {"name_error": "", "pass_error": ""}
    username = ""
    #if 'user' in session:
        #del session['user']
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            if password == "":
                error["pass_error"] = "Password cannot be blank."

            elif existing_user.password == password:
                session['user'] = existing_user.username
                return redirect("/newpost")
            else:
                error["pass_error"] = "Invalid password"
        else:
            error["name_error"] = "Invalid username. Try again or create an account."

    return render_template("login.html", title= "Login",
        name_error= error["name_error"], pass_error= error["pass_error"],
        username= username)


@app.route("/logout", methods= ['POST', 'GET'])
def logout():
    if 'user' in session:
        del session['user']
    return redirect('/blog')



if __name__ == '__main__':
    app.run()