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

# Kombinirani input za pretragu (šifra, naziv ili dimenzija/model)
search_input = st.text_input("Pretraži prema šifri, nazivu ili dimenziji/modelu", "")

# Provjera ako je datoteka učitana
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
        # Uklanjanje nepotrebnih razmaka iz naziva kolona
        df.columns = df.columns.str.strip()

        # Putanje do slika i logotipa
        photo_base_path = r"\\SRV-TS01\Svasta\Italcro\Photo"
        logo_base_path = r"\\SRV-TS01\Svasta\Tehnika\EasyKatalog\Logotipi"

        # Zamjena NaN s praznim stringovima
        df.fillna("", inplace=True)

        # Pretvorba kolona u stringove
        df['Šifra'] = df['Šifra'].astype(str)
        df['Naziv'] = df['Naziv'].astype(str)
        df['Dimenzija/Model'] = df['Dimenzija/Model'].astype(str)

        # Čišćenje razmaka i nevidljivih znakova u kolonama 'Šifra', 'Naziv' i 'Dimenzija/Model'
        df['Šifra'] = df['Šifra'].str.strip()
        df['Naziv'] = df['Naziv'].str.strip()
        df['Dimenzija/Model'] = df['Dimenzija/Model'].str.strip()

        # Filtriranje prema unesenom tekstu (šifra, naziv ili dimenzija/model)
        if search_input:
            df = df[df['Šifra'].str.contains(search_input, case=False, na=False) |
                    df['Naziv'].str.contains(search_input, case=False, na=False) |
                    df['Dimenzija/Model'].str.contains(search_input, case=False, na=False)]

        # Filtriranje dupliciranih proizvoda prema 'Šifra' i 'Naziv'
        df = df.drop_duplicates(subset=["Šifra", "Naziv"], keep="first")

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

                # Zaokruživanje cijene na 2 decimale i dodavanje €
                try:
                    cijena = round(float(cijena), 2)
                except ValueError:
                    cijena = cijena  # Ako cijena nije broj, ostavi originalnu vrijednost

                # Ispis cijene sa znakom €
                cijena_str = f"{cijena} €" if isinstance(cijena, float) else cijena

                # Ispis svih informacija za svaki proizvod
                sifre_html += f"<div style='background-color: white;'><strong>Šifra:</strong> {sifra} | " \
                              f"<strong>Model:</strong> {dimenzija} | " \
                              f"<strong>Pakiranje:</strong> {pakiranje} | " \
                              f"<strong>VPC:</strong> {cijena_str}</div><br>"

                # Dodavanje novih podataka u sifre_html
                sifre_html += f"<div style='background-color: #ff66cc; color: white;'><strong>Rabat:</strong> {row['Rabat']} | " \
                              f"<strong>Rabat A:</strong> {row['RabatA']} | " \
                              f"<strong>Predračun:</strong> {row['Predračun']} | " \
                              f"<strong>Netto:</strong> {row['Netto']} | " \
                              f"<strong>Količina 1:</strong> {row['Količina 1']} | " \
                              f"<strong>Rabat 1:</strong> {row['Rabat 1']} | " \
                              f"<strong>Količina 2:</strong> {row['Količina 2']} | " \
                              f"<strong>Rabat 2:</strong> {row['Rabat 2']} | " \
                              f"<strong>Količina 3:</strong> {row['Količina 3']} | " \
                              f"<strong>Rabat 3:</strong> {row['Rabat 3']}</div><br>"

            all_groups.append({
                "naziv": naziv,
                "podnaziv": podnaziv,
                "image": image_path if image_path and os.path.exists(image_path) else None,
                "sifre_html": sifre_html
            })

        # Dinamička veličina fonta prema broju kolona
        font_sizes = {
            1: ("18px", "16px"),
            2: ("16px", "14px"),
            3: ("14px", "12px"),
            4: ("12px", "10px"),
            5: ("10px", "8px"),
        }
        title_font, subtitle_font = font_sizes.get(num_columns, ("18px", "14px"))

        # Prikaz u kolone
        for i in range(0, len(all_groups), num_columns):
            cols = st.columns(num_columns)
            for j in range(num_columns):
                if i + j < len(all_groups):
                    group = all_groups[i + j]
                    with cols[j]:
                        # Ispisivanje naziva sa žutom pozadinom (smanjeni font)
                        st.markdown(
                            f"<div style='font-size:{title_font}; font-weight:bold; background-color: yellow'>{group['naziv']}</div>",
                            unsafe_allow_html=True
                        )
                        # Ispisivanje podnaziva
                        st.markdown(
                            f"<div style='font-size:{subtitle_font}; color:gray'>{group['podnaziv']}</div>",
                            unsafe_allow_html=True
                        )
                        if group['image']:
                            st.image(group['image'], width=189)  # cca 50mm
                        else:
                            st.write("Slika nije dostupna")  # Ako slika nije dostupna

                        # Ispisivanje sivo pozadinske boje za cijenu
                        sifre_html_siva = group['sifre_html'].replace("VPC: ",
                                                                      f"<span style='background-color: #f2f2f2;'>VPC:</span>")

                        st.markdown(
                            f"<div style='background-color: #f2f2f2;'>{sifre_html_siva}</div>",
                            unsafe_allow_html=True
                        )

                        # Promjena boje za Rabat, Rabat A, Predračun, Netto, Količina (Roza)
                        sifre_html_roza = group['sifre_html'].replace("Rabat: ",
                                                                      f"<span style='background-color: #ff66cc; color: white;'>Rabat:</span>") \
                            .replace("Rabat A:", f"<span style='background-color: #ff66cc; color: white;'>Rabat A:</span>") \
                            .replace("Predračun:", f"<span style='background-color: #ff66cc; color: white;'>Predračun:</span>") \
                            .replace("Netto:", f"<span style='background-color: #ff66cc; color: white;'>Netto:</span>") \
                            .replace("Količina", f"<span style='background-color: #ff66cc; color: white;'>Količina</span>")

                        st.markdown(
                            f"<div style='background-color: #f2f2f2;'>{sifre_html_roza}</div>",
                            unsafe_allow_html=True
                        )

                        # Dodaj razmak između proizvoda
                        st.markdown("<br>", unsafe_allow_html=True)
