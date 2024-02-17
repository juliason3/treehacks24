from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
#app.config.from_pyfile('config.py') #load configuration from config.py

db = SQLAlchemy(app) #initialize Flask-SQLAlchemy
migrate = Migrate(app, db)

#defining database models
#creating a simple user model:
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)

    def __repr__(self): 
        return '<User %r>' %self.username #returning string with username

@app.route('/') 
def hello_world():    
    return 'Hello, World!'  


#adding a new user to the database (SQLAlchemy)
@app.route('/register') #route /register to add a new user to database, this connects it to flask
def register():
    new_user = User(username='john doe', email= 'john@example.com')
    db.session.add(new_user)
    db.session.commit()
    return 'User registered successfully!'
if __name__ == '__main__':     
    app.run(debug=True)