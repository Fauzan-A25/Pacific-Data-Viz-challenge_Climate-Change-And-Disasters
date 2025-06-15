import streamlit as st
import plotly.express as px
import pandas as pd
from geopy.geocoders import Nominatim
import time

# Koordinat fallback untuk negara-negara Pasifik
FALLBACK_COORDS = {
    "Fiji": (-17.7134, 178.0650),
    "New Caledonia": (-22.2558, 166.4505),
    "Papua New Guinea": (-6.314993, 143.9555),
    "Solomon Islands": (-9.6457, 160.1562),
    "Vanuatu": (-15.3767, 166.9592),
    "Kiribati": (1.8709, -157.3630),
    "Marshall Islands": (7.1315, 171.1845),
    "Micronesia": (7.4256, 150.5508),
    "Nauru": (-0.5228, 166.9315),
    "Palau": (7.5149, 134.5825),
    "Cook Islands": (-21.2367, -159.7777),
    "Niue": (-19.0544, -169.8672),
    "French Polynesia": (-17.6797, -149.4068),
    "Tonga": (-21.1789, -175.1982),
    "Tuvalu": (-7.1095, 179.1943),
    "Samoa": (-13.7590, -172.1046)
}

@st.cache_data(show_spinner=False)
def get_coordinates_cached(countries):
    geolocator = Nominatim(user_agent="pacific-locator")
    coords = []
    for country in countries:
        lat, lon = None, None
        try:
            location = geolocator.geocode(country)
            if location:
                lat, lon = location.latitude, location.longitude
        except:
            pass
        if lat is None or lon is None:
            lat, lon = FALLBACK_COORDS.get(country, (None, None))
        coords.append({"Country": country, "Lat": lat, "Lon": lon})
        time.sleep(0.5)  # rate limit
    return pd.DataFrame(coords)

def show_interactive_map(df, selected_country, lang):
    # Kamus teks dua bahasa
    texts = {
        "Indonesia": {
            "spinner": "🛰️ Sedang mengambil dan memuat koordinat negara-negara Pasifik...",
            "error": "❌ Tidak ada koordinat yang berhasil diambil.",
            "title": "🌍 Lokasi Negara-Negara Pasifik",
            "success": "✅ Peta berhasil dimuat!",
            "caption": "🗺️ Peta ini menunjukkan lokasi negara-negara Pasifik dengan kapasitas energi terbarukan per kapita yang telah dipilih. "
                       "Negara yang dipilih ditandai dengan warna hijau, sedangkan negara lainnya berwarna abu-abu."
        },
        "English": {
            "spinner": "🛰️ Retrieving and loading coordinates of Pacific countries...",
            "error": "❌ No coordinates could be retrieved.",
            "title": "🌍 Locations of Pacific Countries",
            "success": "✅ Map successfully loaded!",
            "caption": "🗺️ This map shows the locations of Pacific countries with the selected per capita renewable energy capacity. "
                       "The selected country is marked in green, while the others are in gray."
        }
    }

    t = texts[lang]  # Shortcut for selected language

    countries = df['Country'].unique()

    with st.spinner(t["spinner"]):
        coords_df = get_coordinates_cached(countries)

    if coords_df['Lat'].isnull().all() or coords_df['Lon'].isnull().all():
        st.error(t["error"])
        return

    coords_df['Color'] = coords_df['Country'].apply(lambda x: "green" if x == selected_country else "lightgray")
    coords_df['Opacity'] = coords_df['Country'].apply(lambda x: 1.0 if x == selected_country else 0.3)

    nauru = coords_df[coords_df['Country'] == 'Nauru']
    if not nauru.empty:
        center_lat, center_lon = nauru.iloc[0][['Lat', 'Lon']]
    else:
        center_lat, center_lon = coords_df[['Lat', 'Lon']].mean()

    fig = px.scatter_geo(
        coords_df.dropna(subset=['Lat', 'Lon']),
        lat="Lat",
        lon="Lon",
        hover_name="Country",
        text="Country",
        scope="world",
        projection="orthographic",
        title=t["title"],
    )

    fig.update_traces(
        marker=dict(
            size=15,
            color=coords_df['Color'],
            opacity=coords_df['Opacity'],
            line=dict(width=2, color='darkgreen'),
            symbol='circle'
        ),
        selector=dict(mode='markers+text')
    )

    fig.update_layout(
        height=700,
        margin=dict(l=0, r=0, t=40, b=0),
        dragmode=False,
        hovermode='closest',
    )

    fig.update_geos(
        center=dict(lat=center_lat, lon=center_lon),
        projection=dict(
            type="orthographic",
            rotation=dict(
                lon=center_lon,
                lat=center_lat,
                roll=0
            )
        ),
        showcountries=True,
        showcoastlines=True,
        showland=True,
        landcolor="lightgray",
        countrycolor="black",
        coastlinecolor="darkslategray",
        showocean=True,
        oceancolor="lightblue",
        resolution=50,
    )

    st.success(t["success"])
    st.plotly_chart(fig, use_container_width=True)
    st.caption(t["caption"])

