

# 🧾 Soal Pemrograman: Pelacak Status Pesanan Pizza Concurrent

## 🧠 Latar Belakang

Sebuah restoran pizza yang sedang ramai pesanan membutuhkan sebuah dasbor internal untuk memantau semua pesanan yang sedang berjalan. Untuk membangun dasbor ini, diperlukan sebuah aplikasi client yang dapat **mengambil status setiap pesanan dari API sistem kasir**. Aplikasi ini harus:

- Mampu melacak status banyak pesanan sekaligus secara *concurrent* (paralel) agar dasbor selalu menampilkan data terbaru.
- Mencatat setiap aktivitas pelacakan (misalnya, "Baking", "Out for Delivery", atau "Order Not Found") ke dalam file log secara **aman dari race condition** untuk keperluan audit.
- Dapat menangani berbagai skenario error, seperti ID pesanan yang salah, API yang lambat merespons (timeout), atau error server lainnya.

Anda diminta untuk melengkapi kode Python yang sudah disiapkan untuk membuat aplikasi pelacak pesanan ini.

---

## 🎯 Tujuan

1. Memahami cara menggunakan **threading dan lock** untuk membangun sistem pemantauan yang efisien dan responsif.
2. Menerapkan **logging yang thread-safe** untuk pencatatan aktivitas yang akurat dalam sistem yang berjalan secara paralel.
3. Membuat client yang tangguh (*robust*) dan dapat diandalkan untuk berinteraksi dengan API eksternal, termasuk penanganan error yang baik.