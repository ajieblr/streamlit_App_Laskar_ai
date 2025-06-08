# **Laporan Lengkap Analisis Data Pelanggan E-Commerce**

Dokumen ini merinci semua tahapan yang dilakukan dalam proyek analisis data pelanggan, mulai dari pemrosesan data awal hingga interpretasi hasil dan visualisasi.

### **Tujuan Analisis**

Tujuan utama dari analisis ini adalah untuk memahami perilaku pelanggan secara mendalam dengan mengidentifikasi pelanggan paling bernilai, menemukan pola pembelian, dan mengelompokkan pelanggan ke dalam segmen-segmen yang dapat ditindaklanjuti. Wawasan ini bertujuan untuk membantu pengambilan keputusan strategis dalam bidang pemasaran, retensi pelanggan, dan pengembangan bisnis.

### **Tahap 1: Data Wrangling dan Data Cleaning**

Tahap ini merupakan fondasi dari seluruh analisis, di mana data mentah disiapkan agar bersih, konsisten, dan siap untuk dianalisis.

1. **Pemuatan Data:** Tiga dataset utama dimuat ke dalam lingkungan analisis menggunakan library pandas:  
   * customers\_dataset.csv: Informasi mengenai pelanggan.  
   * orders\_dataset.csv: Detail setiap pesanan yang dibuat.  
   * order\_items\_dataset.csv: Rincian item dalam setiap pesanan, termasuk harga.  
2. **Penggabungan Data (Merging):** Ketiga dataset tersebut digabungkan menjadi satu DataFrame tunggal yang komprehensif.  
   * orders\_df digabungkan dengan order\_items\_df menggunakan order\_id sebagai kunci.  
   * Hasilnya kemudian digabungkan dengan customers\_df menggunakan customer\_id sebagai kunci.  
   * Penggabungan ini memungkinkan kita untuk menghubungkan setiap item yang dibeli dengan pesanan dan pelanggan yang bersangkutan dalam satu baris data.  
3. **Pembersihan Data:**  
   * **Konversi Tipe Data:** Kolom-kolom yang berisi informasi tanggal (order\_purchase\_timestamp, order\_delivered\_customer\_date, dll.) diubah dari tipe data object (teks) menjadi datetime. Ini sangat penting untuk melakukan kalkulasi berbasis waktu seperti *Recency*.  
   * **Filtering Status Pesanan:** Analisis difokuskan pada pesanan yang telah berhasil terkirim (order\_status \== 'delivered'). Langkah ini penting karena pesanan yang dibatalkan atau belum sampai tidak merepresentasikan siklus pembelian yang lengkap dan tidak relevan untuk analisis nilai pelanggan.  
   * **Penanganan Nilai yang Hilang (Missing Values):** Data diperiksa untuk nilai yang hilang, terutama pada kolom krusial seperti order\_delivered\_customer\_date. Baris dengan nilai yang hilang pada kolom-kolom kunci untuk analisis RFM (Recency, Frequency, Monetary) dihapus untuk memastikan integritas data.  
   * **Pemeriksaan Duplikat:** Seluruh dataset diperiksa untuk baris duplikat dan baris yang identik sepenuhnya dihapus untuk menghindari perhitungan ganda.

### **Tahap 2: Analisis Data Eksploratif (EDA) & Kalkulasi RFM**

Setelah data bersih, kami melakukan analisis untuk menghitung metrik RFM, yang merupakan standar industri untuk segmentasi pelanggan.

* **Recency (Kebaruan):** Mengukur seberapa baru seorang pelanggan melakukan pembelian.  
  * **Kalkulasi:** Kami menentukan "tanggal snapshot" sebagai tanggal transaksi terakhir dalam dataset ditambah satu hari. Recency untuk setiap pelanggan dihitung sebagai selisih hari antara tanggal snapshot dan tanggal pembelian terakhir mereka. *Semakin kecil nilai Recency, semakin baik.*  
* **Frequency (Frekuensi):** Mengukur seberapa sering seorang pelanggan melakukan pembelian.  
  * **Kalkulasi:** Untuk setiap pelanggan unik (customer\_unique\_id), kami menghitung jumlah pesanan unik (order\_id) yang mereka buat. *Semakin tinggi nilai Frequency, semakin baik.*  
* **Monetary (Nilai Moneter):** Mengukur total nilai uang yang telah dibelanjakan oleh seorang pelanggan.  
  * **Kalkulasi:** Untuk setiap pelanggan, kami menjumlahkan total price dari semua item yang pernah mereka beli. *Semakin tinggi nilai Monetary, semakin baik.*

Hasil dari kalkulasi ini disimpan dalam sebuah DataFrame baru bernama rfm\_df yang menjadi dasar untuk segmentasi.

### **Tahap 3: Segmentasi Pelanggan**

Dengan metrik RFM yang telah dihitung, kami mengelompokkan pelanggan ke dalam segmen-segmen yang berbeda.

1. **Pemberian Skor RFM:** Setiap pelanggan diberi skor dari 1 hingga 5 untuk setiap metrik RFM menggunakan metode kuantil (qcut).  
   * Skor 5 untuk Recency diberikan kepada pelanggan yang paling baru membeli.  
   * Skor 5 untuk Frequency diberikan kepada pelanggan yang paling sering membeli.  
   * Skor 5 untuk Monetary diberikan kepada pelanggan yang paling banyak menghabiskan uang.  
2. **Pendefinisian Segmen:** Berdasarkan kombinasi skor R, F, dan M, segmen-segmen berikut didefinisikan:  
   * **Champions:** Pelanggan dengan skor tinggi di ketiga metrik (R, F, M ≥ 4). Mereka adalah pelanggan terbaik.  
   * **Loyal Customers:** Pelanggan yang sering membeli dan cukup baru (F ≥ 3, R ≥ 3).  
   * **Big Spenders:** Pelanggan yang menghabiskan banyak uang (M ≥ 4), meskipun mungkin tidak terlalu sering atau baru.  
   * **Lapsed:** Pelanggan yang sudah lama tidak membeli (R ≤ 2).  
   * **At Risk / Lapsed Low Value:** Pelanggan dengan skor rendah di Recency dan Frequency, berisiko tinggi untuk churn.  
   * **Others:** Pelanggan yang tidak masuk ke dalam kategori di atas.

### **Tahap 4: Analisis Geografis**

Untuk memahami di mana pelanggan berada, data geografis dari cleaned\_df digabungkan dengan rfm\_df.

* **Distribusi Pelanggan:** Kami menganalisis distribusi pelanggan berdasarkan negara bagian (customer\_state) dan kota (customer\_city).  
* **Perbandingan Geografis:** Kami membandingkan pola lokasi antara segmen pelanggan yang berbeda, seperti membandingkan lokasi pelanggan 'Loyal' dengan 'Tidak Loyal', serta lokasi pelanggan 'Champions' dan 'Big Spenders'.

### **Tahap 5: Visualisasi Data dengan Streamlit**

Untuk menyajikan hasil analisis secara interaktif dan mudah dipahami, sebuah dasbor web dibangun menggunakan **Streamlit**.

* **Tujuan Dasbor:** Memberikan visualisasi interaktif dari segmentasi pelanggan dan analisis geografis kepada para pemangku kepentingan.  
* **Fitur Utama Dasbor:**  
  1. **Halaman Ringkasan & Segmentasi RFM:** Menampilkan grafik batang distribusi jumlah pelanggan di setiap segmen dan daftar pelanggan 'Champions' teratas.  
  2. **Halaman Analisis Geografis:** Membandingkan lokasi pelanggan loyal vs. tidak loyal dan menunjukkan negara bagian dengan konsentrasi pelanggan bernilai tinggi terbanyak.  
  3. **Halaman Distribusi Metrik RFM:** Menyajikan histogram interaktif untuk Recency, Frequency, dan Monetary, yang memungkinkan pengguna untuk memahami sebaran dari setiap metrik.

### **Kesimpulan Utama dari Analisis**

* Mayoritas pelanggan adalah pembeli satu kali, yang menyoroti adanya peluang besar untuk meningkatkan retensi dan frekuensi pembelian.  
* Negara bagian **São Paulo (SP)** secara konsisten menjadi pusat bagi sebagian besar pelanggan di semua segmen, termasuk pelanggan paling bernilai ('Champions' dan 'Big Spenders').  
* Pelanggan yang membeli lebih dari satu kali (Frequency \> 1\) secara signifikan lebih bernilai (rata-rata MonetaryValue lebih tinggi) dibandingkan pembeli satu kali.  
* Segmentasi RFM berhasil mengidentifikasi kelompok pelanggan yang berbeda dengan jelas, yang dapat menjadi target untuk kampanye pemasaran yang dipersonalisasi.