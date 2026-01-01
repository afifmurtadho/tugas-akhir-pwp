from app.extensions import db

class Event(db.Model):
    __tablename__ = "event"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id_event = db.Column(db.Integer, primary_key=True)
    nama_event = db.Column(db.String(100))
    jenis_event = db.Column(db.String(100))
    tanggal_event = db.Column(db.Date)
    lokasi_event = db.Column(db.String(100))

    id_user = db.Column(
        db.Integer,
        db.ForeignKey('users.id_user', ondelete='SET NULL'),
        nullable=True
    )

    user = db.relationship('User', backref='events')

    def to_dict(self):
        return {
            'id_event': self.id_event,
            'nama_event': self.nama_event,
            'jenis_event': self.jenis_event,
            'tanggal_event': self.tanggal_event.isoformat() if self.tanggal_event else None,
            'lokasi_event': self.lokasi_event,
            'id_user': self.id_user
        }
