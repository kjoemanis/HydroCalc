import streamlit as st

# Data kebutuhan air (ml/100m²)
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

def estimasi_air(data, umur_input):
    umur_tersedia = sorted(data.keys())
    if umur_input in data:
        return data[umur_input], False  # False = bukan interpolasi

    bawah = max([u for u in umur_tersedia if u < umur_input], default=None)
    atas = min([u for u in umur_tersedia if u > umur_input], default=None)

    if bawah is None or atas is None:
        return None, None  # di luar rentang data

    y_bawah = data[bawah]
    y_atas = data[atas]
    proporsi = (umur_input - bawah) / (atas - bawah)
    estimasi = y_bawah + (y_atas - y_bawah) * proporsi

    return estimasi, True  # True = hasil interpolasi

# UI
st.set_page_config(page_title="HydroCalc", page_icon="💧")
st.title("💧 HydroCalc - Kalkulator Kebutuhan Air Tanaman")
st.markdown("Perhitungan berdasarkan umur tanaman dan data empiris. Sistem dapat mengestimasi kebutuhan air jika umur tidak ada dalam data.")

# Input pengguna
tanaman = st.selectbox("Pilih jenis tanaman:", list(kebutuhan_air.keys()))
umur = st.number_input("Masukkan umur tanaman (hari):", min_value=1, step=1)
luas = st.number_input("Masukkan luas lahan (m²):", min_value=1.0, step=1.0)

if st.button("Hitung Kebutuhan Air"):
    air_ml_per_100m2, interpolasi = estimasi_air(kebutuhan_air[tanaman], umur)

    if air_ml_per_100m2 is None:
        st.error("Umur tanaman terlalu kecil atau terlalu besar dari data yang tersedia.")
    else:
        air_per_m2 = air_ml_per_100m2 / 100
        total_liter = air_per_m2 * luas / 1000  # dari ml ke liter

        st.success(f"Kebutuhan air untuk {tanaman} umur {umur} hari pada lahan {luas:.1f} m² adalah: **{total_liter:.2f} liter**")

        if interpolasi:
            st.info("⚠️ Umur tanaman tidak ada dalam data. Nilai di atas merupakan estimasi hasil interpolasi.")

st.caption("© 2025 HydroCalc | Dibuat dengan Python + Streamlit")
