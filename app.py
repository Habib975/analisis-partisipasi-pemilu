import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Partisipasi Pemilu Pamekasan")

st.title("📊 Analisis Partisipasi Pemilu 2019 - Kabupaten Pamekasan")

# Upload file
uploaded_file = st.file_uploader("📂 Unggah file", type="csv")

def klasifikasi(p):
    if pd.isna(p):
        return 'Tidak Diketahui'
    elif p >= 75:
        return 'Tinggi'
    else:
        return 'Rendah'

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Bersihkan kolom
    df.columns = df.columns.str.strip()
    df.rename(columns={'G1': 'kecamatan', 'G2': 'kelurahan', 'P': 'persentase'}, inplace=True)

    df['kecamatan'] = df['kecamatan'].astype(str).str.strip().str.upper().replace({'BATUMAMAR': 'BATUMARMAR'})
    df['kelurahan'] = df['kelurahan'].astype(str).str.strip().str.upper()
    df['persentase'] = pd.to_numeric(df['persentase'].astype(str).str.replace(',', '.'), errors='coerce')

    # Agregasi
    avg_kec = df.groupby('kecamatan')['persentase'].mean().reset_index()
    avg_kec['kategori'] = avg_kec['persentase'].apply(klasifikasi)
    avg_kec = avg_kec.sort_values(by='persentase', ascending=False)

    avg_kel = df.groupby(['kecamatan', 'kelurahan'])['persentase'].mean().reset_index()
    avg_kel['kategori'] = avg_kel['persentase'].apply(klasifikasi)
    top20 = avg_kel.sort_values(by='persentase', ascending=False).head(20)

    # Statistik
    tinggi_kec = avg_kec[avg_kec['kategori'] == 'Tinggi'].shape[0]
    rendah_kec = avg_kec[avg_kec['kategori'] == 'Rendah'].shape[0]
    tinggi_kel = avg_kel[avg_kel['kategori'] == 'Tinggi'].shape[0]
    rendah_kel = avg_kel[avg_kel['kategori'] == 'Rendah'].shape[0]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("📍 Kecamatan dengan Partisipasi Tinggi", tinggi_kec)
        st.metric("📍 Kecamatan dengan Partisipasi Rendah", rendah_kec)
    with col2:
        st.metric("🏘️ Kelurahan dengan Partisipasi Tinggi", tinggi_kel)
        st.metric("🏘️ Kelurahan dengan Partisipasi Rendah", rendah_kel)

    # Tabs UI
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📍 Kecamatan", 
        "🏅 Top 20 Kelurahan", 
        "🟢 Semua Partisipasi Tinggi", 
        "🔴 Semua Partisipasi Rendah", 
        "📜 Semua Kelurahan"
    ])

    with tab1:
        st.subheader("📌 Rata-rata Partisipasi per Kecamatan")
        st.dataframe(avg_kec.style.background_gradient(subset='persentase', cmap='YlGn'))

        fig1, ax1 = plt.subplots(figsize=(14, 6))
        colors = avg_kec['kategori'].map({'Tinggi': 'green', 'Rendah': 'red'})
        ax1.bar(avg_kec['kecamatan'], avg_kec['persentase'], color=colors)
        ax1.set_title("🎯 Partisipasi Pemilu per Kecamatan")
        ax1.set_ylabel("Persentase Partisipasi (%)")
        ax1.set_xticklabels(avg_kec['kecamatan'], rotation=45, ha='right')
        ax1.grid(axis='y', linestyle='--', alpha=0.5)
        st.pyplot(fig1)

    with tab2:
        st.subheader("🏆 Top 20 Kelurahan dengan Partisipasi Tertinggi")
        st.dataframe(top20.style.background_gradient(subset='persentase', cmap='BuGn'))

        fig2, ax2 = plt.subplots(figsize=(14, 6))
        colors = top20['kategori'].map({'Tinggi': 'darkblue', 'Rendah': 'orange'})
        ax2.bar(top20['kelurahan'], top20['persentase'], color=colors)
        ax2.set_xticklabels(top20['kelurahan'], rotation=90)
        ax2.set_ylabel("Tingkat Partisipasi (%)")
        ax2.set_title("Top 20 Kelurahan/Desa Berdasarkan Partisipasi")
        ax2.grid(axis='y', linestyle='--', alpha=0.5)
        st.pyplot(fig2)

    with tab3:
        st.subheader("🟢 Daftar Semua Kelurahan dengan Partisipasi Tinggi")
        st.dataframe(avg_kel[avg_kel['kategori'] == 'Tinggi'].sort_values(by='persentase', ascending=False))

    with tab4:
        st.subheader("🔴 Daftar Semua Kelurahan dengan Partisipasi Rendah")
        st.dataframe(avg_kel[avg_kel['kategori'] == 'Rendah'].sort_values(by='persentase'))

    with tab5:
        st.subheader("📜 Semua Data Kelurahan/Desa")
        st.dataframe(avg_kel.sort_values(by='persentase', ascending=False))

else:
    st.info("⬆️ Silakan unggah file terlebih dahulu.")
