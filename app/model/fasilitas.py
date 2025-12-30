from sqlalchemy.dialects.mysql import INTEGER
from app.extensions import db


class Fasilitas(db.Model):
    __tablename__ = "fasilitas"
    __table_args__ = {"mysql_engine": "InnoDB"}


    id_fasilitas = db.Column(db.Integer, primary_key=True)
    nama_fasilitas = db.Column(db.String(100))
    lokasi = db.Column(db.String(100))
    kondisi = db.Column(db.String(50))
    jadwal_perawatan = db.Column(db.String(100))

    id_user = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey('users.id_user'),
        nullable=True
    )

