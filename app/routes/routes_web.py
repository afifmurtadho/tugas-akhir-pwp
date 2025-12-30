from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.middleware.auth import login_required
from app.controller.AuthController import login_web
from app.extensions import db
from app.model.user import User 
from werkzeug.security import generate_password_hash, check_password_hash
from app.model.hewan import Hewan 
from app.model.kandang import Kandang 
from app.model.inventaris import Inventaris
from app.model.event import Event
from app.model.fasilitas import Fasilitas

web = Blueprint('web', __name__)

# ==============================
# ROUTE LOGIN & REGISTER
# ==============================
@web.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id_user # Sesuai kolom id_user di database
            session['username'] = user.username
            session['nama'] = user.nama_lengkap # Sesuai kolom nama_lengkap di database
            session['role'] = user.role
            return redirect(url_for('web.dashboard'))
        
        flash('Username atau Password salah!', 'danger')
    return render_template('login.html')

# Route Register
@web.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        nama_lengkap = request.form.get('nama_lengkap')
        role = request.form.get('role')

        # Cek duplikasi
        if User.query.filter_by(username=username).first():
            flash('Username sudah ada!', 'warning')
            return redirect(url_for('web.register'))

        new_user = User(
            username=username,
            password=generate_password_hash(password),
            nama_lengkap=nama_lengkap,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Akun berhasil dibuat!', 'success')
        return redirect(url_for('web.login'))
    return render_template('register.html')


@web.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('web.login'))
    return render_template('dashboard.html', data=[])

@web.route('/home')
def home():
    # Karena Anda punya home.html dan dashboard.html, fungsi ini khusus untuk home.html
    if 'user_id' not in session: return redirect(url_for('web.login'))
    return render_template('home.html')

# Route Hewan
@web.route('/hewan', methods=['GET', 'POST'])
def hewan():
    if 'user_id' not in session:
        return redirect(url_for('web.login'))

    # --- LOGIKA POST (TAMBAH & UPDATE) ---
    if request.method == 'POST':
        mode = request.form.get('form_mode')
        
        # Ambil data dari form
        nama = request.form.get('nama_hewan')
        spesies = request.form.get('spesies')
        asal = request.form.get('asal')
        status = request.form.get('status_konservasi')
        tgl_masuk = request.form.get('tanggal_masuk')
        pakan = request.form.get('jenis_pakan')
        id_kandang = request.form.get('id_kandang')
        id_user = request.form.get('id_user')

        if mode == 'add':
            new_hewan = Hewan(
                nama_hewan=nama, spesies=spesies, asal=asal,
                status_konservasi=status, tanggal_masuk=tgl_masuk,
                jenis_pakan=pakan, id_kandang=id_kandang, id_user=id_user
            )
            db.session.add(new_hewan)
            db.session.commit()
            flash('Data hewan berhasil ditambahkan!', 'success')

        elif mode == 'update':
            id_h = request.form.get('id_hewan')
            h = Hewan.query.get(id_h)
            if h:
                h.nama_hewan = nama
                h.spesies = spesies
                h.asal = asal
                h.status_konservasi = status
                h.tanggal_masuk = tgl_masuk
                h.jenis_pakan = pakan
                h.id_kandang = id_kandang
                h.id_user = id_user
                db.session.commit()
                flash('Data hewan berhasil diperbarui!', 'success')
        
        return redirect(url_for('web.hewan'))

    daftar_hewan = db.session.query(
        Hewan.id_hewan, Hewan.nama_hewan, Hewan.spesies, Hewan.asal, 
        Hewan.status_konservasi, Hewan.tanggal_masuk, Hewan.jenis_pakan,
        Kandang.jenis_habitat, Kandang.lokasi_zona,
        User.nama_lengkap, User.username
    ).outerjoin(Kandang, Hewan.id_kandang == Kandang.id_kandang)\
     .outerjoin(User, Hewan.id_user == User.id_user).all()

    # 2. Cek apakah sedang mode Edit (ada parameter ?edit=ID di URL)
    edit_id = request.args.get('edit')
    hewan_to_edit = None
    if edit_id:
        hewan_to_edit = Hewan.query.get(edit_id)

    # 3. Ambil data untuk dropdown Kandang dan Petugas
    list_kandang = Kandang.query.all()
    list_users = User.query.all()

    return render_template('hewan.html', 
                           hewan=daftar_hewan, 
                           kandang=list_kandang, 
                           users=list_users,
                           hewan_to_edit=hewan_to_edit)

# Route Delete Hewan
@web.route('/hewan/delete/<int:id_hewan>')
def delete_hewan(id_hewan):
    if 'user_id' not in session: return redirect(url_for('web.login'))
    
    h = Hewan.query.get_or_404(id_hewan)
    db.session.delete(h)
    db.session.commit()
    flash('Data hewan berhasil dihapus!', 'success')
    return redirect(url_for('web.hewan'))

# ==============================
# Route Kandang
# ==============================
@web.route('/kandang', methods=['GET', 'POST'])
def kandang():
    if 'user_id' not in session:
        return redirect(url_for('web.login'))

    # --- 1. LOGIKA SIMPAN & UPDATE (POST) ---
    if request.method == 'POST':
        mode = request.form.get('form_mode')
        
        # Ambil data dari form kandang
        jenis_habitat = request.form.get('jenis_habitat')
        kapasitas = request.form.get('kapasitas')
        suhu_ideal = request.form.get('suhu_ideal')
        lokasi_zona = request.form.get('lokasi_zona')
        id_user = request.form.get('id_user')

        if mode == 'add':
            new_kandang = Kandang(
                jenis_habitat=jenis_habitat,
                kapasitas=kapasitas,
                suhu_ideal=suhu_ideal,
                lokasi_zona=lokasi_zona,
                id_user=id_user if id_user else None
            )
            db.session.add(new_kandang)
            db.session.commit()
            flash('Kandang baru berhasil ditambahkan!', 'success')

        elif mode == 'update':
            id_k = request.form.get('id_kandang')
            k = Kandang.query.get(id_k)
            if k:
                k.jenis_habitat = jenis_habitat
                k.kapasitas = kapasitas
                k.suhu_ideal = suhu_ideal
                k.lokasi_zona = lokasi_zona
                k.id_user = id_user if id_user else None
                db.session.commit()
                flash('Data kandang berhasil diperbarui!', 'success')
        
        return redirect(url_for('web.kandang'))

    # GET KANDANG
    daftar_kandang = db.session.query(
        Kandang.id_kandang, Kandang.jenis_habitat, Kandang.kapasitas, 
        Kandang.suhu_ideal, Kandang.lokasi_zona,
        User.nama_lengkap, User.username
    ).outerjoin(User, Kandang.id_user == User.id_user).all()

    # EDIT KANDANG
    edit_id = request.args.get('edit')
    kandang_to_edit = None
    if edit_id:
        kandang_to_edit = Kandang.query.get(edit_id)

    # Ambil daftar user untuk dropdown petugas
    list_users = User.query.all()

    return render_template('kandang.html', 
                           kandang=daftar_kandang,
                           users=list_users, 
                           kandang_to_edit=kandang_to_edit)

# DELETE KANDANG
@web.route('/kandang/delete/<int:id_kandang>')
def delete_kandang(id_kandang):
    if 'user_id' not in session:
        return redirect(url_for('web.login'))
    
    k = Kandang.query.get_or_404(id_kandang)
    try:
        db.session.delete(k)
        db.session.commit()
        flash('Kandang berhasil dihapus!', 'success')
    except:
        db.session.rollback()
        flash('Gagal menghapus! Kandang mungkin masih berisi hewan.', 'danger')
        
    return redirect(url_for('web.kandang'))

# ==============================
# ROUTE INVENTARIS
# ==============================
@web.route('/inventaris')
@web.route('/inventaris', methods=['GET', 'POST'])
def inventaris():
    if 'user_id' not in session:
        return redirect(url_for('web.login'))

    # --- 1. LOGIKA SIMPAN & UPDATE (POST) ---
    if request.method == 'POST':
        mode = request.form.get('form_mode')
        
        # Ambil data dari form
        nama_barang = request.form.get('nama_barang')
        kategori = request.form.get('kategori')
        jumlah = request.form.get('jumlah')
        satuan = request.form.get('satuan')
        kondisi = request.form.get('kondisi')
        tanggal_update = request.form.get('tanggal_update')

        if mode == 'add':
            new_item = Inventaris(
                nama_barang=nama_barang,
                kategori=kategori,
                jumlah=jumlah,
                satuan=satuan,
                kondisi=kondisi,
                tanggal_update=tanggal_update
            )
            db.session.add(new_item)
            db.session.commit()
            flash('Barang berhasil ditambahkan ke inventaris!', 'success')

        elif mode == 'update':
            id_inv = request.form.get('id_inventaris')
            item = Inventaris.query.get(id_inv)
            if item:
                item.nama_barang = nama_barang
                item.kategori = kategori
                item.jumlah = jumlah
                item.satuan = satuan
                item.kondisi = kondisi
                item.tanggal_update = tanggal_update
                db.session.commit()
                flash('Data inventaris berhasil diperbarui!', 'success')
        
        return redirect(url_for('web.inventaris'))

    # --- 2. LOGIKA TAMPIL DATA & EDIT (GET) ---
    
    # Ambil semua data inventaris
    daftar_inventaris = Inventaris.query.all()

    # Cek jika sedang mode Edit
    edit_id = request.args.get('edit')
    inventaris_to_edit = None
    if edit_id:
        inventaris_to_edit = Inventaris.query.get(edit_id)

    return render_template('inventaris.html', 
                           inventaris=daftar_inventaris, 
                           inventaris_to_edit=inventaris_to_edit)

@web.route('/inventaris/delete/<int:id_inventaris>')
def delete_inventaris(id_inventaris):
    if 'user_id' not in session:
        return redirect(url_for('web.login'))
    
    item = Inventaris.query.get_or_404(id_inventaris)
    db.session.delete(item)
    db.session.commit()
    flash('Barang berhasil dihapus dari inventaris!', 'success')
    return redirect(url_for('web.inventaris'))

# ===============
# ROUTE EVENT
# ===============

@web.route('/event', methods=['GET', 'POST'])
def event():
    if 'user_id' not in session:
        return redirect(url_for('web.login'))

    # --- 1. LOGIKA SIMPAN & UPDATE (POST) ---
    if request.method == 'POST':
        mode = request.form.get('form_mode')
        
        nama_event = request.form.get('nama_event')
        jenis_event = request.form.get('jenis_event')
        tanggal_event = request.form.get('tanggal_event')
        lokasi_event = request.form.get('lokasi_event')
        id_petugas = request.form.get('id_petugas')

        if mode == 'add':
            new_event = Event(
                nama_event=nama_event,
                jenis_event=jenis_event,
                tanggal_event=tanggal_event,
                lokasi_event=lokasi_event,
                id_petugas=id_petugas if id_petugas else None
            )
            db.session.add(new_event)
            db.session.commit()
            flash('Event baru berhasil ditambahkan!', 'success')

        elif mode == 'update':
            id_ev = request.form.get('id_event')
            ev = Event.query.get(id_ev)
            if ev:
                ev.nama_event = nama_event
                ev.jenis_event = jenis_event
                ev.tanggal_event = tanggal_event
                ev.lokasi_event = lokasi_event
                ev.id_petugas = id_petugas if id_petugas else None
                db.session.commit()
                flash('Data event berhasil diperbarui!', 'success')
        
        return redirect(url_for('web.event'))

    # --- 2. LOGIKA TAMPIL DATA & EDIT (GET) ---
    
    # Ambil data event dengan join ke User untuk mendapatkan nama penanggung jawab
    # Kita gunakan alias nama_petugas agar sesuai dengan {{ e.nama_petugas }} di HTML
    daftar_event = db.session.query(
        Event.id_event, Event.nama_event, Event.jenis_event, 
        Event.tanggal_event, Event.lokasi_event,
        User.nama_lengkap.label('nama_petugas') 
    ).outerjoin(User, Event.id_petugas == User.id_user).all()

    list_petugas = User.query.filter_by(role='petugas').all() 

    # Cek mode Edit
    edit_id = request.args.get('edit')
    event_to_edit = None
    if edit_id:
        event_to_edit = Event.query.get(edit_id)

    return render_template('event.html', 
                           event=daftar_event, 
                           petugas=list_petugas, 
                           event_to_edit=event_to_edit)

@web.route('/event/delete/<int:id_event>')
def delete_event(id_event):
    if 'user_id' not in session:
        return redirect(url_for('web.login'))
    
    ev = Event.query.get_or_404(id_event)
    db.session.delete(ev)
    db.session.commit()
    flash('Event berhasil dihapus!', 'success')
    return redirect(url_for('web.event'))

# =====================
# ROUTE FASILITAS
# =====================

@web.route('/fasilitas', methods=['GET', 'POST'])
def fasilitas():
    if 'user_id' not in session:
        return redirect(url_for('web.login'))

    # --- 1. LOGIKA SIMPAN & UPDATE (POST) ---
    if request.method == 'POST':
        mode = request.form.get('form_mode')
        
        nama_fasilitas = request.form.get('nama_fasilitas')
        lokasi = request.form.get('lokasi')
        kondisi = request.form.get('kondisi')
        jadwal_perawatan = request.form.get('jadwal_perawatan')
        id_user = request.form.get('id_user')

        # Jika jadwal_perawatan kosong string, ubah jadi None agar tidak error di DB date
        if not jadwal_perawatan:
            jadwal_perawatan = None

        if mode == 'add':
            new_fasil = Fasilitas(
                nama_fasilitas=nama_fasilitas,
                lokasi=lokasi,
                kondisi=kondisi,
                jadwal_perawatan=jadwal_perawatan,
                id_user=id_user if id_user else None
            )
            db.session.add(new_fasil)
            db.session.commit()
            flash('Fasilitas berhasil ditambahkan!', 'success')

        elif mode == 'update':
            id_f = request.form.get('id_fasilitas')
            fasil = Fasilitas.query.get(id_f)
            if fasil:
                fasil.nama_fasilitas = nama_fasilitas
                fasil.lokasi = lokasi
                fasil.kondisi = kondisi
                fasil.jadwal_perawatan = jadwal_perawatan
                fasil.id_user = id_user if id_user else None
                db.session.commit()
                flash('Data fasilitas berhasil diperbarui!', 'success')
        
        return redirect(url_for('web.fasilitas'))

    # --- 2. LOGIKA TAMPIL DATA & EDIT (GET) ---
    
    # Query join untuk mendapatkan nama petugas penanggung jawab
    daftar_fasilitas = db.session.query(
        Fasilitas.id_fasilitas, Fasilitas.nama_fasilitas, Fasilitas.lokasi,
        Fasilitas.kondisi, Fasilitas.jadwal_perawatan,
        User.nama_lengkap, User.username
    ).outerjoin(User, Fasilitas.id_user == User.id_user).all()

    # Ambil daftar semua user untuk dropdown penanggung jawab
    list_users = User.query.all()

    # Cek mode Edit
    edit_id = request.args.get('edit')
    fasilitas_to_edit = None
    if edit_id:
        fasilitas_to_edit = Fasilitas.query.get(edit_id)

    return render_template('fasilitas.html', 
                           fasilitas=daftar_fasilitas, 
                           users=list_users, 
                           fasilitas_to_edit=fasilitas_to_edit)

@web.route('/fasilitas/delete/<int:id_fasilitas>')
def delete_fasilitas(id_fasilitas):
    if 'user_id' not in session:
        return redirect(url_for('web.login'))
    
    fasil = Fasilitas.query.get_or_404(id_fasilitas)
    db.session.delete(fasil)
    db.session.commit()
    flash('Fasilitas berhasil dihapus!', 'success')
    return redirect(url_for('web.fasilitas'))

@web.route('/users')
def users():
    if session.get('role') != 'admin': 
        flash('Hanya Admin yang boleh mengakses halaman ini!', 'danger')
        return redirect(url_for('web.dashboard'))
    return render_template('users.html', data=[])

@web.route('/profile')
def profile():
    if 'user_id' not in session: return redirect(url_for('web.login'))
    return render_template('profile.html')

@web.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('web.login'))