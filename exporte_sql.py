import sqlite3
from pathlib import Path

# Chemin absolu vers la base
db_path = Path(__file__).parent /"data" / "base_stock.sqlite"
export_path = Path(__file__).parent /"data" / "export_base.sql"

print(f"Base : {db_path.resolve()}")  # debug
print(f"Export : {export_path.resolve()}")  # debug

# Connexion et export
conn = sqlite3.connect(db_path)
with open(export_path, "w", encoding="utf-8") as f:
    for line in conn.iterdump():
        f.write(f"{line}\n")

conn.close()
print(f"Export terminé : {export_path}")

