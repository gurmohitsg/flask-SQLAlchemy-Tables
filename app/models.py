from app import db
import hashlib


class User(db.Model):

	__tablename__ ="users"
	id = db.Column(db.Integer, primary_key = True) # Sqlite doesn't allow BIGINT used as an primary key with autoincrement. Hence using INT
	signing_identity = db.Column(db.String(120), unique=True, nullable=False)
	signing_key = db.Column(db.String)  
	display_name = db.Column(db.String)
	reachable_at = db.relationship("UserEmails", backref='contact', lazy='dynamic')
	status = db.Column(db.Integer)
	

	def __init__(self, display_name, signing_identity ):
		self.display_name = display_name
		self.signing_identity = signing_identity
		self.signing_key = hashlib.sha224(signing_identity.encode('utf-8')).hexdigest()
		self.status = 2

class UserEmails(db.Model):

	__tablename__  = "UserEmails"
	emails = db.Column(db.String(120), primary_key=True, )
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
