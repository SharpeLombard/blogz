from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
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

#def get_deleted():
    #return Blog.query.filter_by(deleted=True).all()


@app.route("/newposst", methods=['POST'])
def add_blog_text():
    
    #blog-text = request.form['blog-text']
    #new-blog = request.form['new-blog']

    blog.title = new-blog
    blog.body = blog-text
    db.session.add(blog)
    db.session.commit()
    return render_template('new-post.html', blog=blog, blog_text=blog_text)

#/add is where we go after hitting Add New
@app.route("/add", methods=['GET'])
def new_blog_text():
    encoded_error = request.args.get("error1")
    next_error = request.args.get("error2")
    return render_template('Add-New_Blog.html', error1=encoded_error and cgi.escape(encoded_error, quote=True),
    error2=next_error and cgi.escape(next_error, quote=True))

#/Newpost is where we go after hitting 'Add It'
@app.route("/newpost", methods=['POST'])
def add_blog():
    new_blog_title = request.form['new-blog']
    new_blog_text = request.form['blog-text']

    # if the user typed nothing at all, redirect and tell them the error
    
    if ((not new_blog_title) or (new_blog_title.strip() == "")) and ((not new_blog_text) or (new_blog_text.strip() == "")):
        error1 = "Please enter blog title."
        error2 = "Please enter blog text."
        return redirect("/add?error1=" + error1,error2)
    
    if (not new_blog_title) or (new_blog_title.strip() == ""):
        error1 = "Please enter blog title."
        return redirect("/add?error1=" + error1)

        #return redirect("/?error=" + error)
    if (not new_blog_text) or (new_blog_text.strip() == ""):
        error2 = "Please enter blog text."
        return redirect("/add?error2=" + error2)

   

    blog = Blog(new_blog_title,new_blog_text)
    db.session.add(blog)
    db.session.commit()
    return render_template('new-post.html', blog=blog)

@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('blog.html', bloglist=get_bloglist(), error=encoded_error and cgi.escape(encoded_error, quote=True))

if __name__ == "__main__":
    app.run()
