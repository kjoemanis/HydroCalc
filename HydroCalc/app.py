import streamlit as st
import matplotlib.pyplot as plt
import time

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
        return data[umur_input]

    bawah = max([u for u in umur_tersedia if u < umur_input], default=None)
    atas = min([u for u in umur_tersedia if u > umur_input], default=None)

    if bawah is None or atas is None:
        return None

    y_bawah = data[bawah]
    y_atas = data[atas]
    proporsi = (umur_input - bawah) / (atas - bawah)
    return y_bawah + (y_atas - y_bawah) * proporsi

# UI
st.set_page_config(page_title="HydroCalc", page_icon="💧")

st.markdown("<h1 style='text-align: center; color: #2c7be5;'>💧 HydroCalc</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Kalkulator kebutuhan air tanaman berbasis data umur & jenis tanaman</p>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("### Masukkan Data Tanaman:")
tanaman = st.selectbox("Pilih jenis tanaman:", list(kebutuhan_air.keys()))
umur = st.number_input("Masukkan umur tanaman (hari):", min_value=1, step=1)
luas = st.number_input("Masukkan luas lahan (m²):", min_value=1.0, step=1.0)

if st.button("Hitung Kebutuhan Air"):
    with st.spinner("💡 Menghitung kebutuhan air..."):
        time.sleep(2)

        air_ml_per_100m2 = estimasi_air(kebutuhan_air[tanaman], umur)

        if air_ml_per_100m2 is None:
            st.error("Umur tanaman terlalu kecil atau terlalu besar dari data yang tersedia.")
        else:
            air_per_m2 = air_ml_per_100m2 / 100
            total_liter = air_per_m2 * luas / 1000

            st.markdown(f"<div style='padding:10px;background:#e6f4ea;border-left:6px solid #34a853; color:#000;'>"
                        f"<b>Hasil:</b> Kebutuhan air untuk <b>{tanaman}</b> umur <b>{umur} hari</b> pada lahan <b>{luas:.1f} m²</b> adalah:<br>"
                        f"<h3 style='color:#34a853'>{total_liter:.2f} liter</h3></div>", unsafe_allow_html=True)

            st.markdown("### 📈 Grafik Kebutuhan Air per Umur Tanaman")

            data = kebutuhan_air[tanaman]
            x_data = list(data.keys())
            y_data = list(data.values())

            fig, ax = plt.subplots()
            ax.plot(x_data, y_data, marker='o', linestyle='-', color='blue', label='Data asli')
            ax.axvline(x=umur, color='red', linestyle='--', label='Umur yang dipilih')
            ax.set_xlabel("Umur Tanaman (hari)")
            ax.set_ylabel("Kebutuhan Air (ml / 100m²)")
            ax.set_title(f"Kurva Kebutuhan Air - {tanaman}")
            ax.grid(True)
            ax.legend()

            st.pyplot(fig)

st.markdown("---")
st.caption("© 2025 HydroCalc | Made With Pyhton - Powered by Streamlit")
