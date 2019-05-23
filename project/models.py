from datetime import datetime
from project import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#class models that are the database structure (each class its going to be its own table in the db):
#class for user profile
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #unique id for an user
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') #default image
    password = db.Column(db.String(60), nullable=False) #not unique because users can have the same password
    posts = db.relationship('Post', backref='author', lazy=True) # lazy=True loads the data from the db when necessary

    def __repr__(self):
            return '<User %r>' % self.username

    #def __repr__(self): #magic method
        #return "User('{self.username}, '{self.email}', '{self.image_file}')"
    #    return User(self.username), User(self.email), User(self.image_file)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #coordinated universal time
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)#relationship to our user model

    def __repr__(self):
        return Post({self.title}, {self.date_posted})
