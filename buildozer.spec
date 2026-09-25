[app]

# ==========================================================
# IDENTITÉ DE L'APPLICATION
# ==========================================================

# Nom affiché de l'application.
title = Suivi Auto

# Nom technique du package Android.
package.name = suivi_auto

# Domaine utilisé pour construire l'identifiant Android.
package.domain = org.suiviauto


# ==========================================================
# CODE SOURCE
# ==========================================================

# Répertoire contenant main.py.
source.dir = .

# Extensions incluses dans l'APK.
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt,ttf,otf

# Version de l'application.
version = 1.0


# ================================================================
# DÉPENDANCES PYTHON POUR ANDROID
# ================================================================
#
# Python 3.10.11 est imposé à la fois pour :
#
#   - python3      : Python embarqué dans l'application Android ;
#   - hostpython3  : Python utilisé pour construire les modules
#                    Python pendant la compilation.
#
# Les deux versions DOIVENT être identiques.
#
# OpenPyXL est utilisé directement pour la génération des fichiers
# Excel. Pandas n'est donc plus nécessaire.
# ================================================================

requirements = python3==3.10.11,hostpython3==3.10.11,kivy,plyer,openpyxl


# ==========================================================
# INTERFACE
# ==========================================================

# Orientation verticale.
orientation = portrait

# L'application n'est pas en plein écran.
fullscreen = 0


# ==========================================================
# ANDROID
# ==========================================================
#
# IMPORTANT :
# Ces paramètres doivent être directement dans [app].
# Il ne faut PAS créer une section [app:android].
# ==========================================================

# Version de l'API Android utilisée pour compiler.
android.api = 33

# Version minimale d'Android supportée.
android.minapi = 24

# Version des Build Tools.
android.sdk_build_tools = 34.0.0

# Version NDK demandée par Buildozer/p4a.
#
# Le SDK installé par le workflow contient :
# ndk;28.2.13676358
#
# Buildozer utilise ici son alias compatible :
# 28c
android.ndk = 28c

# Répertoire du SDK Android préparé par GitHub Actions.
#
# Le workflow installe le SDK dans .android-sdk
# à la racine du dépôt.
android.sdk_path = .android-sdk

# Répertoire du NDK.
#
# Il se trouve dans le SDK Android :
# .android-sdk/ndk/28.2.13676358
#
# On laisse Buildozer/p4a le déterminer à partir
# de la version android.ndk.
#
# Pas de p4a.local_recipes : ReportLab a été supprimé.


# ==========================================================
# ARCHITECTURES
# ==========================================================

# ARM64 + ARMv7.
android.archs = arm64-v8a,armeabi-v7a


# ==========================================================
# MISE À JOUR DU SDK
# ==========================================================
#
# Le workflow installe explicitement les composants
# nécessaires avant de lancer Buildozer.
#
# On demande donc à Buildozer de ne pas tenter de
# rechercher/installer arbitrairement une autre version
# des composants du SDK.
# ==========================================================

android.skip_update = 1


# ==========================================================
# PYTHON-FOR-ANDROID
# ==========================================================
#
# Utilisation du checkout p4a préparé et corrigé par GitHub Actions.
#
# Le workflow place le code p4a dans :
#
#   .p4a/
#
# afin de contrôler précisément son comportement et son pip interne.
# ================================================================

p4a.source_dir = .p4a

# Bootstrap Kivy/SDL2 standard.
p4a.bootstrap = sdl2


[buildozer]

# Niveau de journalisation.
log_level = 2

# Autorise l'exécution avec l'utilisateur root si nécessaire.
warn_on_root = 1
