# Tugas Akhir Pemrograman Jaringan

Anggota Kelompok:
| NRP         | Nama                             |
|-------------|----------------------------------|
| 5025231055  | Thalyta Vius Pramesti            |
| 5025231059  | Dinda Ayu Ningratu Putri         |
| 5025231138  | Aqila Zahira Naia Puteri Arifin  |
| 5025231312  | Annisa Salma Riavinola           |

# Instruksi Menjalankan Server dan Client

## 1. Persyaratan

- Pastikan `pygame` sudah terinstall.
  - Jika belum, install dengan perintah:
    ```bash
    pip install pygame
    ```

## 2. Langkah-langkah Menjalankan Server

1. Jalankan server dengan perintah:
    ```bash
    python server.py
    ```

2. Server akan menunggu koneksi dari 2 pemain (client) dan menampilkan pesan:
    ```
    Waiting for a connection, Server Started
    ```

## 3. Langkah-langkah Menjalankan Client

1. Buka terminal baru.

2. Jalankan `client.py` untuk pemain pertama menggunakan perintah:
    ```bash
    python client.py
    ```

3. Jendela permainan akan terbuka dengan antarmuka grafis berbasis `pygame`.

4. Buka terminal baru lagi, lalu jalankan `client.py` lagi untuk pemain kedua menggunakan perintah yang sama seperti pemain pertama:
    ```bash
    python client.py
    ```

5. Jendela permainan akan terbuka dengan antarmuka grafis berbasis `pygame`.

6. Setelah kedua client saling terhubung, permainan bisa dilanjutkan (Rock-Paper-Scissors).
