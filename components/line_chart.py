import streamlit as st
import plotly.express as px

def show_line_chart(df, selected_country, lang):
    # Kamus teks untuk dua bahasa
    texts = {
        "Indonesia": {
            "title_chart": f"Kapasitas Terpasang Energi Terbarukan per Kapita di {selected_country}",
            "x_label": "Tahun",
            "y_label": "Kapasitas Terpasang (Watt per Kapita)",
            "tooltip_y": "Kapasitas (Watt/kapita)",
            "tooltip_x": "Tahun",
            "caption": "📌 Data menunjukkan **rata-rata tahunan** kapasitas listrik dari energi terbarukan yang telah dipasang per orang (dalam Watt per kapita).",
            "analysis_title": "Analisis Pertumbuhan Energi Terbarukan per Kapita",
            "section_title": "📈 Perkembangan Energi Terbarukan",
            "analysis_text": """
**New Caledonia** mencatat perkembangan tercepat dalam pemanfaatan energi terbarukan per kapita antara tahun 2000 hingga 2020. Dalam dua dekade, konsumsi energi terbarukan meningkat tajam dari 17,27 menjadi 283,29 watt per kapita, mencerminkan lonjakan sebesar 266,02 watt. Pertumbuhan ini menunjukkan keseriusan negara tersebut dalam melakukan transisi energi dan kemungkinan besar didukung oleh kebijakan serta investasi yang kuat di sektor energi bersih.

Sebaliknya, **Fiji** mengalami perkembangan paling lambat, bahkan menunjukkan kemunduran. Dari yang semula sebesar 130,39 watt per kapita pada tahun 2000, konsumsi energi terbarukannya turun menjadi nol pada tahun 2020. Penurunan drastis ini mengindikasikan adanya penurunan komitmen atau hambatan dalam pengembangan energi ramah lingkungan di negara tersebut.
"""
        },
        "English": {
            "title_chart": f"Installed Renewable Energy Capacity per Capita in {selected_country}",
            "x_label": "Year",
            "y_label": "Installed Capacity (Watts per Capita)",
            "tooltip_y": "Capacity (Watts/capita)",
            "tooltip_x": "Year",
            "caption": "📌 Data shows the **annual average** of installed renewable electricity capacity per person (in watts per capita).",
            "analysis_title": "Renewable Energy Growth Analysis per Capita",
            "section_title": "📈 Renewable Energy Development",
            "analysis_text": """
**New Caledonia** recorded the fastest growth in renewable energy use per capita between 2000 and 2020. Over two decades, renewable energy consumption surged from 17.27 to 283.29 watts per capita, a jump of 266.02 watts. This growth reflects the country's strong commitment to energy transition, likely supported by robust policy and investment in clean energy.

In contrast, **Fiji** showed the slowest progress, even declining. From an initial 130.39 watts per capita in 2000, its renewable energy consumption dropped to zero by 2020. This drastic decline indicates a reduced commitment or barriers in developing clean energy in the country.
"""
        }
    }

    t = texts[lang]  # shortcut

    # Filter berdasarkan negara yang dipilih
    filtered_df = df[df["Country"] == selected_country]

    # Agregasi rata-rata kapasitas per tahun
    agg_df = filtered_df.groupby("Year")["Renewable_Per_Capita"].mean().reset_index()

    # Buat grafik garis
    fig = px.line(
        agg_df,
        x="Year",
        y="Renewable_Per_Capita",
        title=t["title_chart"],
        markers=True,
        labels={
            "Renewable_Per_Capita": t["tooltip_y"],
            "Year": t["tooltip_x"]
        }
    )

    # Penyesuaian tampilan grafik
    fig.update_layout(
        legend_title_text='',
        xaxis_title=t["x_label"],
        yaxis_title=t["y_label"]
    )

    # Tampilkan grafik
    st.plotly_chart(fig, use_container_width=True)

    # Tambahkan keterangan
    st.caption(t["caption"])

    st.title(t["analysis_title"])
    st.subheader(t["section_title"])
    st.markdown(t["analysis_text"])
