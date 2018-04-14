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
    blog_title = db.Column(db.String(100))
    blog_text = db.Column(db.String(600))
    deleted = db.Column(db.Boolean)

    def __init__(self, blog_title, blog_text):
        self.blog_title = blog_title
        self.blog_text = blog_text
        self.deleted = False

    #def __repr__(self):
     #   return '<Blog %r>' % self.blog_title

def get_bloglist():
    return Blog.query.filter_by(deleted=False).all()

def get_deleted():
    return Blog.query.filter_by(deleted=True).all()


@app.route("/blog_text_page", methods=['POST'])
def add_blog_text():
    blog_id = request.form['blog_id']
    blog_text = request.form['blog_text']

    blog.blog_text = blog_text
    db.session.add(blog)
    db.session.commit()
    return render_template('blog-conf-page.html', blog=blog, blog_text=blog_text)

# Creates a new route called movie_ratings which handles a GET on /ratings
@app.route("/new_blog_text", methods=['GET'])
def new_blog_text():
    return render_template('blog_text.html', blogs = get_deleted())

@app.route("/add", methods=['POST'])
def add_blog():
    new_blog_title = request.form['new-blog']
    new_blog_text = request.form['blog-text']

    # if the user typed nothing at all, redirect and tell them the error
    if (not new_blog_title) or (new_blog_title.strip() == ""):
        error = "Please enter a title for your blog."
        return redirect("/?error=" + error)
    elif (not new_blog_text) or (new_blog_text.strip() == ""):
        error = "Please enter some text for your blog."
        return redirect("/?error=" + error)

    blog = Blog(new_blog_title,new_blog_text)
    db.session.add(blog)
    db.session.commit()
    return render_template('add-confirmation.html', blog=blog)

@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('edit.html', bloglist=get_bloglist(), error=encoded_error and cgi.escape(encoded_error, quote=True))

if __name__ == "__main__":
    app.run()
