"""
Utilitaires d'export pour l'application Suivi Auto.

Ce module gère uniquement l'export Excel.

La génération PDF a été supprimée volontairement afin de
simplifier la compilation Android avec Buildozer/python-for-android.

Pandas n'est volontairement pas utilisé :
OpenPyXL suffit pour générer directement les fichiers .xlsx
et évite une dépendance native lourde lors de la compilation Android.
"""

from pathlib import Path
from datetime import datetime

from openpyxl import Workbook


# ================================================================
# RÉPERTOIRE DES EXPORTS
# ================================================================

# Répertoire dans lequel les fichiers Excel seront enregistrés.
EXPORT_DIR = Path("exports")

# Création automatique du répertoire s'il n'existe pas encore.
EXPORT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ================================================================
# EXPORT EXCEL
# ================================================================

def generer_rapport_excel(
    vehicule_id=None,
    date_debut=None,
    date_fin=None,
):
    """
    Génère un fichier Excel contenant les informations du rapport.

    Les paramètres sont conservés afin de rester compatibles avec
    le reste de l'application.

    Parameters
    ----------
    vehicule_id : optional
        Identifiant du véhicule.

    date_debut : optional
        Date de début de la période.

    date_fin : optional
        Date de fin de la période.

    Returns
    -------
    str
        Chemin du fichier Excel créé.
    """

    # ------------------------------------------------------------
    # Nom du fichier
    # ------------------------------------------------------------

    # Génération d'un horodatage afin d'éviter d'écraser un
    # précédent rapport.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"rapport_{timestamp}.xlsx"

    output_path = EXPORT_DIR / filename


    # ------------------------------------------------------------
    # Création du classeur Excel
    # ------------------------------------------------------------

    # OpenPyXL permet de créer directement un fichier .xlsx
    # sans passer par Pandas.
    workbook = Workbook()

    # La feuille active est utilisée pour le rapport.
    worksheet = workbook.active

    # Nom explicite de la feuille.
    worksheet.title = "Rapport"


    # ------------------------------------------------------------
    # En-têtes
    # ------------------------------------------------------------

    worksheet.append(
        [
            "Véhicule",
            "Date début",
            "Date fin",
        ]
    )


    # ------------------------------------------------------------
    # Données
    # ------------------------------------------------------------

    worksheet.append(
        [
            vehicule_id if vehicule_id is not None else "",
            date_debut if date_debut is not None else "",
            date_fin if date_fin is not None else "",
        ]
    )


    # ------------------------------------------------------------
    # Ajustement de la largeur des colonnes
    # ------------------------------------------------------------

    # Ces largeurs rendent le fichier plus lisible lorsqu'il
    # est ouvert avec Excel ou LibreOffice.
    worksheet.column_dimensions["A"].width = 20
    worksheet.column_dimensions["B"].width = 20
    worksheet.column_dimensions["C"].width = 20


    # ------------------------------------------------------------
    # Enregistrement du fichier
    # ------------------------------------------------------------

    workbook.save(output_path)


    # ------------------------------------------------------------
    # Retour du chemin du fichier créé
    # ------------------------------------------------------------

    return str(output_path)
