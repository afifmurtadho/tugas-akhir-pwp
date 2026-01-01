from flask import request, jsonify
from app.extensions import db
from app.model.fasilitas import Fasilitas


def get_fasilitas():
    data = Fasilitas.query.all()
    return jsonify([f.to_dict() for f in data]), 200


def create_fasilitas():
    data = request.json

    fasilitas = Fasilitas(
        nama_fasilitas=data.get('nama_fasilitas'),
        lokasi=data.get('lokasi'),
        kondisi=data.get('kondisi'),
        jadwal_perawatan=data.get('jadwal_perawatan'),
        id_user=data.get('id_user')
    )

    db.session.add(fasilitas)
    db.session.commit()
    return jsonify({'message': 'Fasilitas berhasil ditambahkan'}), 201


def update_fasilitas(id):
    fasilitas = Fasilitas.query.get(id)
    if not fasilitas:
        return jsonify({'message': 'Fasilitas tidak ditemukan'}), 404

    data = request.json
    fasilitas.nama_fasilitas = data.get('nama_fasilitas', fasilitas.nama_fasilitas)
    fasilitas.lokasi = data.get('lokasi', fasilitas.lokasi)
    fasilitas.kondisi = data.get('kondisi', fasilitas.kondisi)
    fasilitas.jadwal_perawatan = data.get(
        'jadwal_perawatan', fasilitas.jadwal_perawatan
    )

    db.session.commit()
    return jsonify({'message': 'Fasilitas berhasil diupdate'}), 200


def delete_fasilitas(id):
    fasilitas = Fasilitas.query.get(id)
    if not fasilitas:
        return jsonify({'message': 'Fasilitas tidak ditemukan'}), 404

    db.session.delete(fasilitas)
    db.session.commit()
    return jsonify({'message': 'Fasilitas berhasil dihapus'}), 200
