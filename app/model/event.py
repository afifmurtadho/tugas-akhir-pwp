from sqlalchemy.dialects.mysql import INTEGER
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
        INTEGER(unsigned=True),
        db.ForeignKey('users.id_user', ondelete='SET NULL'),
        nullable=True
    )
