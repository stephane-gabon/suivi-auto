"""
export_utils.py
Génération de rapports PDF (ReportLab) et Excel (OpenPyXL / Pandas)
pour les entretiens, coûts et consommation de carburant.
"""

import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)

import pandas as pd

from database import (
    lister_vehicules, lister_entretiens, lister_pleins,
    consommation_moyenne, cout_total_par_categorie, get_parametre
)

EXPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

BLEU_APPLE = colors.HexColor("#0071E3")
GRIS_CLAIR = colors.HexColor("#F5F5F7")


def _devise():
    return get_parametre("devise", "FCFA")


def _nom_fichier(prefixe, extension):
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(EXPORT_DIR, f"{prefixe}_{horodatage}.{extension}")


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------

def generer_rapport_pdf(vehicule_id=None, date_debut=None, date_fin=None):
    """
    Génère un rapport PDF récapitulatif : entretiens, coûts par catégorie,
    et consommation carburant, pour un véhicule (ou tous) sur une période.
    Retourne le chemin du fichier généré.
    """
    devise = _devise()
    chemin = _nom_fichier("rapport", "pdf")
    doc = SimpleDocTemplate(chemin, pagesize=A4,
                             topMargin=1.5 * cm, bottomMargin=1.5 * cm)
    styles = getSampleStyleSheet()
    titre_style = ParagraphStyle(
        "TitrePrincipal", parent=styles["Title"], textColor=BLEU_APPLE
    )
    elements = []

    vehicules = lister_vehicules()
    if vehicule_id:
        vehicules = [v for v in vehicules if v["id"] == vehicule_id]

    elements.append(Paragraph("Rapport de suivi automobile", titre_style))
    texte_fin = date_fin or "aujourd'hui"
    periode = f"{date_debut or 'début'} → {texte_fin}"
    elements.append(Paragraph(f"Période : {periode}", styles["Normal"]))
    elements.append(Spacer(1, 0.5 * cm))

    for v in vehicules:
        elements.append(Paragraph(
            f"{v['nom']} ({v.get('marque', '')} {v.get('modele', '')})",
            styles["Heading2"]
        ))

        # Tableau des entretiens
        entretiens = lister_entretiens(v["id"], date_debut, date_fin)
        data = [["Date", "Catégorie", "Kilométrage", f"Coût ({devise})"]]
        total_entretien = 0
        for e in entretiens:
            data.append([e["date_entretien"], e["categorie"],
                         f"{e['kilometrage']:,} km".replace(",", " "),
                         f"{e['cout']:,.0f}".replace(",", " ")])
            total_entretien += e["cout"]
        data.append(["", "", "TOTAL", f"{total_entretien:,.0f}".replace(",", " ")])

        table = Table(data, colWidths=[3 * cm, 4 * cm, 4 * cm, 4 * cm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BLEU_APPLE),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, -1), (-1, -1), GRIS_CLAIR),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3 * cm))

        # Consommation carburant
        conso = consommation_moyenne(v["id"])
        pleins = lister_pleins(v["id"])
        total_carburant = sum(p["prix_total"] for p in pleins)
        texte_conso = (
            f"Consommation moyenne : {conso} L/100km" if conso
            else "Consommation moyenne : données insuffisantes"
        )
        elements.append(Paragraph(texte_conso, styles["Normal"]))
        elements.append(Paragraph(
            f"Total dépensé en carburant : {total_carburant:,.0f} {devise}".replace(",", " "),
            styles["Normal"]
        ))
        elements.append(Spacer(1, 0.8 * cm))

    doc.build(elements)
    return chemin


# ---------------------------------------------------------------------------
# EXCEL
# ---------------------------------------------------------------------------

def generer_rapport_excel(vehicule_id=None, date_debut=None, date_fin=None):
    """
    Génère un classeur Excel avec plusieurs feuilles :
    Entretiens, Carburant, Synthèse par catégorie.
    Retourne le chemin du fichier généré.
    """
    chemin = _nom_fichier("rapport", "xlsx")

    entretiens = lister_entretiens(vehicule_id, date_debut, date_fin)
    pleins = lister_pleins(vehicule_id)
    synthese = cout_total_par_categorie(vehicule_id, date_debut, date_fin)

    df_entretiens = pd.DataFrame(entretiens) if entretiens else pd.DataFrame(
        columns=["vehicule_id", "categorie", "date_entretien", "kilometrage", "cout"]
    )
    df_carburant = pd.DataFrame(pleins) if pleins else pd.DataFrame(
        columns=["vehicule_id", "date_plein", "litres", "prix_total", "kilometrage"]
    )
    df_synthese = pd.DataFrame(
        list(synthese.items()), columns=["Catégorie", "Coût total"]
    )

    with pd.ExcelWriter(chemin, engine="openpyxl") as writer:
        df_entretiens.to_excel(writer, sheet_name="Entretiens", index=False)
        df_carburant.to_excel(writer, sheet_name="Carburant", index=False)
        df_synthese.to_excel(writer, sheet_name="Synthese", index=False)

    _mettre_en_forme_excel(chemin)
    return chemin


def _mettre_en_forme_excel(chemin):
    """Applique une mise en forme simple (en-têtes en bleu) au classeur généré."""
    from openpyxl import load_workbook
    from openpyxl.styles import Font, PatternFill

    wb = load_workbook(chemin)
    entete_fill = PatternFill(start_color="0071E3", end_color="0071E3", fill_type="solid")
    entete_font = Font(color="FFFFFF", bold=True)

    for feuille in wb.sheetnames:
        ws = wb[feuille]
        for cell in ws[1]:
            cell.fill = entete_fill
            cell.font = entete_font
        for colonne in ws.columns:
            largeur_max = max((len(str(c.value)) for c in colonne if c.value is not None), default=10)
            ws.column_dimensions[colonne[0].column_letter].width = min(largeur_max + 2, 30)

    wb.save(chemin)
