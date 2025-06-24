import streamlit as st

# Data kebutuhan air (ml/100 m²)
kebutuhan_air = {
    "Cabai": {
        10: 28000, 30: 44000, 45: 100000, 60: 168800,
        75: 240000, 80: 320000, 95: 459200, 100: 480000, 120: 529200
    },
    "Jagung": {
        10: 28000, 30: 48000, 45: 100000, 60: 140000,
        75: 120000, 80: 80000, 95: 60000, 100: 40000, 120: 20000
    },
    "Padi": {
        10: 28000, 30: 44000, 45: 100000, 60: 168800,
        75: 240000, 80: 320000, 95: 459200, 100: 480000, 120: 529200
    }
}

st.set_page_config(page_title="HydroCalc", page_icon="💧")
st.title("💧 HydroCalc - Kalkulator Kebutuhan Air Tanaman")
st.markdown("Perhitungan berdasarkan data kebutuhan air tanaman pada umur tertentu per 100 m².")

# Input pengguna
tanaman = st.selectbox("Pilih jenis tanaman:", list(kebutuhan_air.keys()))
umur = st.selectbox("Pilih umur tanaman (hari):", list(kebutuhan_air[tanaman].keys()))
luas = st.number_input("Masukkan luas lahan (m²):", min_value=1.0)

if st.button("Hitung Kebutuhan Air"):
    kebutuhan_per_100m2 = kebutuhan_air[tanaman][umur]  # dalam ml
    kebutuhan_per_m2 = kebutuhan_per_100m2 / 100         # ml per m²
    total_kebutuhan_ml = kebutuhan_per_m2 * luas
    total_kebutuhan_liter = total_kebutuhan_ml / 1000    # konversi ke liter

    st.success(f"Kebutuhan air untuk {tanaman} umur {umur} hari pada lahan {luas:.1f} m² adalah: **{total_kebutuhan_liter:.2f} liter**")
