# Putanja do slika na GitHubu
github_image_base_url = "https://raw.githubusercontent.com/{korisničko_ime}/{repozitorij}/{branch}/Slike/"

# U pripremi podataka za prikaz, zamjena lokalne putanje za GitHub URL
for slika, group in grouped:
    naziv = group.iloc[0]['Naziv']
    podnaziv = group.iloc[0]['PodNaziv']

    # Kreiranje GitHub URL-a za sliku
    image_url = f"{github_image_base_url}{slika}" if isinstance(slika, str) else None

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
        "image": image_url if image_url else None,
        "sifre_html": sifre_html
    })
