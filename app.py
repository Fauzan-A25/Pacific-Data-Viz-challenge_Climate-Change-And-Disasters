import streamlit as st
from components.line_chart import show_line_chart
from components.bar_chart import show_bar_chart
from components.interactive_map import show_interactive_map
from components.dropdown_filter import get_selected_country
from data_cleaning import clean_energy_data

# ==================== CONFIG ====================
st.set_page_config(
    page_title="🌱 Pacific Renewable Energy",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================== PILIHAN BAHASA ====================
lang = st.sidebar.selectbox("🌐 Choose Language / Pilih Bahasa", ["English", "Indonesia"])

# ==================== TEKS MULTIBAHASA ====================
texts = {
    "English": {
        "title": "🌱 Pacific Renewable Energy Dashboard",
        "welcome": """
Welcome to the **Pacific Energy Dashboard** an interactive visualization platform designed to explore **renewable energy growth per capita** from **2000 to 2020** in **Pacific countries**.

**🎯 Dashboard Goals:**
- Present trends in renewable energy per capita
- Compare between countries
- Identify fastest and slowest growth
- Offer insights toward 2050 policy directions

---
""",
        "filter": "🔎 Country Filter",
        "line_chart_title": "📈 Renewable Energy Trend per Capita",
        "line_chart_desc": "Visualization of renewable energy growth per capita from 2000 to 2020 in selected countries.",
        "bar_chart_title": "📊 Annual Average Renewable Energy Trend",
        "bar_chart_desc": "Comparison of average renewable energy per capita per country.",
        "map_title": "🗺️ Pacific Countries Interactive Map (Dummy)",
        "map_desc": "Geographic context of Pacific countries.",
        "footer_target": "👥 **Target Audience:** Policymakers, researchers, students, and the general public interested in green energy.",
        "footer_caption": "📊 Data processed from Pacific Data Hub and visualized using Streamlit."
    },
    "Indonesia": {
        "title": "🌱 Dashboard Energi Terbarukan di Kawasan Pasifik",
        "welcome": """
Selamat datang di **Dashboard Energi Pasifik** platform visualisasi interaktif yang dirancang untuk mengeksplorasi **pertumbuhan energi terbarukan per kapita** dari tahun **2000 hingga 2020** di negara-negara **Pasifik**.

**🎯 Tujuan Dashboard:**
- Menyajikan tren energi terbarukan per kapita
- Membandingkan antar negara
- Mengidentifikasi perkembangan tercepat & terlambat
- Memberikan gambaran arah kebijakan menuju 2050

---
""",
        "filter": "🔎 Filter Negara",
        "line_chart_title": "📈 Tren Energi Terbarukan per Kapita",
        "line_chart_desc": "Visualisasi pertumbuhan energi terbarukan per kapita dari tahun 2000 hingga 2020 di negara-negara terpilih.",
        "bar_chart_title": "📊 Tren Rata-rata Tahunan Energi",
        "bar_chart_desc": "Perbandingan rata-rata energi terbarukan per kapita per negara.",
        "map_title": "🗺️ Peta Interaktif Negara Pasifik (Dummy)",
        "map_desc": "Visualisasi lokasi negara-negara Pasifik untuk memberikan konteks geografis.",
        "footer_target": "👥 **Target Audiens:** Pembuat kebijakan, peneliti, mahasiswa, dan masyarakat umum yang peduli energi hijau.",
        "footer_caption": "📊 Data diolah dari Pacific Data Hub dan divisualisasikan menggunakan Streamlit."
    }
}

t = texts[lang]  # Shortcut

# ==================== HEADER UTAMA ====================
st.title(t["title"])
st.markdown(t["welcome"])

# ==================== LOAD DATA ====================
clean_energy_data()
df = st.session_state.processed_data

# ==================== SIDEBAR ====================
st.sidebar.header(t["filter"])
selected_countries = get_selected_country(lang)

# ==================== SECTION 1: Line Chart ====================
st.subheader(t["line_chart_title"])
st.markdown(t["line_chart_desc"])
show_line_chart(df, selected_countries, lang)

# ==================== SECTION 2: Bar Chart ====================
st.subheader(t["bar_chart_title"])
st.markdown(t["bar_chart_desc"])
show_bar_chart(df, selected_countries, lang)

# ==================== SECTION 3: Map ====================
st.subheader(t["map_title"])
st.markdown(t["map_desc"])
show_interactive_map(df, selected_countries, lang)

# ==================== FOOTER ====================
st.markdown("---")
st.info(t["footer_target"])
st.caption(t["footer_caption"])
