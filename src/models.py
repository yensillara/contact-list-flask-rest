from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#class User(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    #password = db.Column(db.String(80), unique=False, nullable=False)
    #is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    #def __repr__(self):
        #return '<User %r>' % self.username

    #def serialize(self):
        #return {
            #"id": self.id,
            #"email": self.email,
            # do not serialize the password, its a security breach
        #}

class Human(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
        }

class Contact(db.Model):
    id = db.Column(db.Integer)
    full_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), primary_key=True, nullable=False)
    adress = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(30), nullable=False)

    def serialize(self):
        return {
            "id":self.id,
            "full_name":self.full_name,
            "email":self.email,
            "adress":self.adress,
            "phone":self.phone,
        }