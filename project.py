from datetime import datetime
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "f8735c65fe944de7878ac9f454e8346b" #When we use wtf forms we need to set a secret key (random charac) to protect against modifying cookies, attacks, etc.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #path to our db file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) #db instance

#class models that are the database structure (each class its going to be its own table in the db):
#class for user profile
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) #unique id for an user
    username = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg") #default image
    password = db.Column(db.String(60), nullable=False) #not unique because users can have the same password
    posts = db.relationship("Post", backref="author", lazy=True) # lazy=True loads the data from the db when necessary

def __repr__(self): #magic method
    #return "User('{self.username}, '{self.email}', '{self.image_file}')"
    return User(self.username), User(self.email), User(self.image_file)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #coordinated universal time
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #relationship to our user model

    def __repr__(self):
        return Post({self.title}, {self.date_posted})

#Example "dummy" posts
posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

#Decorators (routes)
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts) #access our data in our template

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)