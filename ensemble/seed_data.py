import sqlite3
# Chemin vers la base de données SQLite
SQLITE_PATH = "./data/base_stock.sqlite"

def insert_static_data():
    with sqlite3.connect(SQLITE_PATH) as conn:
        cur = conn.cursor()

        regions = [
            (1, "Île-de-France"),
            (2, "Occitanie"),
            (3, "Auvergne-Rhône-Alpes"),
            (4, "Bretagne")
        ]
        cur.executemany("INSERT INTO region VALUES (?, ?);", regions)

        revendeurs = [
            (1, "TechExpress", 1),
            (2, "ElectroZone", 1),
            (3, "SudTech", 2),
            (4, "GadgetShop", 2),
            (5, "Connectik", 3),
            (6, "Domotik+", 3),
            (7, "BreizhTech", 4),
            (8, "SmartBretagne", 4),
            (9, "HighNord", 1),
            (10, "OuestConnect", 4)
        ]
        cur.executemany("INSERT INTO revendeur VALUES (?, ?, ?);", revendeurs)

        produits = [
            (101, "Casque Bluetooth", 59.90),
            (102, "Chargeur USB-C", 19.90),
            (103, "Enceinte Portable", 89.90),
            (104, "Batterie Externe", 24.90),
            (105, "Montre Connectée", 129.90),
            (106, "Webcam HD", 49.90),
            (107, "Hub USB 3.0", 34.90),
            (108, "Clavier sans fil", 44.90),
            (109, "Souris ergonomique", 39.90),
            (110, "Station d'accueil", 109.90)
        ]
        cur.executemany("INSERT INTO produit VALUES (?, ?, ?);", produits)

        production = [
            (101, 50, "2025-07-01"),
            (102, 80, "2025-07-01"),
            (103, 40, "2025-07-02"),
            (104, 60, "2025-07-02"),
            (105, 20, "2025-07-03"),
            (106, 35, "2025-07-03"),
            (107, 25, "2025-07-04"),
            (108, 30, "2025-07-04"),
            (109, 45, "2025-07-05"),
            (110, 15, "2025-07-05")
        ]
        cur.executemany("INSERT INTO production (product_id, quantity, date_production) VALUES (?, ?, ?);", production)

        types_evenement = [
            (1, "Réapprovisionnement"),
            (2, "Commande client")
        ]
        cur.executemany("INSERT OR IGNORE INTO type_evenement VALUES (?, ?);", types_evenement)

        conn.commit()
        print(" Données statiques insérées.")
