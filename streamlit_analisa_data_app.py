import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

# --- Konfigurasi Halaman ---
st.set_page_config(layout="wide")

# Mengatur gaya plot
sns.set(style='dark')

# --- Fungsi untuk Memuat dan Menggabungkan Data ---
@st.cache_data
def load_data():
    # Memuat data utama yang telah diproses
    all_df = pd.read_csv("full_data.csv")
    
    # Memuat data geolokasi
    geoloc_df = pd.read_csv("geolocation_data.csv")
    
    # Mengagregasi data geolokasi untuk mendapatkan satu lat/lng per zip code (mengambil median)
    # Ini untuk efisiensi dan menghindari duplikasi
    geolocation_agg_df = geoloc_df.groupby('geolocation_zip_code_prefix').agg({
        'geolocation_lat': 'median',
        'geolocation_lng': 'median'
    }).reset_index()
    
    # Menggabungkan data utama dengan data geolokasi berdasarkan zip code
    merged_data = pd.merge(
        all_df,
        geolocation_agg_df,
        left_on='customer_zip_code_prefix',
        right_on='geolocation_zip_code_prefix',
        how='left'
    )
    return merged_data

# --- Fungsi untuk Kalkulasi RFM ---
@st.cache_data
def calculate_rfm(df):
    """
    Menghitung Recency, Frequency, dan Monetary value untuk setiap pelanggan.
    """
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    
    snapshot_date = df['order_purchase_timestamp'].max() + dt.timedelta(days=1)
    
    rfm_df = df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (snapshot_date - x.max()).days,
        'order_id': 'nunique',
        'payment_value': 'sum'
    }).reset_index()
    
    rfm_df.rename(columns={
        'order_purchase_timestamp': 'Recency',
        'order_id': 'Frequency',
        'payment_value': 'Monetary'
    }, inplace=True)
    
    return rfm_df

# --- Fungsi Utama Aplikasi ---
def main():
    all_df = load_data()

    # --- Sidebar untuk Navigasi ---
    st.sidebar.title("Navigasi Dasbor")
    page = st.sidebar.selectbox("Pilih Halaman:", 
                                ["Ringkasan Umum", "Analisis Pelanggan (RFM)", "Analisis Geografis"])

    # --- Halaman Utama: Ringkasan Umum ---
    if page == "Ringkasan Umum":
        st.title('📊 Dasbor Analisis E-Commerce')
        st.markdown("Dasbor ini menyajikan analisis dari data E-Commerce publik Brasil.")
        
        st.header('Metrik Utama')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Pelanggan Unik", f"{all_df['customer_unique_id'].nunique():,}")
        with col2:
            st.metric("Total Pesanan", f"{all_df['order_id'].nunique():,}")
        with col3:
            st.metric("Total Pendapatan", f"R$ {all_df['payment_value'].sum():,.2f}")

        st.subheader("Distribusi Status Pesanan")
        fig, ax = plt.subplots(figsize=(10, 5))
        order_status_counts = all_df['order_status'].value_counts()
        sns.barplot(x=order_status_counts.index, y=order_status_counts.values, ax=ax, palette="viridis")
        ax.set_title('Jumlah Pesanan Berdasarkan Status')
        ax.set_ylabel('Jumlah Pesanan')
        ax.set_xlabel('Status Pesanan')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

        st.subheader("Metode Pembayaran Populer")
        fig, ax = plt.subplots(figsize=(10, 5))
        payment_type_counts = all_df['payment_type'].dropna().value_counts().head(5)
        sns.barplot(x=payment_type_counts.index, y=payment_type_counts.values, ax=ax, palette="flare")
        ax.set_title('Top 5 Metode Pembayaran yang Digunakan')
        ax.set_ylabel('Jumlah Transaksi')
        ax.set_xlabel('Tipe Pembayaran')
        st.pyplot(fig)

    # --- Halaman Analisis Pelanggan (RFM) ---
    elif page == "Analisis Pelanggan (RFM)":
        st.title('Segmentasi Pelanggan Berdasarkan RFM')
        st.markdown("Analisis RFM (Recency, Frequency, Monetary) untuk mengidentifikasi pelanggan paling bernilai.")

        rfm_df = calculate_rfm(all_df)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_recency = round(rfm_df.Recency.mean(), 1)
            st.metric("Rata-rata Recency (Hari)", value=avg_recency)
        with col2:
            avg_frequency = round(rfm_df.Frequency.mean(), 1)
            st.metric("Rata-rata Frequency", value=avg_frequency)
        with col3:
            avg_monetary = round(rfm_df.Monetary.mean(), 2)
            st.metric("Rata-rata Monetary (R$)", value=f"{avg_monetary:,.2f}")
        
        st.subheader("Distribusi Pelanggan Berdasarkan RFM Score")
        fig, axes = plt.subplots(1, 3, figsize=(20, 6))
        
        sns.histplot(rfm_df['Recency'], bins=30, kde=True, ax=axes[0], color='skyblue')
        axes[0].set_title('Distribusi Recency')
        
        sns.histplot(rfm_df['Frequency'], bins=30, kde=True, ax=axes[1], color='salmon')
        axes[1].set_title('Distribusi Frequency')
        
        sns.histplot(rfm_df['Monetary'], bins=30, kde=True, ax=axes[2], color='lightgreen')
        axes[2].set_title('Distribusi Monetary')
        
        st.pyplot(fig)
        
        st.markdown("""
        **Insight:** - **Recency:** Sebagian besar pelanggan melakukan pembelian dalam 200 hari terakhir.
        - **Frequency:** Mayoritas pelanggan hanya melakukan satu kali transaksi, menunjukkan adanya peluang besar untuk meningkatkan retensi.
        - **Monetary:** Distribusi nilai moneter cenderung miring ke kanan, menandakan ada sejumlah kecil pelanggan yang berbelanja dengan nilai sangat tinggi.
        """)

    # --- Halaman Analisis Geografis ---
    elif page == "Analisis Geografis":
        st.title('Analisis Geografis Pelanggan')
        
        st.subheader('Pelanggan dengan Nilai Pembelian Tertinggi Berdasarkan Wilayah (Kota)')
        
        city_payment = all_df.groupby('customer_city')['payment_value'].sum().sort_values(ascending=False).head(10)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=city_payment.values, y=city_payment.index, palette="mako", ax=ax)
        ax.set_title('Top 10 Kota dengan Total Nilai Pembelian Tertinggi')
        ax.set_xlabel('Total Nilai Pembelian (R$)')
        ax.set_ylabel('Kota')
        st.pyplot(fig)
        st.markdown("São Paulo dan Rio de Janeiro secara signifikan mendominasi total nilai pembelian, menunjukkan konsentrasi pasar di kota-kota besar.")
        
        st.subheader('Peta Sebaran Pelanggan di Brasil')
        # Menghapus duplikat dan nilai NaN untuk visualisasi peta yang lebih bersih
        geo_df = all_df[['customer_unique_id', 'geolocation_lat', 'geolocation_lng']].drop_duplicates(subset='customer_unique_id').dropna()
        st.map(geo_df, latitude='geolocation_lat', longitude='geolocation_lng', size=10)
        st.markdown("Peta interaktif di atas menunjukkan konsentrasi pelanggan yang sangat padat di wilayah tenggara dan selatan Brasil, terutama di sekitar kota-kota besar.")

if __name__ == '__main__':
    main()