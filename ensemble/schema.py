import sqlite3
# Chemin vers la base de données SQLite
SQLITE_PATH = "./data/base_stock.sqlite"

def create_tables():
    with sqlite3.connect(SQLITE_PATH) as conn:
        cur = conn.cursor()
        cur.executescript("""
        -- Suppression des anciennes tables (si elles existent)
        DROP TABLE IF EXISTS stock;
        DROP TABLE IF EXISTS ligne_commande;
        DROP TABLE IF EXISTS commande;
        DROP TABLE IF EXISTS production;
        DROP TABLE IF EXISTS produit;
        DROP TABLE IF EXISTS revendeur;
        DROP TABLE IF EXISTS region;
        DROP TABLE IF EXISTS type_evenement;

        -- Tables régionales
        CREATE TABLE region (
            region_id INTEGER PRIMARY KEY,
            region_name TEXT NOT NULL
        );

        CREATE TABLE revendeur (
            revendeur_id INTEGER PRIMARY KEY,
            revendeur_name TEXT NOT NULL,
            region_id INTEGER NOT NULL,
            FOREIGN KEY (region_id) REFERENCES region(region_id)
        );

        -- Table produit
        CREATE TABLE produit (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            cout_unitaire REAL NOT NULL
        );

        -- Production (réapprovisionnement)
        CREATE TABLE production (
            production_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            date_production TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES produit(product_id)
        );

        -- Table commande (clé TEXT !)
        CREATE TABLE commande (
            numero_commande TEXT PRIMARY KEY,
            revendeur_id INTEGER NOT NULL,
            commande_date TEXT NOT NULL,
            FOREIGN KEY (revendeur_id) REFERENCES revendeur(revendeur_id)
        );

        -- Lignes de commande
        CREATE TABLE ligne_commande (
            id_ligne INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_commande TEXT NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (numero_commande) REFERENCES commande(numero_commande),
            FOREIGN KEY (product_id) REFERENCES produit(product_id)
        );

        -- Types de mouvements
        CREATE TABLE type_evenement (
            id_type INTEGER PRIMARY KEY,
            libelle_type TEXT UNIQUE
        );

        -- Mouvements de stock
        CREATE TABLE stock (
            id_stock INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            date_mouvement TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            id_type INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES produit(product_id),
            FOREIGN KEY (id_type) REFERENCES type_evenement(id_type)
        );
        """)
        conn.commit()
        print(" Tables créées avec succès.")
