import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Dasbor Analisis Pelanggan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Fungsi untuk Memuat Data ---
# Menggunakan cache untuk mempercepat pemuatan data pada interaksi berikutnya
@st.cache_data
def load_data(filepath):
    """Memuat data dari file CSV."""
    try:
        df = pd.read_csv(filepath)
        # Konversi kolom tanggal jika ada (meskipun tidak digunakan langsung di dasbor ini)
        # Jika file tidak ditemukan, berikan pesan error yang jelas
        return df
    except FileNotFoundError:
        st.error(f"File tidak ditemukan di '{filepath}'. Pastikan file 'rfm_with_geo_segments.csv' berada di direktori yang sama dengan skrip Streamlit Anda.")
        return None

# --- Memuat Data ---
# Ganti 'rfm_with_geo_segments.csv' dengan path yang benar jika perlu
DATA_URL = 'rfm_with_geo_segments.csv'
data = load_data(DATA_URL)

# --- Tampilan Utama ---
st.title("📊 Dasbor Analisis Pelanggan")
st.markdown("Dasbor interaktif untuk memvisualisasikan segmentasi pelanggan berdasarkan RFM (Recency, Frequency, Monetary) dan analisis geografis.")

# --- Sidebar untuk Navigasi ---
st.sidebar.title("Navigasi")
selection = st.sidebar.radio("Pilih Halaman:", 
    ['Ringkasan & Segmentasi RFM', 'Analisis Geografis', 'Distribusi Metrik RFM']
)
st.sidebar.markdown("---")
st.sidebar.info("Dasbor ini dibuat untuk menganalisis perilaku pelanggan dari data E-Commerce.")


# --- Logika Halaman ---
# Hanya jalankan jika data berhasil dimuat
if data is not None:

    # ==============================================================================
    # Halaman 1: Ringkasan & Segmentasi RFM
    # ==============================================================================
    if selection == 'Ringkasan & Segmentasi RFM':
        st.header("Segmentasi Pelanggan RFM")
        st.markdown("Halaman ini menampilkan pembagian pelanggan ke dalam segmen-segmen berbeda berdasarkan perilaku pembelian mereka.")

        # --- Visualisasi Distribusi Segmen ---
        st.subheader("Distribusi Segmen Pelanggan")
        
        # Hitung jumlah pelanggan per segmen
        segment_counts = data['Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Jumlah Pelanggan']

        # Buat bar chart dengan Plotly Express
        fig_segment = px.bar(
            segment_counts,
            x='Segment',
            y='Jumlah Pelanggan',
            color='Segment',
            title="Jumlah Pelanggan per Segmen",
            labels={'Segment': 'Segmen Pelanggan', 'Jumlah Pelanggan': 'Jumlah Pelanggan'},
            text='Jumlah Pelanggan'
        )
        fig_segment.update_traces(textposition='outside')
        fig_segment.update_layout(xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig_segment, use_container_width=True)
        
        st.markdown("""
        **Interpretasi:**
        - **Champions:** Pelanggan terbaik Anda. Mereka membeli baru-baru ini, sering, dan menghabiskan banyak uang.
        - **Loyal Customers:** Pelanggan yang membeli cukup sering dan baru-baru ini.
        - **Big Spenders:** Pelanggan yang menghabiskan banyak uang, meskipun mungkin tidak terlalu sering.
        - **Lapsed:** Pelanggan yang sudah lama tidak melakukan pembelian.
        - **At Risk / Lapsed Low Value:** Pelanggan bernilai rendah yang berisiko churn atau sudah tidak aktif.
        """)
        
        st.markdown("---")
        
        # --- Menampilkan Pelanggan Champions ---
        st.subheader("🏆 Pelanggan 'Champions' Teratas")
        st.markdown("Berikut adalah daftar pelanggan paling bernilai berdasarkan skor RFM gabungan.")
        
        champions_df = data[data['Segment'] == 'Champions'].sort_values(
            by='RFM_Score_Sum', ascending=False
        ).head(10)
        
        st.dataframe(champions_df[[
            'customer_unique_id', 'Recency', 'Frequency', 'MonetaryValue', 'RFM_Score_Sum', 'customer_city', 'customer_state'
        ]], use_container_width=True)


    # ==============================================================================
    # Halaman 2: Analisis Geografis
    # ==============================================================================
    elif selection == 'Analisis Geografis':
        st.header("Analisis Geografis Pelanggan")
        st.markdown("Melihat distribusi geografis pelanggan berdasarkan loyalitas dan nilai pembelian.")
        
        col1, col2 = st.columns(2)

        with col1:
            # --- Perbandingan Loyal vs Tidak Loyal ---
            st.subheader("Distribusi Pelanggan Loyal vs. Tidak Loyal")
            
            loyalty_counts = data.groupby(['customer_state', 'Loyalty']).size().reset_index(name='counts')
            loyal_customers = loyalty_counts[loyalty_counts['Loyalty'] == 'Loyal'].nlargest(10, 'counts')
            not_loyal_customers = loyalty_counts[loyalty_counts['Loyalty'] == 'Not Loyal'].nlargest(10, 'counts')
            
            fig_loyal = px.bar(
                loyal_customers, 
                x='customer_state', y='counts', 
                title='Top 10 Negara Bagian (Pelanggan Loyal)',
                labels={'customer_state': 'Negara Bagian', 'counts': 'Jumlah Pelanggan'},
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            st.plotly_chart(fig_loyal, use_container_width=True)

        with col2:
            st.subheader(" ") # spasi untuk alignment
            st.markdown(" ") # spasi untuk alignment
            
            fig_not_loyal = px.bar(
                not_loyal_customers,
                x='customer_state', y='counts',
                title='Top 10 Negara Bagian (Pelanggan Tidak Loyal)',
                labels={'customer_state': 'Negara Bagian', 'counts': 'Jumlah Pelanggan'},
                color_discrete_sequence=px.colors.qualitative.Pastel1
            )
            st.plotly_chart(fig_not_loyal, use_container_width=True)

        st.markdown("---")
        
        # --- Pelanggan Bernilai Tinggi ---
        st.subheader("Lokasi Pelanggan dengan Nilai Pembelian Tertinggi")
        st.markdown("Negara bagian dengan jumlah pelanggan 'Big Spenders' terbanyak.")

        big_spenders_geo = data[data['Segment'] == 'Big Spenders']['customer_state'].value_counts().nlargest(10).reset_index()
        big_spenders_geo.columns = ['Negara Bagian', 'Jumlah Pelanggan']

        fig_high_value = px.bar(
            big_spenders_geo,
            x='Negara Bagian',
            y='Jumlah Pelanggan',
            title="Top 10 Negara Bagian untuk Pelanggan Bernilai Tinggi",
            text='Jumlah Pelanggan',
            color='Negara Bagian'
        )
        fig_high_value.update_traces(textposition='outside')
        fig_high_value.update_layout(showlegend=False)
        st.plotly_chart(fig_high_value, use_container_width=True)
        

    # ==============================================================================
    # Halaman 3: Distribusi Metrik RFM
    # ==============================================================================
    elif selection == 'Distribusi Metrik RFM':
        st.header("Distribusi Metrik RFM")
        st.markdown("Memahami sebaran nilai Recency, Frequency, dan Monetary di seluruh basis pelanggan.")

        # Slider untuk memilih jumlah bins
        num_bins = st.slider('Pilih jumlah bins untuk histogram:', min_value=10, max_value=100, value=50)

        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram untuk Recency
            fig_recency = px.histogram(data, x='Recency', nbins=num_bins, title='Distribusi Recency')
            fig_recency.update_layout(bargap=0.1)
            st.plotly_chart(fig_recency, use_container_width=True)
        
        with col2:
            # Histogram untuk Monetary Value
            # Menggunakan log scale untuk menangani outlier
            fig_monetary = px.histogram(data, x='MonetaryValue', nbins=num_bins, title='Distribusi Monetary Value (Log Scale)', log_y=True)
            fig_monetary.update_layout(bargap=0.1)
            st.plotly_chart(fig_monetary, use_container_width=True)
            
        # Histogram untuk Frequency
        # Karena frekuensi sangat miring, kita akan memfilternya untuk visualisasi yang lebih baik
        st.subheader("Distribusi Frekuensi")
        st.markdown("Mayoritas pelanggan hanya membeli sekali. Grafik berikut menunjukkan distribusi untuk pelanggan dengan frekuensi > 1.")
        
        freq_filtered = data[data['Frequency'] > 1]
        fig_frequency = px.histogram(freq_filtered, x='Frequency', nbins=num_bins, title='Distribusi Frekuensi (untuk F > 1)', log_y=True)
        fig_frequency.update_layout(bargap=0.1)
        st.plotly_chart(fig_frequency, use_container_width=True)

# Pesan jika data tidak dapat dimuat
else:
    st.warning("Tidak dapat memuat data. Aplikasi tidak dapat dijalankan.")

