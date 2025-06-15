import pandas as pd
import os
import streamlit as st

def clean_energy_data(input_path='data/raw_energy_data.csv'):
    # Pastikan file ada
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File tidak ditemukan: {input_path}")

    # Baca data mentah
    df = pd.read_csv(input_path)

    # Ambil hanya data dengan satuan WPC
    df_clean = df[df['UNIT_MEASURE'] == 'WPC'].copy()

    # Pilih kolom penting
    df_clean = df_clean[['GEO_PICT', 'TIME_PERIOD', 'OBS_VALUE', 'UNIT_MEASURE', 'DATA_SOURCE']]

    # Rename kolom
    df_clean.columns = ['Country', 'Year', 'Renewable_Per_Capita', 'Unit', 'Source']

    map_negara = {
        'FJ': 'Fiji',
        'NC': 'New Caledonia',
        'PG': 'Papua New Guinea',
        'SB': 'Solomon Islands',
        'VU': 'Vanuatu',
        'KI': 'Kiribati',
        'MH': 'Marshall Islands',
        'FM': 'Micronesia',
        'NR': 'Nauru',
        'PW': 'Palau',
        'CK': 'Cook Islands',
        'NU': 'Niue',
        'PF': 'French Polynesia',
        'TO': 'Tonga',
        'TV': 'Tuvalu',
        'WS': 'Samoa',
    }

    # Filter tahun 2000–2020
    df_clean = df_clean[(df_clean['Year'] >= 2000) & (df_clean['Year'] <= 2020)]

    # Urutkan berdasarkan Year (dan bisa juga Country agar rapi)
    df_clean = df_clean.sort_values(by=['Year', 'Country']).reset_index(drop=True)

    df_clean['Country'] = df_clean['Country'].apply(lambda x: map_negara.get(x, x))  # Ganti kode negara dengan nama lengkap
    # Save df_clean ke csv di folder data
    output_path = 'data/cleaned_energy_data.csv'
    df_clean.to_csv(output_path, index=False)

    st.session_state.processed_data = df_clean