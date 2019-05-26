from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from project import db, login_manager, app
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

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod #with this method we tell python to not expect the self as an arguments, but only token
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

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
