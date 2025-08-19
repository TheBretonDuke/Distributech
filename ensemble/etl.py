import sqlite3
import pandas as pd

# Chemin vers la base de données SQLite
SQLITE_PATH = "./data/base_stock.sqlite"
# Chemin vers le fichier CSV avec les commandes
CSV_PATH = "https://www.dropbox.com/scl/fi/srp2zfsbam0mr3v55io27/commande_revendeur_tech_express.csv?rlkey=ia505a1wt25dcsld9ppp94p47&st=8ekwtpvv&dl=1"


def run_etl():
    # Lire le fichier CSV avec pandas
    df = pd.read_csv(CSV_PATH)


    # Forcer les types des colonnes pour éviter les erreurs
    df['numero_commande'] = df['numero_commande'].astype(str)
    df['revendeur_id'] = df['revendeur_id'].astype(int)
    df['commande_date'] = df['commande_date'].astype(str)
    df['product_id'] = df['product_id'].astype(int)
    df['quantity'] = df['quantity'].astype(int)
    df['unit_price'] = df['unit_price'].astype(float)

    # Ouvrir une connexion à la base de données SQLite
    conn = sqlite3.connect(SQLITE_PATH)
    cur = conn.cursor()

    # Extraire les commandes uniques (sans doublons) du DataFrame
    commandes = df[['numero_commande', 'revendeur_id', 'commande_date']].drop_duplicates()

    # Insérer les commandes dans la table commande (évite les doublons avec INSERT OR IGNORE)
    for _, row in commandes.iterrows():
        cur.execute(
            "INSERT OR IGNORE INTO commande (numero_commande, revendeur_id, commande_date) VALUES (?, ?, ?)",
            (row['numero_commande'], row['revendeur_id'], row['commande_date'])
        )

    # Insérer chaque ligne de commande dans la table ligne_commande
    for _, row in df.iterrows():
        cur.execute(
            "INSERT INTO ligne_commande (numero_commande, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
            (row['numero_commande'], row['product_id'], row['quantity'], row['unit_price'])
        )

    # Ajouter le réapprovisionnement à partir de la table production dans la table stock
    cur.execute("""
        INSERT INTO stock (product_id, date_mouvement, quantity, id_type)
        SELECT product_id, date_production, quantity, 1 FROM production
    """)

    # Ajouter les sorties de stock (commandes) dans la table stock (quantité négative)
    cur.execute("""
        INSERT INTO stock (product_id, date_mouvement, quantity, id_type)
        SELECT lc.product_id, c.commande_date, -lc.quantity, 2
        FROM ligne_commande lc
        JOIN commande c ON lc.numero_commande = c.numero_commande
    """)

    # Valider (commit) toutes les modifications dans la base de données
    conn.commit()
    # Fermer la connexion à la base
    conn.close()

    print("Données CSV intégrées et stock mis à jour.")
