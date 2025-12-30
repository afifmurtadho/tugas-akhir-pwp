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
        db.Integer,
        db.ForeignKey('users.id_user'),
        nullable=True
    )

    user = db.relationship('User', backref='kandangs')

    def to_dict(self):
        return {
            'id_kandang': self.id_kandang,
            'jenis_habitat': self.jenis_habitat,
            'kapasitas': self.kapasitas,
            'suhu_ideal': self.suhu_ideal,
            'lokasi_zona': self.lokasi_zona,
            'id_user': self.id_user
        }

