from flask import Blueprint
from app.controller.UserController import (get_users, create_user, update_user, delete_user)
from app.middleware.auth import (login_required, admin_required)
from app.controller.AuthController import (login_api, register_api, logout_api)
#---
from app.controller.HewanController import (get_hewan, create_hewan, update_hewan, delete_hewan)
from app.controller.KandangController import (get_kandang, create_kandang, update_kandang, delete_kandang)
from app.controller.EventController import (get_events, create_event, update_event, delete_event)
from app.controller.InventarisController import (get_inventaris, create_inventaris, update_inventaris, delete_inventaris)
from app.controller.FasilitasController import (get_fasilitas, create_fasilitas, update_fasilitas, delete_fasilitas)

api = Blueprint('api', __name__, url_prefix='/api')


# ---------- LOGIN ----------
@api.route('/login', methods=['POST'])
def api_login():
    return login_api()


# ---------- REGISTER ----------
@api.route('/register', methods=['POST'])
def register():
    return register_api()


# ---------- USERS ----------
@api.route('/users', methods=['GET'])
@login_required
@admin_required
def users():
    return get_users()

@api.route('/users', methods=['POST'])
@login_required
@admin_required
def add_user():
    return create_user()

@api.route('/users/<int:id_user>', methods=['PUT'])
@login_required
@admin_required
def edit_user(id_user):
    return update_user(id_user)

@api.route('/users/<int:id_user>', methods=['DELETE'])
@login_required
@admin_required
def remove_user(id_user):
    return delete_user(id_user)


# ---------- KANDANG ----------
@api.route('/kandang', methods=['GET'])
@login_required
def kandangs():
    return get_kandang()

@api.route('/kandang', methods=['POST'])
@login_required
@admin_required
def add_kandang():
    return create_kandang()

@api.route('/kandang/<int:id_kandang>', methods=['PUT'])
@login_required
@admin_required
def edit_kandang(id_kandang):
    return update_kandang(id_kandang)

@api.route('/kandang/<int:id_kandang>', methods=['DELETE'])
@login_required
@admin_required
def remove_kandang(id_kandang):
    return delete_kandang(id_kandang)


# ---------- HEWAN ----------
@api.route('/hewan', methods=['GET'])
@login_required
def hewans():
    return get_hewan()

@api.route('/hewan', methods=['POST'])
@login_required
def add_hewan():
    return create_hewan()

@api.route('/hewan/<int:id_hewan>', methods=['PUT'])
@login_required
def edit_hewan(id_hewan):
    return update_hewan(id_hewan)

@api.route('/hewan/<int:id_hewan>', methods=['DELETE'])
@login_required
@admin_required
def remove_hewan(id_hewan):
    return delete_hewan(id_hewan)


# ---------- EVENT ----------
@api.route('/event', methods=['GET'])
@login_required
def events():
    return get_events()

@api.route('/event', methods=['POST'])
@login_required
@admin_required
def add_event():
    return create_event()

@api.route('/event/<int:id>', methods=['PUT'])
@login_required
@admin_required
def edit_event(id):
    return update_event(id)

@api.route('/event/<int:id>', methods=['DELETE'])
@login_required
@admin_required
def remove_event(id):
    return delete_event(id)


# ---------- INVENTARIS ----------
@api.route('/inventaris', methods=['GET'])
@login_required
def inventaris():
    return get_inventaris()

@api.route('/inventaris', methods=['POST'])
@login_required
@admin_required
def add_inventaris():
    return create_inventaris()

@api.route('/inventaris/<int:id>', methods=['PUT'])
@login_required
@admin_required
def edit_inventaris(id):
    return update_inventaris(id)

@api.route('/inventaris/<int:id>', methods=['DELETE'])
@login_required
@admin_required
def remove_inventaris(id):
    return delete_inventaris(id)


# ---------- FASILITAS ----------
@api.route('/fasilitas', methods=['GET'])
@login_required
def fasilitas():
    return get_fasilitas()

@api.route('/fasilitas', methods=['POST'])
@login_required
@admin_required
def add_fasilitas():
    return create_fasilitas()

@api.route('/fasilitas/<int:id>', methods=['PUT'])
@login_required
@admin_required
def edit_fasilitas(id):
    return update_fasilitas(id)

@api.route('/fasilitas/<int:id>', methods=['DELETE'])
@login_required
@admin_required
def remove_fasilitas(id):
    return delete_fasilitas(id)

# ---------- FASILITAS ----------
@api.route('/logout', methods=['POST'])
@login_required
def logout():
    return logout_api()