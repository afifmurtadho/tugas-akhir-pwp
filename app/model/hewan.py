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
        db.Integer,
        db.ForeignKey('users.id_user'),
        nullable=True
    )

    kandang = db.relationship('Kandang', backref='hewans')
    user = db.relationship('User', backref='hewans')

    def to_dict(self):
        return {
            'id_hewan': self.id_hewan,
            'nama_hewan': self.nama_hewan,
            'spesies': self.spesies,
            'asal': self.asal,
            'status_konservasi': self.status_konservasi,
            'tanggal_masuk': self.tanggal_masuk.isoformat() if self.tanggal_masuk else None,
            'jenis_pakan': self.jenis_pakan,
            'id_kandang': self.id_kandang,
            'id_user': self.id_user
        }
