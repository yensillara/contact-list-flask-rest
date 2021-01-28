from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    address = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(30), nullable=False)

    def serialize(self):
        return {
            "id":self.id,
            "full_name":self.full_name,
            "email":self.email,
            "address":self.address,
            "phone":self.phone,
        }