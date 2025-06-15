import streamlit as st
import plotly.express as px

def show_bar_chart(df, selected_country, lang="Indonesia"):
    # Kamus teks dua bahasa
    texts = {
        "Indonesia": {
            "select_year": "📅 Pilih Tahun:",
            "compare_with": "🔄 Bandingkan dengan negara lain:",
            "title": "Perbandingan Rata-Rata Energi Terbarukan per Kapita ({year}): {a} vs {b}",
            "x_title": "Negara",
            "y_title": "Energi Terbarukan per Kapita (kWh)"
        },
        "English": {
            "select_year": "📅 Select Year:",
            "compare_with": "🔄 Compare with another country:",
            "title": "Comparison of Average Renewable Energy per Capita ({year}): {a} vs {b}",
            "x_title": "Country",
            "y_title": "Renewable Energy per Capita (kWh)"
        }
    }

    t = texts[lang]  # shortcut untuk teks bahasa terpilih

    # Dropdown untuk memilih tahun
    selected_year = st.selectbox(t["select_year"], sorted(df["Year"].unique()))

    # Filter data berdasarkan tahun yang dipilih
    df_year = df[df["Year"] == selected_year]

    # Pilih negara pembanding (selain yang dipilih)
    comparison_options = [c for c in df_year["Country"].unique() if c != selected_country]
    comparison_country = st.selectbox(t["compare_with"], comparison_options)

    # Filter untuk 2 negara yang dipilih
    selected_countries = [selected_country, comparison_country]
    df_filtered = df_year[df_year["Country"].isin(selected_countries)]

    # Hitung rata-rata energi per kapita untuk tahun tersebut
    df_avg = df_filtered.groupby("Country")["Renewable_Per_Capita"].mean().reset_index()

    # Buat bar chart
    fig = px.bar(
        df_avg,
        x="Country",
        y="Renewable_Per_Capita",
        color="Country",
        title=t["title"].format(year=selected_year, a=selected_country, b=comparison_country)
    )
    fig.update_layout(
        xaxis_title=t["x_title"],
        yaxis_title=t["y_title"]
    )
    st.plotly_chart(fig, use_container_width=True)