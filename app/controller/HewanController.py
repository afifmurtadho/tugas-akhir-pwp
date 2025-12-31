from flask import request, jsonify
from app.extensions import db
from app.model.hewan import Hewan
from datetime import datetime

# =========================
# GET ALL HEWAN
# =========================
def get_hewan():
    data = Hewan.query.all()
    return jsonify([h.to_dict() for h in data]), 200


# =========================
# GET HEWAN BY ID
# =========================
def get_hewan_by_id(id):
    hewan = Hewan.query.get(id)
    if not hewan:
        return jsonify({'message': 'Hewan tidak ditemukan'}), 404
    return jsonify(hewan.to_dict()), 200


# =========================
# CREATE HEWAN
# =========================
def create_hewan():
    data = request.json

    hewan = Hewan(
        nama_hewan=data.get('nama_hewan'),
        spesies=data.get('spesies'),
        asal=data.get('asal'),
        status_konservasi=data.get('status_konservasi'),
        tanggal_masuk=datetime.strptime(
            data.get('tanggal_masuk'), '%Y-%m-%d'
        ) if data.get('tanggal_masuk') else None,
        jenis_pakan=data.get('jenis_pakan'),
        id_kandang=data.get('id_kandang'),
        id_user=data.get('id_user')
    )

    db.session.add(hewan)
    db.session.commit()

    return jsonify({'message': 'Hewan berhasil ditambahkan'}), 201


# =========================
# UPDATE HEWAN
# =========================
def update_hewan(id):
    hewan = Hewan.query.get(id)
    if not hewan:
        return jsonify({'message': 'Hewan tidak ditemukan'}), 404

    data = request.json

    hewan.nama_hewan = data.get('nama_hewan', hewan.nama_hewan)
    hewan.spesies = data.get('spesies', hewan.spesies)
    hewan.asal = data.get('asal', hewan.asal)
    hewan.status_konservasi = data.get('status_konservasi', hewan.status_konservasi)
    hewan.jenis_pakan = data.get('jenis_pakan', hewan.jenis_pakan)
    hewan.id_kandang = data.get('id_kandang', hewan.id_kandang)

    db.session.commit()
    return jsonify({'message': 'Hewan berhasil diupdate'}), 200


# =========================
# DELETE HEWAN
# =========================
def delete_hewan(id):
    hewan = Hewan.query.get(id)
    if not hewan:
        return jsonify({'message': 'Hewan tidak ditemukan'}), 404

    db.session.delete(hewan)
    db.session.commit()
    return jsonify({'message': 'Hewan berhasil dihapus'}), 200
