from app.extensions import db
from sqlalchemy.dialects import mysql
from sqlalchemy.dialects.mysql import INTEGER

class User(db.Model):
    __tablename__ = 'users'
    id_user = db.Column(INTEGER(unsigned=True), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    nama_lengkap = db.Column(db.String(100), nullable=False)
