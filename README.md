# **Dashboard Analisis Data E-Commerce**

## **Ikhtisar Proyek**

Proyek ini bertujuan untuk menganalisis dataset publik E-Commerce dari Olist (sebuah platform e-commerce di Brasil). Analisis ini berfokus pada pemahaman perilaku pelanggan, melakukan segmentasi pelanggan menggunakan model RFM, dan memvisualisasikan distribusi geografis untuk mendapatkan wawasan bisnis yang berharga.

Hasil analisis kemudian disajikan dalam sebuah dasbor web interaktif yang dibangun menggunakan Streamlit, memungkinkan para pemangku kepentingan untuk dengan mudah menjelajahi dan memahami temuan-temuan kunci dari data.

## **Fitur Dasbor**

Dasbor interaktif ini terdiri dari tiga halaman utama:

1. **Ringkasan Umum:**  
   * Menampilkan metrik bisnis utama seperti Total Pendapatan, Total Pelanggan Unik, dan Jumlah Pesanan Keseluruhan.  
   * Visualisasi distribusi status pesanan untuk memantau efisiensi operasional.  
   * Grafik yang menunjukkan metode pembayaran yang paling sering digunakan oleh pelanggan.  
2. **Analisis Pelanggan (RFM):**  
   * Segmentasi pelanggan berbasis model RFM (*Recency, Frequency, Monetary*).  
   * Visualisasi distribusi untuk setiap komponen RFM guna memahami karakteristik pelanggan.  
   * Mengidentifikasi segmen pelanggan yang paling bernilai (*Champions*) serta pelanggan yang berisiko meninggalkan platform (*At Risk*).  
3. **Analisis Geografis:**  
   * Menampilkan 10 kota teratas berdasarkan total nilai pembelian.  
   * Peta interaktif yang memvisualisasikan sebaran geografis pelanggan di seluruh Brasil, memberikan gambaran tentang konsentrasi pasar.

## **Persiapan Lingkungan (Setup)**

Untuk dapat menjalankan dasbor ini secara lokal, pastikan Anda telah memiliki **Python 3.9+** dan manajer paket pip.

#### **1\. File yang Diperlukan**

Pastikan Anda memiliki semua file berikut dalam satu direktori/folder proyek:

* dashboard.py (skrip aplikasi Streamlit)  
* full\_data.csv (dataset utama yang telah dibersihkan dari notebook analisis)  
* geolocation\_dataset.csv (dataset geolokasi mentah dari Olist)  
* requirements.txt (dijelaskan di bawah)

#### **2\. Buat File requirements.txt**

Buat sebuah file baru bernama requirements.txt di dalam folder proyek Anda, lalu salin dan tempel daftar pustaka (library) berikut ke dalamnya:

streamlit  
pandas  
matplotlib  
seaborn

## **Cara Menjalankan Aplikasi**

Ikuti langkah-langkah di bawah ini untuk menjalankan dasbor di komputer Anda.

1. Clone Repository (atau Unduh File)  
   Unduh semua file yang diperlukan dari repository dan letakkan dalam satu folder.  
2. Buat Lingkungan Virtual (Direkomendasikan)  
   Buka terminal atau command prompt Anda, arahkan ke direktori proyek, dan jalankan perintah berikut untuk membuat dan mengaktifkan lingkungan virtual. Ini akan mengisolasi dependensi proyek Anda.  
   \# Membuat virtual environment  
   python \-m venv venv

   \# Mengaktifkan virtual environment  
   \# Untuk Windows:  
   venv\\Scripts\\activate  
   \# Untuk MacOS/Linux:  
   source venv/bin/activate

3. Instal Dependensi  
   Dengan lingkungan virtual yang sudah aktif, instal semua pustaka yang diperlukan dengan menjalankan perintah ini:  
   pip install \-r requirements.txt  
