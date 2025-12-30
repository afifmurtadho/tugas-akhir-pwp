from app.model.user import User
from app.extensions import db


def dashboard_data():
    total_user = User.query.count()
    total_admin = User.query.filter_by(role="admin").count()
    total_petugas = User.query.filter_by(role="petugas").count()

    return {
        "total_user": total_user,
        "total_admin": total_admin,
        "total_petugas": total_petugas
    }
