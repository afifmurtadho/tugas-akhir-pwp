from sqlalchemy.dialects.mysql import INTEGER
from app.extensions import db

class Hewan(db.Model):
    __tablename__ = "hewan"
    __table_args__ = {"mysql_engine": "InnoDB"}


    id_hewan = db.Column(db.Integer, primary_key=True)
    nama_hewan = db.Column(db.String(100), nullable=False)
    spesies = db.Column(db.String(100))
    asal = db.Column(db.String(100))
    status_konservasi = db.Column(db.String(50))
    tanggal_masuk = db.Column(db.Date)
    jenis_pakan = db.Column(db.String(100))

    id_kandang = db.Column(
        db.Integer,
        db.ForeignKey("kandang.id_kandang")
    )

    id_user = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey('users.id_user'),
        nullable=True
    )
