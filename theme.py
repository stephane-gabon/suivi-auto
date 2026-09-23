"""
theme.py
Constantes de style partagées par toute l'application, pour un rendu
inspiré du site Apple : typographie sobre, palette blanc / gris clair / bleu.
"""

# Couleurs (RGBA, 0-1)
BLANC = (1, 1, 1, 1)
GRIS_CLAIR = (0.96, 0.96, 0.97, 1)
GRIS_MOYEN = (0.55, 0.55, 0.58, 1)
GRIS_FONCE = (0.2, 0.2, 0.22, 1)
BLEU = (0, 0.44, 0.89, 1)          # #0071E3
BLEU_FONCE = (0, 0.32, 0.65, 1)
ROUGE_ALERTE = (0.9, 0.25, 0.2, 1)
VERT_OK = (0.2, 0.72, 0.4, 1)

# Typographie : on retombe sur Roboto (fournie avec Kivy) si San Francisco
# n'est pas installée sur le système - garantit un rendu cohérent partout.
POLICE_PRINCIPALE = "Roboto"

TAILLE_TITRE = "22sp"
TAILLE_SOUS_TITRE = "16sp"
TAILLE_TEXTE = "14sp"
TAILLE_PETIT = "12sp"

ESPACEMENT = "12dp"
RAYON_COIN = [14]
