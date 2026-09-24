[app]

# Nom de l'application

title = Suivi Auto

# Identifiant Android

package.name = suivi_auto
package.domain = org.stephane

# Code source

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt,csv

# Version

version = 0.1

# Dépendances Python

requirements = python3,kivy,plyer,openpyxl,pandas,reportlab

# Orientation

orientation = portrait

# Pas de plein écran

fullscreen = 0

# Icône

icon.filename = %(source.dir)s/icon.png

# Permissions Android

android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,POST_NOTIFICATIONS

[buildozer]

# Niveau de logs

log_level = 2

# Ne pas exécuter Buildozer en root

warn_on_root = 1

[android]

# ============================================================

# ANDROID SDK

# ============================================================

# API utilisée pour compiler

android.api = 33

# API minimale supportée par l'application

android.minapi = 24

# SDK

android.sdk = 33

# ============================================================

# ANDROID NDK

# ============================================================

# Utiliser le NDK déjà présent dans ton environnement

android.ndk = 28c

# API NDK minimale

android.ndk_api = 24

# ============================================================

# ARCHITECTURES

# ============================================================

android.arch = arm64-v8a,armeabi-v7a

# ============================================================

# OPTIONS DE BUILD

# ============================================================

android.accept_sdk_license = True

android.enable_androidx = True

android.add_src = src

android.entrypoint = org.kivy.android.PythonActivity

# ============================================================

# JAVA

# ============================================================

# Java 17 utilisé par le workflow

# ============================================================

# LOG

# ============================================================

p4a.branch = master
