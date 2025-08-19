import sqlite3               
import pandas as pd          

# Chemin vers la base de données SQLite
SQLITE_PATH = "./data/base_stock.sqlite"

def analyser_et_exporter_stock(output_filename="etat_stock_par_produit.csv"):
    

    # Variable pour le chemin de sortie du fichier CSV
    output_path = "/home/mathieu/Dropbox/Distributech/Etat des stocks/" + output_filename


    # Ouvre une connexion à la bdd SQLite
    with sqlite3.connect(SQLITE_PATH) as conn:
        # Requête SQL : pour chaque produit, on récupère son ID, son nom,
        # et la somme des quantités en stock (si aucune entrée dans `stock`, le produit apparaîtra quand même)
        query = """
        SELECT 
            p.product_id,
            p.product_name,
            SUM(s.quantity) AS stock_disponible
        FROM produit p
        LEFT JOIN stock s ON p.product_id = s.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY p.product_id;
        """
        # Exécute la requête SQL et charge le résultat dans un DataFrame pandas
        df = pd.read_sql_query(query, conn)

    # Affiche le tableau en console, sans l'index de pandas
    print("\n État actuel du stock par produit :\n")
    print(df.to_string(index=False))

    # Exporte le DataFrame en CSV dans le chemin `output_path`, sans index
    df.to_csv(output_path, index=False)
    print(f"\n Fichier CSV exporté : {output_path}")


if __name__ == "__main__":
    analyser_et_exporter_stock()
