from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True     
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(600))
    deleted = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.owner = owner
        self.deleted = False

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    #def __repr__(self):
     #   return '<Blog %r>' % self.blog_title

def get_bloglist():
    return Blog.query.filter_by(deleted=False).all()

#/add is where we go after hitting Add New
#@app.route("/add", methods=['GET','POST'])
#def new_blog_text():
    #encoded_error = request.args.get("error1")
    #next_error = request.args.get("error2")
    return render_template('Add-New_Blog.html')

#/Newpost is where we go after hitting 'Add It'
@app.route("/newpost", methods=['POST','GET'])
def add_blog():
    if request.method == 'POST':
        new_blog = request.form['new_blog']
        blog_text = request.form['blog_text']
        title_error = ''
        body_error = ''    

    #if len(new_blog_text)==0 and len(new_blog_title)==0:
     #   title-error = "Please enter blog title."
      #  body-error = "Please enter blog text." 

        if not blog_text:
            body_error = "Please enter blog text."
            #blog_text = blog_text
            #new_blog = new_blog

        if not new_blog:
            title_error = "Please enter blog title."
            blog_text = blog_text
            new_blog = new_blog

        if not title_error and not body_error:
            blog = Blog(new_blog,blog_text)
            db.session.add(blog)
            db.session.commit()
            #return render_template('new-post.html', blog=blog)
            return redirect('/blog?id={}'.format(blog.id))
        else:
            #new_blog = request.form['new_blog']
            #blog_text = request.form['blog_text']
            return render_template('Add-New_Blog.html',blog_text=blog_text, new_blog=new_blog,
            body_error=body_error,title_error=title_error)
    return render_template('Add-New_Blog.html', title='New Post')

@app.route("/blog")
def viewblog():
    blog_id = request.args.get('id')
    if blog_id == None:
        blogs = Blog.query.all()
        return render_template('alt-blog.html',blogs=blogs, title='Build-A-Blog')
    else:
        blog = Blog.query.get(blog_id)
        return render_template('new-post.html',blog=blog, title='Blog Entry')
    
   # body = blog.body
    #title = blog.title
    return render_template('new-post.html', title=blog_title, body=blog.body)

@app.route("/")
def index():
    #encoded_error = request.args.get("error")
    #return render_template('blog.html', bloglist=get_bloglist(), error=encoded_error and cgi.escape(encoded_error, quote=True))
    return redirect('/blog')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        if user and user.password != password:
            flash()
            return redirect('/newpost')
    return render_template('login.html')

@app.route('/logout')

@app.before_request

@app.route('/signup', methods=['POST'])
def validate_inputs():

    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    username_error = ''
    password_error = ''
    verify_password_error = ''

    if len(username) < 3 or len(username) > 20:
        username_error = 'Username must be 3-20 characters'
        username = ''
        password = ''
        verify_password = ''
    elif ' ' in username:
        username_error = 'Username cannot contain spaces'
        username = ''
        password = ''
        verify_password = ''
    else:
        username = username

    if len(password) < 3 or len(password) > 20:
        password_error = 'Password must be 3-20 characters'
        password = ''
        verify_password = ''
    else:
        password = password

    if password != verify_password:
        verify_password_error = 'Passwords do not match!'
        verify_password = ''
        password = ''

    if not username_error and not password_error and not verify_password_error:
        return redirect("/newpost")
    else:
        return render_template('signup.html',username=username, password=password, 
        username_error=username_error, password_error=password_error, verify_password=verify_password, 
        verify_password_error=verify_password_error, email=email,
        email_error=email_error)

if __name__ == "__main__":
    app.run()
