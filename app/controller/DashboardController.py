from app.model.user import User
from app.extensions import db
from app.model.hewan import Hewan
from app.model.kandang import Kandang
from app.model.inventaris import Inventaris
from app.model.event import Event
from app.model.fasilitas import Fasilitas


def dashboard_data():
    total_user = User.query.count()
    total_admin = User.query.filter_by(role="admin").count()
    total_petugas = User.query.filter_by(role="petugas").count()

    total_hewan = Hewan.query.count()
    total_kandang = Kandang.query.count()
    total_inventaris = Inventaris.query.count()
    total_event = Event.query.count()
    total_fasilitas = Fasilitas.query.count()

    return {
        "total_user": total_user,
        "total_admin": total_admin,
        "total_petugas": total_petugas,
        "total_hewan": total_hewan,
        "total_kandang": total_kandang,
        "total_inventaris": total_inventaris,
        "total_event": total_event,
        "total_fasilitas": total_fasilitas
    }
