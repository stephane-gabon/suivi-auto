[app]
title = Suivi Auto
package.name = suivi_auto
package.domain = org.stephane
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,plyer,reportlab,openpyxl,pandas
orientation = portrait
fullscreen = 0

# Permissions Android
android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,POST_NOTIFICATIONS

# Icône (optionnelle, ajoute ton fichier icon.png)
icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1

[android]
# SDK et NDK par défaut
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21
