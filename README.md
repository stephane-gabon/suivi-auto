# Suivi Auto — Application mobile de suivi d'entretien automobile

Application Kivy (Python) pour suivre l'entretien, le carburant et les coûts
de plusieurs véhicules, avec export PDF/Excel. Devise par défaut : **FCFA (XAF)**.

## Structure du projet

```
car_maintenance_app/
├── main.py                  # Point d'entrée, navigation par onglets
├── database.py               # Accès SQLite (véhicules, entretiens, carburant)
├── theme.py                   # Couleurs et typographie (style Apple)
├── car_maintenance.kv        # Styles des widgets Kivy
├── screens/
│   ├── home_screen.py         # Accueil : véhicules + alertes pop-up
│   ├── entretien_screen.py    # Entretiens : CRUD + photo de facture
│   ├── carburant_screen.py    # Carburant : pleins + consommation moyenne
│   ├── rapports_screen.py     # Rapports : coûts par catégorie + export
│   └── parametres_screen.py   # Paramètres : véhicules + devise
├── utils/
│   ├── export_utils.py        # Génération PDF (ReportLab) / Excel (OpenPyXL)
│   └── notification_utils.py  # Notifications push (Plyer) + logique d'alerte
├── exports/                   # Rapports générés (créé automatiquement)
└── requirements.txt
```

## Installation

```bash
python3 -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Lancement (bureau, pour développement/tests)

```bash
python main.py
```

## Génération d'un APK Android

Kivy seul ne suffit pas à empaqueter une app Android : utilisez **Buildozer**
(Linux/WSL recommandé) :

```bash
pip install buildozer
buildozer init          # crée buildozer.spec
# éditer buildozer.spec : title, package.name, requirements = python3,kivy,plyer,reportlab,openpyxl,pandas
buildozer -v android debug
```

Pour les notifications push et l'accès à la caméra/galerie sur Android,
ajoutez dans `buildozer.spec` :
```
android.permissions = CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, POST_NOTIFICATIONS
```

## Fonctionnalités livrées dans ce scaffold

- ✅ Gestion multi-véhicules (ajout/suppression, kilométrage)
- ✅ Entretiens : catégories prédéfinies, historique par véhicule, photo de facture
- ✅ Alertes automatiques (km restant ≤ 500, échéance ≤ 14 jours) avec pop-up + notification push
- ✅ Carburant : saisie des pleins, calcul de consommation moyenne (L/100km)
- ✅ Rapports : synthèse par catégorie (barres), filtres trimestre/semestre/année/tout
- ✅ Export PDF (ReportLab) et Excel (OpenPyXL/Pandas), dossier `exports/`
- ✅ Devise configurable (FCFA par défaut)
- ✅ Thème visuel sobre : blanc / gris clair / bleu, police Roboto

## Pistes d'amélioration (non incluses ici, à développer selon vos priorités)

- Compression/redimensionnement des photos de factures avant stockage
- Envoi des rapports par email (ex: via `smtplib` ou un service tiers)
- Graphiques plus riches (courbes d'évolution) avec `kivy_garden.graph` ou `matplotlib`
- Synchronisation cloud / sauvegarde de la base SQLite
- Authentification multi-utilisateurs si l'app est partagée
- Tests unitaires sur `database.py` et `export_utils.py`
