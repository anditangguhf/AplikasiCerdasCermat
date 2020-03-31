# AplikasiCerdasCermat
Aplikasi Cerdas Cermat sbg tugas besar mata kuliah Jaringan Komputer

Anggota kelompok:
* 2015730005 - Nadya Vio
* 2015730017 - Andi Tangguh Kippi Nusantara

# Cara Penggunaan
Program dijalankan melalui terminal, dengan urutan sebagai berikut:
1. Jalankan `server.py` terlebih dahulu, masukkan jumlah client minimum sebagai syarat quiz dimulai
2. Jalankan `client.py`, kemudian masukkan nama dari Client. **Satu client tidak boleh memiliki nama yang sama dengan client lain**. jalankan minimal sebanyak yang dimasukkan sebagai syarat client minimum di server. Bisa memasukkan lebih dari batas minimum.
3. Server hanya akan melakukan monitoring client, input jawaban client, waktu delta dari client, dan menghitung score per client. Perhitungan score client adalah dengan menghitung `score soal * delta`, di mana delta telah diformat ulang hingga hanya mencakup 2 angka di belakang koma. Delta akan dikalikan dengan 100 sehingga akan membentuk nilai bulat yang cukup untuk menjadi pembeda delta antar client.
4. Server memiliki pengaturan dasar untuk timer per soal yaitu 15 detik, sehingga soal akan berganti otomatis setelah timer habis. Client yang tidak berhasil memasukkan jawaban sebelum soal berganti maka tidak akan mendapatkan nilai. Timer ini dapat diubah pada file `server.py` line 17, variabel `QUESTION_TIMER`
5. Setelah seluruh soal berhasil dikeluarkan, Server dan tiap Client akan menampilkan rekap score client dan keseluruhan client yang mengikuti quiz.

# Kemungkinan bug
* Terdapat bug yang belum diketahui sumber permasalahannya, kemungkinan adanya message yang conflict di client, sehingga saat melakukan parsing json dari server menjadi error. Bug ini terkadang muncul dan terkadang tidak, jika muncul yang bisa kami lakukan hingga saat ini adalah menjalankan seluruh program dari awal.
