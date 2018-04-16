from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True     
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(600))
    deleted = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.deleted = False

    #def __repr__(self):
     #   return '<Blog %r>' % self.blog_title

def get_bloglist():
    return Blog.query.filter_by(deleted=False).all()

#/add is where we go after hitting Add New
@app.route("/add", methods=['GET'])
def new_blog_text():
    #encoded_error = request.args.get("error1")
    #next_error = request.args.get("error2")
    return render_template('Add-New_Blog.html')

#/Newpost is where we go after hitting 'Add It'
@app.route("/newpost", methods=['POST','GET'])
def add_blog():
   # if request.method == 'POST':
    new_blog = request.form['new_blog']
    blog_text = request.form['blog_text']
    title_error = ''
    body_error = ''    

    #if len(new_blog_text)==0 and len(new_blog_title)==0:
     #   title-error = "Please enter blog title."
      #  body-error = "Please enter blog text." 

    if not blog_text:
        body_error = "Please enter blog text."
        blog_text = blog_text
        new_blog = new_blog

    if not new_blog:
        title_error = "Please enter blog title."
        blog_text = blog_text
        new_blog = new_blog

    if not title_error and not body_error:
        blog = Blog(new_blog,blog_text)
        db.session.add(blog)
        db.session.commit()
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

if __name__ == "__main__":
    app.run()
