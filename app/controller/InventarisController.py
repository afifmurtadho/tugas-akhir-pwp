from flask import request, jsonify
from app.extensions import db
from app.model.inventaris import Inventaris
from datetime import date


def get_inventaris():
    data = Inventaris.query.all()
    return jsonify([i.to_dict() for i in data]), 200


def create_inventaris():
    data = request.json

    inventaris = Inventaris(
        nama_barang=data.get('nama_barang'),
        kategori=data.get('kategori'),
        jumlah=data.get('jumlah'),
        satuan=data.get('satuan'),
        kondisi=data.get('kondisi'),
        tanggal_update=date.today()
    )

    db.session.add(inventaris)
    db.session.commit()
    return jsonify({'message': 'Inventaris berhasil ditambahkan'}), 201


def update_inventaris(id):
    inv = Inventaris.query.get(id)
    if not inv:
        return jsonify({'message': 'Inventaris tidak ditemukan'}), 404

    data = request.json
    inv.nama_barang = data.get('nama_barang', inv.nama_barang)
    inv.kategori = data.get('kategori', inv.kategori)
    inv.jumlah = data.get('jumlah', inv.jumlah)
    inv.satuan = data.get('satuan', inv.satuan)
    inv.kondisi = data.get('kondisi', inv.kondisi)
    inv.tanggal_update = date.today()

    db.session.commit()
    return jsonify({'message': 'Inventaris berhasil diupdate'}), 200


def delete_inventaris(id):
    inv = Inventaris.query.get(id)
    if not inv:
        return jsonify({'message': 'Inventaris tidak ditemukan'}), 404

    db.session.delete(inv)
    db.session.commit()
    return jsonify({'message': 'Inventaris berhasil dihapus'}), 200
