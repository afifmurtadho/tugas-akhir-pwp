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
