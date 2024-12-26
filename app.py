from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_mysqldb import MySQL, MySQLdb
import mysql.connector
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import hashlib

app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'minimarketsemesta.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'adminsemesta'
app.config['MYSQL_PASSWORD'] = 'Semesta123'
app.config['MYSQL_DB'] = 'minimarket_semesta'
app.config['MYSQL_PORT'] = 3306


app.secret_key = 'secret key'
CORS(app, origins=["http://127.0.0.1:3000"])
socketio = SocketIO(app)


# Initialize limiter after app is configured
# Initialize limiter with key_func
limiter = Limiter(key_func=get_remote_address)

# Initialize the app with limiter
limiter.init_app(app)

mysql = MySQL(app)

# Konfigurasi API Duitku
DUITKU_BASE_URL = "https://sandbox.duitku.com/webapi/api/merchant/v2/inquiry"
MERCHANT_CODE = "DS21366"  # Ganti dengan kode merchant Anda
MERCHANT_KEY = "d2a335e77105918ce19b9733f9e9fd52"  # Ganti dengan merchant key Anda



@app.route('/', methods=['GET', 'POST'])
@limiter.limit("3 per minute")  # Batasan 3 permintaan per menit
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return jsonify(success=False, error="Username dan password wajib diisi."), 400

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT id_akun, username, role FROM tbl_akun WHERE username = %s AND password = %s', (username, password))
        login = cursor.fetchone()
        print(login)

        if login:
            session['loggedin'] = True
            session['id_akun'] = login['id_akun']
            session['username'] = login['username']
            session['role'] = login['role']

            # Cek role kasir dan redirect sesuai dengan role
            if login['role'] == 'admin':
                return jsonify(success=True, redirect_url=url_for('riwayat'))  # Redirect ke riwayat jika role adalah admin
            elif login['role'] == 'kasir':
                return jsonify(success=True, redirect_url=url_for('transaksi'))  # Redirect ke transaksi jika role adalah kasir
            else:
                return jsonify(success=False, error="Role tidak valid!"), 403  # Jika role tidak valid
        else:
            return jsonify(success=False, error="Username atau password salah."), 401

    return render_template('login page.html')

@app.route('/logout')
def logout():
    if 'id_akun' in session:
        # Jika yang logout adalah admin
        session.pop('loggedin', None)
        session.pop('id_akun', None)
        session.pop('username', None)
        session.pop('password', None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
        
@app.route('/chat/<kasir>')
def chat_page(kasir):
    username = session.get('username')
    role = session.get('role')

    # Ambil pesan dari database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT * FROM tbl_chat 
        WHERE (pengirim = %s AND penerima = %s) 
           OR (pengirim = %s AND penerima = %s) 
        ORDER BY waktu_chat ASC
    """
    cursor.execute(query, (username, kasir, kasir, username))
    messages = cursor.fetchall()

    return render_template('admin chat.html', kasir=kasir, messages=messages)

@socketio.on('send_message')
def handle_send_message(data):
    pengirim = session.get('username')
    role = session.get('role')  # Untuk validasi tambahan
    penerima = data['penerima']
    message = data['message']
    print(f"Pengirim: {pengirim}, Penerima: {penerima}, Pesan: {message}")

    # Validasi penerima jika role adalah kasir
    if role == 'kasir':
        penerima = 'indra'  # Semua pesan dari kasir ditujukan ke admin
    elif role == 'admin' and not penerima:
        return  # Jika admin tidak menentukan penerima, abaikan pesan
    
    message = data['message']
    # Simpan pesan ke database
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """
            INSERT INTO tbl_chat (pengirim, penerima, chat, waktu_chat)
            VALUES (%s, %s, %s, NOW())
        """
        cursor.execute(query, (pengirim, penerima, message))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error menyimpan pesan: {e}")
        return

    # Kirimkan pesan ke penerima
    emit('receive_message', {
    'pengirim': pengirim,
    'penerima': penerima,
    'message': message
    }, broadcast=True)

@app.route('/payment', methods=['POST'])
def payment():
    # Ambil data dari session
    no_nota = session.get('no_nota')
    total_pembayaran = session.get('total_pembayaran')
    produk_list = session.get('produk_list', [])

    if not no_nota or not total_pembayaran or not produk_list:
        return jsonify({"error": "Data transaksi tidak lengkap."}), 400

    # Siapkan payload untuk API Duitku
    payment_method = request.form.get('payment_method', 'VC')  # Default ke Virtual Credit (VC)
    callback_url = "https://minimarketsemesta-a2bzf3fwd8a8fshq.canadacentral-01.azurewebsites.net/payment"  # URL untuk menerima notifikasi pembayaran
    # return_url = "http://yourdomain.com/return"  # URL untuk redirect setelah pembayaran

    # Buat signature
    signature_string = f"{MERCHANT_CODE}{no_nota}{total_pembayaran}{MERCHANT_KEY}"
    signature = hashlib.sha256(signature_string.encode('utf-8')).hexdigest()

    payload = {
        "merchantCode": MERCHANT_CODE,
        "paymentAmount": total_pembayaran,
        "paymentMethod": payment_method,
        "merchantOrderId": no_nota,
        "productDetails": "Pembelian Produk",
        "callbackUrl": callback_url,
        # "returnUrl": return_url,
        "signature": signature
    }

    headers = {"Content-Type": "application/json"}

    # Kirim permintaan ke API Duitku
    try:
        response = request.post(DUITKU_BASE_URL, json=payload, headers=headers)
        result = response.json()

        # Periksa apakah API berhasil
        if response.status_code == 200 and "paymentUrl" in result:
            payment_url = result["paymentUrl"]
            return redirect(payment_url)  # Redirect ke URL pembayaran
        else:
            return jsonify({"error": "Gagal membuat pembayaran.", "message": result.get("message", "Unknown error")}), 400

    except Exception as e:
        return jsonify({"error": "Terjadi kesalahan saat menghubungi API Duitku.", "details": str(e)}), 500 
    
@app.route('/transaksi', methods=['GET'])
def transaksi():
    if 'loggedin' in session:
        session['loggedin'] = True
        id_akun = session['id_akun']
        username = session['username']
        return render_template('dashboard kasir.html', id_akun=id_akun, username=username)
    else:
        return redirect(url_for('login'))  # Redirect to login page if not logged in
        
    
@app.route('/transaksi', methods=['GET', 'POST'])
def input_transaksi():
    if request.method == 'POST':
        # Periksa apakah form untuk menambahkan produk atau pembayaran
        if 'id_produk' in request.form and 'kuantitas_produk' in request.form:
            # Proses menambahkan produk ke keranjang
            no_nota = request.form['no_nota']
            session['no_nota'] = no_nota
            tanggal = request.form['tanggal']
            session['tanggal'] = tanggal
            pilih_produk = request.form['id_produk']
            kuantitas_produk = int(request.form['kuantitas_produk'])

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM tbl_produk WHERE id_produk = %s", (pilih_produk,))
            produk_data = cursor.fetchall()

            if not produk_data:
                print('Produk tidak ada')
                return redirect(url_for('transaksi'))

            # Ambil produk_list dari sesi
            produk_list = session.get('produk_list', [])

            # Tambahkan produk baru ke keranjang
            new_product = {
                'no_nota': no_nota,
                'id_produk': produk_data[0]['id_produk'],
                'nama_produk': produk_data[0]['nama_produk'],
                'kuantitas_produk': kuantitas_produk,
                'harga_satuan': produk_data[0]['harga_satuan'],
                'sub_total': kuantitas_produk * produk_data[0]['harga_satuan']
            }

            # Periksa apakah produk sudah ada di keranjang
            for produk in produk_list:
                if produk['id_produk'] == new_product['id_produk']:
                    produk['sub_total'] = produk['kuantitas_produk'] * produk['harga_satuan']
                    break
            else:
                # Tambahkan produk baru jika belum ada
                produk_list.append(new_product)

            session['produk_list'] = produk_list
            total_pembayaran = sum(produk['sub_total'] for produk in produk_list)
            session['total_pembayaran'] = total_pembayaran

            return render_template('dashboard kasir.html', produk_list=produk_list, total_pembayaran=total_pembayaran, tanggal=tanggal, no_nota=no_nota)

        elif 'dibayarkan' in request.form:
            # Proses pembayaran
            dibayarkan = int(request.form['dibayarkan'])
            session['dibayarkan'] = dibayarkan

            total_pembayaran = session.get('total_pembayaran')
            if total_pembayaran is None:
                return "Total pembayaran tidak ditemukan di sesi.", 400

            # Hitung kembalian
            kembalian = dibayarkan - total_pembayaran
            session['kembalian'] = kembalian

            # Ambil detail kasir dan transaksi dari sesi
            kasir = {'id_akun': session.get('id_akun')}
            no_nota = session.get('no_nota')
            tanggal = session.get('tanggal')
            produk_list = session.get('produk_list', [])
            if not produk_list:
                return "Produk list tidak ditemukan di sesi.", 400

            # Simpan transaksi ke database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            for produk in produk_list:
                cursor.execute(
                    '''INSERT INTO tbl_transaksi 
                    (no_nota, id_akun, id_produk, kuantitas_produk, harga_satuan, sub_total, tanggal_transaksi, total_pembayaran, dibayarkan, kembalian) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (no_nota, kasir['id_akun'], produk['id_produk'], produk['kuantitas_produk'], produk['harga_satuan'], produk['sub_total'], tanggal, total_pembayaran, dibayarkan, kembalian)
                )

            mysql.connection.commit()
            cursor.close()
            username = session['username']
            # Kembalikan data ke template
            return render_template('dashboard kasir.html', produk_list=produk_list, total_pembayaran=total_pembayaran, kembalian=kembalian, tanggal=tanggal, no_nota=no_nota, username=username)

    # GET request, tampilkan halaman transaksi
    return render_template('dashboard kasir.html', produk_list=session.get('produk_list', []), total_pembayaran=session.get('total_pembayaran', 0), kembalian=session.get('kembalian', 0))

@app.route('/admin/riwayat', methods=['GET', 'POST'])
def riwayat():
    if 'loggedin' in session and session.get('role') == 'admin':
        if request.method == 'GET':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
            # Mengambil semua data transaksi
            cursor.execute("SELECT * FROM tbl_transaksi")
            riwayat_transaksi = cursor.fetchall()
        
            transaksi_list = []
            for row in riwayat_transaksi:
                transaksi_list.append({
                    'id_transaksi': row['id_transaksi'],
                    'no_nota': row['no_nota'],
                    'id_akun': row['id_akun'],
                    'id_produk': row['id_produk'],
                    'kuantitas_produk': row['kuantitas_produk'],
                    'harga_satuan': row['harga_satuan'],
                    'sub_total': row['sub_total'],
                    'tanggal_transaksi': row['tanggal_transaksi'],
                    'total_pembayaran': row['total_pembayaran'],
                    'dibayarkan': row['dibayarkan'],
                    'kembalian': row['kembalian']
                })
            
            # Hitung jumlah produk
            cursor.execute('SELECT COUNT(*) as jumlah FROM tbl_produk')
            result = cursor.fetchone()
            jumlah_produk = result['jumlah'] if result else 0
            
            # Hitung jumlah pemasukan
            cursor.execute('SELECT SUM(total_pembayaran) AS total_pemasukan FROM tbl_transaksi')
            result = cursor.fetchone()
            total_pemasukan = result['total_pemasukan'] if result else 0
            
            # Mengambil transaksi dari kasir dengan id_akun = 1
            cursor.execute('''
                SELECT 
                    k.id_akun,
                    k.username,
                    t.id_transaksi,
                    t.tanggal_transaksi,
                    t.total_pembayaran,
                    t.dibayarkan,
                    t.kembalian
                FROM 
                    tbl_akun k
                JOIN 
                    tbl_transaksi t ON k.id_akun = t.id_akun
                WHERE 
                    k.id_akun = 1
            ''')
            kasir_satu = cursor.fetchall()
        
            # Mengambil transaksi dari kasir dengan id_akun = 2
            cursor.execute('''
                SELECT 
                    k.id_akun,
                    k.username,
                    t.id_transaksi,
                    t.no_nota,
                    t.tanggal_transaksi,
                    t.total_pembayaran,
                    t.dibayarkan,
                    t.kembalian
                FROM 
                    tbl_akun k
                JOIN 
                    tbl_transaksi t ON k.id_akun = t.id_akun
                WHERE 
                    k.id_akun = 2
            ''')
            kasir_dua = cursor.fetchall()

            cursor.close()
            
            return render_template('dashboard admin.html', transaksi_list=transaksi_list, jumlah_produk=jumlah_produk, total_pemasukan=total_pemasukan, kasir_satu=kasir_satu, kasir_dua=kasir_dua)
    else:
        return redirect(url_for('login page'))

@app.route('/produk', methods=['GET', 'POST'])
def produk():
    if 'loggedin' in session and session.get('role') == 'admin':
        # Pastikan session['id_akun'] dan session['username'] tersedia
        id_akun = session.get('id_akun')
        username = session.get('username')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if request.method == 'POST':
            if 'delete' in request.form:
                # Hapus produk
                id_produk = request.form['id_produk']
                cursor.execute('DELETE FROM tbl_produk WHERE id_produk = %s', (id_produk,))
                mysql.connection.commit()
                print('Data dihapus')
            else:
                # Tambah produk
                id_produk = request.form['id_produk']
                nama = request.form['nama_produk']
                harga = request.form['harga_produk']
                cursor.execute('INSERT INTO tbl_produk (id_produk, nama_produk, harga_satuan) VALUES (%s, %s, %s)', (id_produk, nama, harga))
                mysql.connection.commit()
                print('Data ditambahkan')

            cursor.close()
            return redirect(url_for('produk'))

        # Fetch all products
        cursor.execute('SELECT * FROM tbl_produk')
        produk_data = cursor.fetchall()
        produk_list = []
        for row in produk_data:
            produk_list.append({
                'id_produk': row['id_produk'],
                'nama_produk': row['nama_produk'],
                'harga_satuan': row['harga_satuan']
            })

        cursor.close()
        return render_template('managemen produk.html', produk_list=produk_list, id_akun=id_akun, username=username)
    else:
        return redirect(url_for('admin'))  # Redirect to login page if not logged in


@app.route('/produk/update', methods=['PUT', 'POST'])
def update_produk():
    if 'loggedin' in session and session.get('role') == 'admin':
        # Pastikan session['id_akun'] dan session['username'] tersedia
        id_akun = session.get('id_akun')
        username = session.get('username')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            id_produk = request.form['id_produk']
            print(id_produk)
            nama = request.form['edit_nama']
            print(nama)
            harga = request.form['edit_harga']
            print(harga)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sql = 'UPDATE tbl_produk SET nama_produk=%s, harga_satuan=%s WHERE id_produk=%s'
            sql_update = (nama, harga, id_produk)  # Define sql_update as a tuple
            cursor.execute(sql, sql_update)  # Pass sql_update as an argument
            mysql.connection.commit()
            return redirect(url_for('produk', id_akun=id_akun, username=username))
        else:
            print('produk tidak ada')

@app.route('/akun', methods=['GET', 'POST'])
def akun():
    if 'loggedin' in session and session.get('role') == 'admin':
        # Pastikan session['id_akun'] dan session['username'] tersedia
        id_akun = session.get('id_akun')
        username = session.get('username')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            if 'delete' in request.form:
                # Hapus akun kasir
                id_akun = request.form['id_akun']
                cursor.execute('DELETE FROM tbl_akun WHERE id_akun = %s', (id_akun,))
                mysql.connection.commit()
            else:
                # Tambah akun kasir
                username = request.form['username']
                password = request.form['password']
                cursor.execute('INSERT INTO tbl_akun (username, password) VALUES (%s, %s)', (username, password))
                mysql.connection.commit()

            cursor.close()
            return redirect(url_for('akun'))

        # Fetch all accounts
        cursor.execute('SELECT * FROM tbl_akun')
        akun_kasir_data = cursor.fetchall()
        akun_kasir_list = []
        for row in akun_kasir_data:
            akun_kasir_list.append({
                'id_akun': row['id_akun'],
                'username': row['username'],
                'password': row['password']
            })
        
        cursor.close()
        return render_template('managemen akun.html', akun_kasir_list=akun_kasir_list, id_akun=id_akun)
    else:
        return redirect(url_for('admin'))  # Redirect to login page if not logged in


@app.route('/akun/edit', methods=['GET', 'POST'])
def edit_akun():
    if 'loggedin' in session and session.get('role') == 'admin':
        # Pastikan session['id_akun'] dan session['username'] tersedia
        id_akun = session.get('id_akun')
        username = session.get('username')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            id_akun = request.form['id_akun']
            print(id_akun)
            nama = request.form['edit_nama']
            print(nama)
            password = request.form['password']
            print(password)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sql = 'UPDATE tbl_akun SET username=%s, password=%s WHERE id_akun=%s'
            sql_update = (nama, password, id_akun)  # Define sql_update as a tuple
            cursor.execute(sql, sql_update)  # Pass sql_update as an argument
            mysql.connection.commit()
            return redirect(url_for('akun', id_akun=id_akun, username=username))
        else:
            print('akun tidak ada')

def handle_rate_limit(e):
    return jsonify(success=False, error="Rate limit exceeded. Please wait a moment before trying again."), 429

if __name__ == '_main_':
    app.run(debug=True)
