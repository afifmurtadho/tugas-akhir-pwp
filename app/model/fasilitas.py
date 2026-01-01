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
        db.Integer,
        db.ForeignKey('users.id_user'),
        nullable=True
    )

    user = db.relationship('User', backref='fasilitass')

    def to_dict(self):
        return {
            'id_fasilitas': self.id_fasilitas,
            'nama_fasilitas': self.nama_fasilitas,
            'lokasi': self.lokasi,
            'kondisi': self.kondisi,
            'jadwal_perawatan': self.jadwal_perawatan,
            'id_user': self.id_user
        }

