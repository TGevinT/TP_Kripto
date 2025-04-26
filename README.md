# Anggota Kelompok
- Achmad Noval Fahrezi - 2106750931
- Raden Dhaneswara Timur Bhamakrti Rasendriya - 2106750710
- Teuku Gevin Taufan - 2106750194

# Penjelasan mengenai file-file pada folder

# 1. folder src

## sha256.py
File ini mengambil referensi dari https://medium.com/@domspaulo/python-implementation-of-sha-256-from-scratch-924f660c5d57. 
Kode yang tertera pada file ini diimplementasi **mulai dari awal tanpa menggunakan hashlib ataupun library tambahan**. 
Selain itu, berikut adalah penjelasan singkat pada masing-masing fungsi

- right_rotate(n, d): Fungsi untuk rotasi bit ke kanan sebanyak d posisi dalam 32-bit.
- Konstanta k: 64 buah konstanta untuk setiap ronde komputasi dalam SHA-256.
- Inisialisasi h: 8 buah nilai awal (h0-h7) standar SHA-256.
- Padding pesan: Menambahkan bit '1' diikuti '0' agar panjang pesan menjadi kelipatan 512-bit, dan menambahkan panjang asli pesan di akhir.
- Pemrosesan blok 512-bit:
- Memecah blok menjadi 64 buah word 32-bit (w).
- Setiap word dihitung menggunakan operasi rotasi dan shift.
- Loop kompresi 64 ronde:
- Update variabel kerja (a, b, c, d, e, f, g, h0) menggunakan operasi bitwise, rotasi, dan konstanta.
- Update nilai h akhir dengan menjumlahkan nilai sebelumnya dan nilai variabel kerja.
- Hasil akhir: Digabungkan menjadi array byte (bytes).

## utils.py

Pada file ini, akan berisi fungsi-fungsi dasar untuk mendukung pembuatan dan pengelolaan kunci RSA serta operasi dasar bilangan besar

- read_key_file: Membaca file kunci (modulus n dan eksponen exp) dalam format heksadesimal.
- write_key_file: Menulis n dan exp ke file dalam format heksadesimal.
- bytes_to_int dan int_to_bytes: Konversi antara tipe bytes dan int.
- secure_random_bits dan secure_random_bytes: Membuat bilangan acak aman secara kriptografis menggunakan secrets.
- is_prime: Mengecek apakah sebuah bilangan adalah prima dengan algoritma Miller-Rabin.
- egcd: Menghitung GCD dan koefisien Bezout menggunakan Extended Euclidean Algorithm.
- modinv: Menghitung invers modulo (penting untuk mencari private key RSA).

## decrypt.py
File ini bertujuan untuk mendekripsi file yang sebelumnya dienkripsi pada RSA dan OAEP. Akan digunakan pada main.py
Berikut adalah kontennya:

- read_key_file: Membaca modulus n dan private exponent d dari file private key.
- Menghitung k: Ukuran blok dalam byte berdasarkan panjang n.
- Proses dekripsi per blok:
1. Membaca blok terenkripsi dari file input.
2. Memastikan ukuran blok valid (k byte).
3. Mengubah blok dari bytes ke int.
4. Melakukan dekripsi RSA: m = c<sup>d</sup> mod n
5. Mengubah hasil dekripsi kembali ke bytes.
6. Menghapus OAEP padding dari hasil dekripsi.
7. Menulis plaintext ke file output.

## encrypt.py
File ini mendefinisikan fungsi rsa_encrypt_file untuk mengenkripsi file menggunakan RSA dengan OAEP padding
Berikut adalah kontennya:

- read_key_file: Membaca modulus n dan public exponent e dari file public key.
- Menghitung k: Ukuran blok RSA dalam byte.
- Menghitung max_block_size: Maksimal ukuran plaintext per blok setelah mempertimbangkan panjang padding OAEP.
- Proses enkripsi per blok:
1. Membaca blok plaintext dari file input.
2. Menambahkan OAEP padding pada blok.
3. Mengubah blok padded dari bytes ke int.
4. Melakukan enkripsi RSA: c = m<sup>e</sup>e mod n.
5. Menulis hasil ciphertext ke file output.

## oaep.py
File ini akan mendefinisikan fungsi-fungsi untuk OAEP (Optimal Asymmetric Encryption Padding) dalam proses RSA:
- mgf1: Mask Generation Function 1 — menghasilkan mask dari sebuah seed menggunakan SHA-256.
- oaep_pad:
1. Menambahkan padding OAEP ke sebuah pesan.
2. Langkah-langkah: buat label hash (l_hash), tambahkan padding string (ps), buat data block (db), buat seed acak, lalu mask db dan seed.
- oaep_unpad:
1. Menghapus OAEP padding dari hasil dekripsi.
2. Langkah-langkah: cek bit pertama, unmask seed dan db, verifikasi l_hash, cari delimiter 0x01, dan kembalikan pesan asli.

## rsa.py
Berisi kode yang bertugas untuk menghasilkan pasangan kunci RSA (public dan private) dengan konten:
- generate_large_prime: Membuat bilangan prima besar (default 1024 bit) dengan memastikan bit paling kiri (MSB) dan paling kanan (LSB) bernilai 1.
- generate_rsa_keypair:
1. Menghasilkan dua bilangan prima besar p dan q.
2. Menghitung:
+ n = p × q (modulus)
+ phi = (p-1) × (q-1) (fungsi totien Euler)
+ e = 65537 (eksponen publik standar)
+ d = modinv(e, phi) (eksponen privat)
3. Menyimpan kunci publik ke keys/public.txt dan kunci privat ke keys/private.txt.

## main.py
Berisi kode GUI utama dan juga memanggil fungsi-fungsi pengaturan enkripsi dan dekripsi

Di dalam aplikasinya, ada empat fitur utama yang dapat diakses melalui tombol:

1. Generate RSA Key Pair
Membuat sepasang kunci RSA 2048-bit (publik dan privat) lalu menyimpannya ke folder keys/. Proses ini menggunakan bilangan prima acak besar dan algoritma Extended Euclidean untuk menghitung kunci privat.

2. Encrypt File
Memungkinkan pengguna memilih file plaintext lewat file dialog, lalu mengenkripsinya menggunakan kunci publik RSA dengan padding OAEP. Ciphertext disimpan dalam file .bin.

3. Decrypt File
Membuka file ciphertext .bin, lalu melakukan dekripsi menggunakan kunci privat. Hasil dekripsi disimpan sebagai file baru, memungkinkan pengguna memilih lokasi penyimpanannya.

4. Run File Integrity Test
Fitur ini melakukan enkripsi-dekripsi otomatis terhadap sebuah file, lalu membandingkan file asli dengan hasil dekripsi. Jika identik, maka file dinyatakan aman (integritas terjaga); jika tidak, muncul peringatan.

5. Selain itu, semua proses yang sukses akan menampilkan notifikasi, dan error apapun ditangani serta ditampilkan ke pengguna melalui pop-up message.

# 1. folder tests

Berisi kumpulan file-file dalam bentuk binary executable file, image, dan video untuk pengecekan apakah berhasil atau tidak. Terdapat
juga hasil yang sudah dienkripsi dan yang sudah didekripsi