import csv

def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        with open(file_path, "r", newline="", encoding="utf-8") as f:
            valori = []
            righe = csv.reader(f)
            next(righe) #salto intestazione

            for riga in righe:
                codice = riga[0]
                titolo = riga[1]
                autore = riga[2]
                mese = int(riga[3])
                anno = int(riga[4])  # parametri di ogni riga

                foto = [codice, titolo, autore, mese, anno]

                trovato = False
                for elemento in valori:
                    if elemento[0] == anno:
                        elemento[1].append(foto) # anno esistente: aggiungo la foto
                        trovato = True
                        break

                if not trovato:
                    valori.append([anno, [foto]]) # anno nuovo: lo creo

            return valori #ottengo una lista di liste
    except FileNotFoundError:
        return None

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    if mese < 1 or mese > 12:
        return None

    for elemento in album: # elemento è la coppia anno + lista foto (codice, ecc...)!!!
        for foto in elemento[1]: # scorro le foto singolarmente
            if foto[0] == codice:
                return None # dalla traccia
    try:
        nuova_foto = [codice, titolo, autore, mese, anno]
        with open(file_path, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(nuova_foto) # aggiungo nuova riga con nuova foto in fondo al file
    except FileNotFoundError:
        return None

    trovato = False
    for elemento in album:
        if elemento[0] == anno:
            elemento[1].append(nuova_foto) # anno esistente: aggiungo la nuova foto
            trovato = True
            break

    if not trovato:
        album.append([anno, [nuova_foto]]) # anno nuovo: lo creo (stesso ciclo di prima)

    return nuova_foto

def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for elemento in album:
        for foto in elemento[1]:
            if foto[0] == codice:
                return f"{foto[0]}, {foto[1]}, {foto[2]}, {foto[3]}, {foto[4]}"

    return None

def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    for elemento in album:
        if elemento[0] == anno:
            titoli = []

            for foto in elemento[1]: # aggiungo i titoli in una nuova lista e li ordino
                titoli.append(foto[1])
            titoli.sort()
            return titoli
    return None

def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")

if __name__ == "__main__":
    main()
