import streamlit as st
import matplotlib.pyplot as plt

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
        return data[umur_input], False

    bawah = max([u for u in umur_tersedia if u < umur_input], default=None)
    atas = min([u for u in umur_tersedia if u > umur_input], default=None)

    if bawah is None or atas is None:
        return None, None

    y_bawah = data[bawah]
    y_atas = data[atas]
    proporsi = (umur_input - bawah) / (atas - bawah)
    estimasi = y_bawah + (y_atas - y_bawah) * proporsi

    return estimasi, True

# UI
st.set_page_config(page_title="HydroCalc", page_icon="💧")
st.title("💧 HydroCalc - Kalkulator Kebutuhan Air Tanaman")

st.markdown(
    "Masukkan umur tanaman dan luas lahan. "
    "Jika umur tidak tersedia, sistem akan memperkirakan nilai menggunakan interpolasi. "
    "Grafik di bawah membantu memahami perubahan kebutuhan air berdasarkan umur tanaman."
)

tanaman = st.selectbox("Pilih jenis tanaman:", list(kebutuhan_air.keys()))
umur = st.number_input("Masukkan umur tanaman (hari):", min_value=1, step=1)
luas = st.number_input("Masukkan luas lahan (m²):", min_value=1.0, step=1.0)

if st.button("Hitung Kebutuhan Air"):
    air_ml_per_100m2, interpolasi = estimasi_air(kebutuhan_air[tanaman], umur)

    if air_ml_per_100m2 is None:
        st.error("Umur tanaman terlalu kecil atau terlalu besar dari data yang tersedia.")
    else:
        air_per_m2 = air_ml_per_100m2 / 100
        total_liter = air_per_m2 * luas / 1000

        st.success(f"Kebutuhan air untuk {tanaman} umur {umur} hari pada lahan {luas:.1f} m² adalah: **{total_liter:.2f} liter**")

        if interpolasi:
            st.info("⚠️ Hasil merupakan estimasi interpolasi karena umur tidak ada dalam data.")

        # Buat grafik
        data = kebutuhan_air[tanaman]
        x_data = list(data.keys())
        y_data = list(data.values())

        fig, ax = plt.subplots()
        ax.plot(x_data, y_data, marker='o', linestyle='-', color='blue', label='Data asli')
        ax.set_xlabel("Umur Tanaman (hari)")
        ax.set_ylabel("Kebutuhan Air (ml / 100m²)")
        ax.set_title(f"Kurva Kebutuhan Air - {tanaman}")
        ax.grid(True)

        # Tambahkan titik umur input user
        ax.axvline(x=umur, color='red', linestyle='--', label='Umur yang dipilih')
        ax.legend()

        st.pyplot(fig)

st.caption("© 2025 HydroCalc | Dibuat dengan Python + Streamlit + Matplotlib")
