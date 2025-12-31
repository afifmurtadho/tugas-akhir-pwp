from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    nama_lengkap = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id_user': self.id_user,
            'username': self.username,
            'role': self.role,
            'nama_lengkap': self.nama_lengkap
        }
