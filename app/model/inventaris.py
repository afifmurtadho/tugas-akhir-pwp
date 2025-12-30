from app.extensions import db
from datetime import date

class Inventaris(db.Model):
    __tablename__ = "inventaris"
    __table_args__ = {"mysql_engine": "InnoDB"}


    id_inventaris = db.Column(db.Integer, primary_key=True)
    nama_barang = db.Column(db.String(100))
    kategori = db.Column(db.String(100))
    jumlah = db.Column(db.Integer)
    satuan = db.Column(db.String(50))
    kondisi = db.Column(db.String(50))
    tanggal_update = db.Column(db.Date, default=date.today)

    def to_dict(self):
        return {
            'id_inventaris': self.id_inventaris,
            'nama_barang': self.nama_barang,
            'kategori': self.kategori,
            'jumlah': self.jumlah,
            'satuan': self.satuan,
            'kondisi': self.kondisi,
            'tanggal_update': self.tanggal_update.isoformat() if self.tanggal_update else None
        }
