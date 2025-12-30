from sqlalchemy.dialects.mysql import INTEGER
from app.extensions import db

class Kandang(db.Model):
    __tablename__ = "kandang"
    __table_args__ = {"mysql_engine": "InnoDB"}


    id_kandang = db.Column(db.Integer, primary_key=True)
    jenis_habitat = db.Column(db.String(100))
    kapasitas = db.Column(db.Integer)
    suhu_ideal = db.Column(db.String(20))
    lokasi_zona = db.Column(db.String(100))

    id_user = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey('users.id_user'),
        nullable=True
    )

