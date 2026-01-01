from flask import request, jsonify
from app.extensions import db
from app.model.kandang import Kandang

def get_kandang():
    data = Kandang.query.all()
    return jsonify([k.to_dict() for k in data]), 200


def create_kandang():
    data = request.json

    kandang = Kandang(
        jenis_habitat=data.get('jenis_habitat'),
        kapasitas=data.get('kapasitas'),
        suhu_ideal=data.get('suhu_ideal'),
        lokasi_zona=data.get('lokasi_zona'),
        id_user=data.get('id_user')
    )

    db.session.add(kandang)
    db.session.commit()

    return jsonify({'message': 'Kandang berhasil ditambahkan'}), 201


def update_kandang(id):
    kandang = Kandang.query.get(id)
    if not kandang:
        return jsonify({'message': 'Kandang tidak ditemukan'}), 404

    data = request.json
    kandang.jenis_habitat = data.get('jenis_habitat', kandang.jenis_habitat)
    kandang.kapasitas = data.get('kapasitas', kandang.kapasitas)
    kandang.suhu_ideal = data.get('suhu_ideal', kandang.suhu_ideal)
    kandang.lokasi_zona = data.get('lokasi_zona', kandang.lokasi_zona)

    db.session.commit()
    return jsonify({'message': 'Kandang berhasil diupdate'}), 200


def delete_kandang(id):
    kandang = Kandang.query.get(id)
    if not kandang:
        return jsonify({'message': 'Kandang tidak ditemukan'}), 404

    db.session.delete(kandang)
    db.session.commit()
    return jsonify({'message': 'Kandang berhasil dihapus'}), 200
