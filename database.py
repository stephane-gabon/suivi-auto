"""
database.py
Couche d'accès aux données (SQLite) pour l'application de suivi automobile.
Gère : véhicules, entretiens, pleins de carburant, factures (photos).
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "car_maintenance.db")

# Catégories d'entretien par défaut + intervalle recommandé (km) et (mois)
CATEGORIES_ENTRETIEN = [
    ("Vidange", 5000, 6),
    ("Freins", 20000, 12),
    ("Pneus", 40000, 24),
    ("Suspension", 30000, 24),
    ("Filtre à air", 15000, 12),
    ("Courroie de distribution", 60000, 48),
    ("Contrôle technique", None, 12),
    ("Autre", None, None),
]


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Crée les tables si elles n'existent pas déjà."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS vehicules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            marque TEXT,
            modele TEXT,
            immatriculation TEXT,
            annee INTEGER,
            kilometrage_actuel INTEGER DEFAULT 0,
            date_creation TEXT DEFAULT (datetime('now'))
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS entretiens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicule_id INTEGER NOT NULL,
            categorie TEXT NOT NULL,
            date_entretien TEXT NOT NULL,
            kilometrage INTEGER NOT NULL,
            cout REAL NOT NULL DEFAULT 0,
            note TEXT,
            photo_facture TEXT,
            prochain_km INTEGER,
            prochaine_date TEXT,
            FOREIGN KEY (vehicule_id) REFERENCES vehicules(id) ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS carburant (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicule_id INTEGER NOT NULL,
            date_plein TEXT NOT NULL,
            litres REAL NOT NULL,
            prix_total REAL NOT NULL,
            kilometrage INTEGER NOT NULL,
            plein_complet INTEGER DEFAULT 1,
            FOREIGN KEY (vehicule_id) REFERENCES vehicules(id) ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS parametres (
            cle TEXT PRIMARY KEY,
            valeur TEXT
        )
    """)
    cur.execute("INSERT OR IGNORE INTO parametres (cle, valeur) VALUES ('devise', 'FCFA')")

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# VEHICULES
# ---------------------------------------------------------------------------

def ajouter_vehicule(nom, marque="", modele="", immatriculation="", annee=None, kilometrage_actuel=0):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO vehicules (nom, marque, modele, immatriculation, annee, kilometrage_actuel)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (nom, marque, modele, immatriculation, annee, kilometrage_actuel),
    )
    conn.commit()
    vid = cur.lastrowid
    conn.close()
    return vid


def modifier_vehicule(vehicule_id, **champs):
    if not champs:
        return
    conn = get_connection()
    cur = conn.cursor()
    sets = ", ".join(f"{k} = ?" for k in champs)
    valeurs = list(champs.values()) + [vehicule_id]
    cur.execute(f"UPDATE vehicules SET {sets} WHERE id = ?", valeurs)
    conn.commit()
    conn.close()


def supprimer_vehicule(vehicule_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM vehicules WHERE id = ?", (vehicule_id,))
    conn.commit()
    conn.close()


def lister_vehicules():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vehicules ORDER BY nom")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_vehicule(vehicule_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vehicules WHERE id = ?", (vehicule_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def maj_kilometrage_vehicule(vehicule_id, kilometrage):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE vehicules SET kilometrage_actuel = MAX(kilometrage_actuel, ?) WHERE id = ?",
        (kilometrage, vehicule_id),
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# ENTRETIENS
# ---------------------------------------------------------------------------

def ajouter_entretien(vehicule_id, categorie, date_entretien, kilometrage, cout,
                       note="", photo_facture=None, prochain_km=None, prochaine_date=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO entretiens
           (vehicule_id, categorie, date_entretien, kilometrage, cout, note, photo_facture, prochain_km, prochaine_date)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (vehicule_id, categorie, date_entretien, kilometrage, cout, note, photo_facture, prochain_km, prochaine_date),
    )
    conn.commit()
    eid = cur.lastrowid
    conn.close()
    maj_kilometrage_vehicule(vehicule_id, kilometrage)
    return eid


def modifier_entretien(entretien_id, **champs):
    if not champs:
        return
    conn = get_connection()
    cur = conn.cursor()
    sets = ", ".join(f"{k} = ?" for k in champs)
    valeurs = list(champs.values()) + [entretien_id]
    cur.execute(f"UPDATE entretiens SET {sets} WHERE id = ?", valeurs)
    conn.commit()
    conn.close()


def supprimer_entretien(entretien_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM entretiens WHERE id = ?", (entretien_id,))
    conn.commit()
    conn.close()


def lister_entretiens(vehicule_id=None, date_debut=None, date_fin=None):
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT * FROM entretiens WHERE 1=1"
    params = []
    if vehicule_id:
        query += " AND vehicule_id = ?"
        params.append(vehicule_id)
    if date_debut:
        query += " AND date_entretien >= ?"
        params.append(date_debut)
    if date_fin:
        query += " AND date_entretien <= ?"
        params.append(date_fin)
    query += " ORDER BY date_entretien DESC"
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def entretiens_a_venir():
    """Retourne les entretiens dont la prochaine échéance (km ou date) est proche."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.*, v.nom AS vehicule_nom, v.kilometrage_actuel
        FROM entretiens e
        JOIN vehicules v ON v.id = e.vehicule_id
        WHERE e.prochain_km IS NOT NULL OR e.prochaine_date IS NOT NULL
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    alertes = []
    aujourdhui = datetime.now().date()
    for r in rows:
        km_restant = None
        jours_restants = None
        if r["prochain_km"] is not None:
            km_restant = r["prochain_km"] - r["kilometrage_actuel"]
        if r["prochaine_date"]:
            try:
                d = datetime.strptime(r["prochaine_date"], "%Y-%m-%d").date()
                jours_restants = (d - aujourdhui).days
            except ValueError:
                pass

        proche = (km_restant is not None and km_restant <= 500) or \
                  (jours_restants is not None and jours_restants <= 14)
        if proche:
            r["km_restant"] = km_restant
            r["jours_restants"] = jours_restants
            alertes.append(r)
    return alertes


# ---------------------------------------------------------------------------
# CARBURANT
# ---------------------------------------------------------------------------

def ajouter_plein(vehicule_id, date_plein, litres, prix_total, kilometrage, plein_complet=True):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO carburant (vehicule_id, date_plein, litres, prix_total, kilometrage, plein_complet)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (vehicule_id, date_plein, litres, prix_total, kilometrage, int(plein_complet)),
    )
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    maj_kilometrage_vehicule(vehicule_id, kilometrage)
    return pid


def lister_pleins(vehicule_id=None):
    conn = get_connection()
    cur = conn.cursor()
    if vehicule_id:
        cur.execute("SELECT * FROM carburant WHERE vehicule_id = ? ORDER BY date_plein DESC", (vehicule_id,))
    else:
        cur.execute("SELECT * FROM carburant ORDER BY date_plein DESC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def consommation_moyenne(vehicule_id):
    """Calcule la consommation moyenne (L/100km) à partir des pleins complets successifs."""
    pleins = lister_pleins(vehicule_id)
    pleins = sorted(pleins, key=lambda p: p["kilometrage"])
    pleins_complets = [p for p in pleins if p["plein_complet"]]
    if len(pleins_complets) < 2:
        return None

    total_litres = sum(p["litres"] for p in pleins_complets[1:])
    distance = pleins_complets[-1]["kilometrage"] - pleins_complets[0]["kilometrage"]
    if distance <= 0:
        return None
    return round((total_litres / distance) * 100, 2)


# ---------------------------------------------------------------------------
# RAPPORTS / STATISTIQUES
# ---------------------------------------------------------------------------

def cout_total_par_categorie(vehicule_id=None, date_debut=None, date_fin=None):
    entretiens = lister_entretiens(vehicule_id, date_debut, date_fin)
    resultats = {}
    for e in entretiens:
        resultats[e["categorie"]] = resultats.get(e["categorie"], 0) + e["cout"]
    return resultats


def cout_total_par_vehicule(date_debut=None, date_fin=None):
    entretiens = lister_entretiens(None, date_debut, date_fin)
    pleins = lister_pleins()
    resultats = {}
    for e in entretiens:
        resultats.setdefault(e["vehicule_id"], {"entretiens": 0, "carburant": 0})
        resultats[e["vehicule_id"]]["entretiens"] += e["cout"]
    for p in pleins:
        if date_debut and p["date_plein"] < date_debut:
            continue
        if date_fin and p["date_plein"] > date_fin:
            continue
        resultats.setdefault(p["vehicule_id"], {"entretiens": 0, "carburant": 0})
        resultats[p["vehicule_id"]]["carburant"] += p["prix_total"]
    return resultats


# ---------------------------------------------------------------------------
# PARAMETRES
# ---------------------------------------------------------------------------

def get_parametre(cle, defaut=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT valeur FROM parametres WHERE cle = ?", (cle,))
    row = cur.fetchone()
    conn.close()
    return row["valeur"] if row else defaut


def set_parametre(cle, valeur):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO parametres (cle, valeur) VALUES (?, ?)", (cle, valeur))
    conn.commit()
    conn.close()
