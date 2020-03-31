Spesifikasi:
a.  multiple client (peserta cerdas cermat sekurang-kurangnya 2 peserta/group);
    tetapi spesifikasi dapat ditambahkan (misalnya bisa menangani n
    peserta/group, n >=2)
b.  client perlu melakukan autentikasi/user login hanya untuk membedakan nama
    peserta / group
c.  aplikasi yang menangani satu sesi cerdas cermat
d.  admin mengelola Q & A, bisa client – server
e.  Q and A dikirim ke (via server) ke client (para peserta) secara multicast
f.  Score setiap soal fixed; jumlah fixed
g.  Admin kirim soal – next untuk berikutnya; get time terima soal dan get time
    kirim jawab (deltanya) ; delta ini menentukan siapa yang lebih cepat
h.  Format file bank soal (separator #); file bisa format JSON/XML
    i.    No soal
    ii.   Soal
    iii.  Bobot nilai soal jika benar
    iv.   Pilihan jawaban a
    v.    Pilihan jawaban b
    vi.   Pilihan jawaban c
    vii.  Pilihan jawaban d
    viii. Jawaban benar
i.  Setelah sesi cerdas/cermat (soal habis) release score akhir/total ke
    client/peserta
j.  Soal akan berganti setelah waktu tertentu (1 menit – perlu di-optimalkan),
    terlepas sdh dijawab dan tidak dijawab oleh peserta
    i.    Bagi yang sudah menjawab, maka jika benar akan diberikan nilai
    ii.   Bagi yang tidak menjawab, nilai nya 0
k.  Disepakati: alternatif no j
    i.  Semua menjawab dan jika benar akan diberikan score sebesar bobot *
        persentase delta
    ii. Misalnya jika bobot soal: 1 dan deltanya 2 (yang paling cepat) akan
        diberikan score: 1; tetapi jika deltanya 3 (lebih lama) akan diberikan nilai
        lebih kecil dari 1, dst.... Bisa juga dengan cara mengurut berdasarkan
        delta. Delta terkecil diberikan angka full, disusul delta terkecil ke-2 80%
        dari bobot, dan seterusnya. Bagian ini mestinya dibuat tdk terlalu kaku.
