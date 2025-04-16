import streamlit as st
import pandas as pd
from PIL import Image
import os

st.title("Pregled proizvoda")

# Učitavanje CSV datoteke
upload_file = st.file_uploader("Izaberi CSV fajl", type="csv")

# Odabir delimiter-a
delimiter = st.selectbox("Izaberi delimiter", [",", ";", "\t", "|"], index=0)

# Slider za broj kolona
num_columns = st.slider("Broj kolona za prikaz proizvoda", min_value=1, max_value=5, value=2)

if upload_file is not None:
    st.write("Datoteka uploadana")

    success = False
    for encoding in ["utf-8", "utf-8-sig", "cp1252", "latin1"]:
        upload_file.seek(0)
        try:
            # Pokušaj učitati datoteku s različitim encodingovima
            df = pd.read_csv(upload_file, encoding=encoding, delimiter=delimiter)
            st.success(f"Učitano sa encoding-om: {encoding}")
            success = True
            break
        except Exception as e:
            continue

    if not success:
        st.error("Provjeri delimiter i encoding.")
    else:
        # Zamjena specijalnih znakova u koloni 'Naziv'
        df['Naziv'] = df['Naziv'].str.replace('Æ', 'Ć')  # Zamjena neispravnih znakova, npr. 'Æ' sa 'Ć'

        # Putanje do slika i logotipa
        photo_base_path = r"\\SRV-TS01\Svasta\Italcro\Photo"
        logo_base_path = r"\\SRV-TS01\Svasta\Tehnika\EasyKatalog\Logotipi"

        # Zamjena NaN s praznim stringovima
        df.fillna("", inplace=True)

        # Grupiranje po putanji slike
        grouped = df.groupby('Slika')

        # Priprema podataka za prikaz
        all_groups = []
        for slika, group in grouped:
            naziv = group.iloc[0]['Naziv']
            podnaziv = group.iloc[0]['PodNaziv']
            image_path = os.path.join(photo_base_path, slika) if isinstance(slika, str) else None

            sifre_html = ""
            for _, row in group.iterrows():
                sifra = row['Šifra']
                dimenzija = row['Dimenzija/Model']
                pakiranje = row['Pakiranje']
                cijena = row['Cijena VPC']
                rabat = row['Rabat']
                rabat_a = row['RabatA']
                predračun = row['Predračun']
                netto = row['Netto']
                kolicina_1 = row['Količina 1']
                rabat_1 = row['Rabat 1']
                kolicina_2 = row['Količina 2']
                rabat_2 = row['Rabat 2']
                kolicina_3 = row['Količina 3']
                rabat_3 = row['Rabat 3']

                # Funkcija za formatiranje s dvije decimale
                def format_value(value):
                    try:
                        value = float(str(value).replace(',', '.'))  # Zamjena ',' s '.' u cijeni
                        return f"{value:.2f}"  # Zaokruživanje na 2 decimale
                    except ValueError:
                        return value  # Ako nije broj, vrati originalnu vrijednost

                # Formatiranje cijene i drugih numeričkih vrijednosti
                cijena_str = f"{format_value(cijena)} €"
                rabat_str = f"{format_value(rabat)}"
                rabat_a_str = f"{format_value(rabat_a)}"
                predračun_str = f"{format_value(predračun)}"
                netto_str = f"{format_value(netto)}"
                kolicina_1_str = f"{format_value(kolicina_1)}"
                rabat_1_str = f"{format_value(rabat_1)}"
                kolicina_2_str = f"{format_value(kolicina_2)}"
                rabat_2_str = f"{format_value(rabat_2)}"
                kolicina_3_str = f"{format_value(kolicina_3)}"
                rabat_3_str = f"{format_value(rabat_3)}"

                # Ispis svih informacija za svaki proizvod
                sifre_html += f"Šifra: {sifra} | Model: {dimenzija} | Pakiranje: {pakiranje} | VPC: {cijena_str} <br>"

                # Dodavanje novih podataka u sifre_html
                sifre_html += f"Rabat: {rabat_str} | Rabat A: {rabat_a_str} | Predračun: {predračun_str} | Netto: {netto_str} | " \
                              f"Količina 1: {kolicina_1_str} | Rabat 1: {rabat_1_str} | Količina 2: {kolicina_2_str} | " \
                              f"Rabat 2: {rabat_2_str} | Količina 3: {kolicina_3_str} | Rabat 3: {rabat_3_str}<br>"

            all_groups.append({
                "naziv": naziv,
                "podnaziv": podnaziv,
                "image": image_path if image_path and os.path.exists(image_path) else None,
                "sifre_html": sifre_html
            })

        # Dinamička veličina fonta prema broju kolona
        font_sizes = {
            1: ("24px", "18px"),
            2: ("22px", "16px"),
            3: ("20px", "14px"),
            4: ("18px", "13px"),
            5: ("16px", "12px"),
        }
        title_font, subtitle_font = font_sizes.get(num_columns, ("18px", "14px"))

        # Prikaz u kolone
        for i in range(0, len(all_groups), num_columns):
            cols = st.columns(num_columns)
            for j in range(num_columns):
                if i + j < len(all_groups):
                    group = all_groups[i + j]
                    with cols[j]:
                        st.markdown(
                            f"<div style='font-size:{title_font}; font-weight:bold'>{group['naziv']}</div>",
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"<div style='font-size:{subtitle_font}; color:gray'>{group['podnaziv']}</div>",
                            unsafe_allow_html=True
                        )
                        if group['image']:
                            st.image(group['image'], width=189)  # cca 50mm
                        else:
                            st.write("Slika nije dostupna")  # Ako slika nije dostupna
                        st.markdown(group['sifre_html'], unsafe_allow_html=True)
