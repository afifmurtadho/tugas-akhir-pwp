from flask import request, jsonify
from app.extensions import db
from app.model.event import Event
from datetime import datetime


def get_events():
    data = Event.query.all()
    return jsonify([e.to_dict() for e in data]), 200


def create_event():
    data = request.json

    event = Event(
        nama_event=data.get('nama_event'),
        jenis_event=data.get('jenis_event'),
        tanggal_event=datetime.strptime(
            data.get('tanggal_event'), '%Y-%m-%d'
        ) if data.get('tanggal_event') else None,
        lokasi_event=data.get('lokasi_event'),
        id_user=data.get('id_user')
    )

    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event berhasil ditambahkan'}), 201


def update_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({'message': 'Event tidak ditemukan'}), 404

    data = request.json
    event.nama_event = data.get('nama_event', event.nama_event)
    event.jenis_event = data.get('jenis_event', event.jenis_event)
    event.lokasi_event = data.get('lokasi_event', event.lokasi_event)

    if data.get('tanggal_event'):
        event.tanggal_event = datetime.strptime(
            data.get('tanggal_event'), '%Y-%m-%d'
        )

    db.session.commit()
    return jsonify({'message': 'Event berhasil diupdate'}), 200


def delete_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({'message': 'Event tidak ditemukan'}), 404

    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event berhasil dihapus'}), 200
