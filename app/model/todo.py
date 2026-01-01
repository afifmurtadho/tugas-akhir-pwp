from app.extensions import db


class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id_user"))

    user = db.relationship('User', backref='todos')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status,
            'user_id': self.user_id
        }
