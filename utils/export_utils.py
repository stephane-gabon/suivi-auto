"""
Utilitaires d'export pour l'application Suivi Auto.

Ce module gère uniquement l'export Excel.

La génération PDF a été supprimée volontairement afin de
simplifier la compilation Android avec Buildozer/python-for-android.
"""

from pathlib import Path
from datetime import datetime

import pandas as pd


# ================================================================
# RÉPERTOIRE DES EXPORTS
# ================================================================

EXPORT_DIR = Path("exports")

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
    Génère un fichier Excel.

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

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = (
        f"rapport_{timestamp}.xlsx"
    )

    output_path = EXPORT_DIR / filename


    # ------------------------------------------------------------
    # Données de base
    #
    # Cette partie peut être adaptée selon les données réellement
    # utilisées par l'application.
    # ------------------------------------------------------------

    data = {
        "Véhicule": [
            vehicule_id if vehicule_id is not None else ""
        ],
        "Date début": [
            date_debut if date_debut is not None else ""
        ],
        "Date fin": [
            date_fin if date_fin is not None else ""
        ],
    }


    dataframe = pd.DataFrame(data)


    # ------------------------------------------------------------
    # Création du fichier Excel
    # ------------------------------------------------------------

    dataframe.to_excel(
        output_path,
        index=False,
        engine="openpyxl",
    )


    return str(output_path)
