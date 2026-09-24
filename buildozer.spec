[app]

title = Suivi Auto
package.name = suivi_auto
package.domain = org.stephane

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt,csv

version = 0.1

requirements = python3,kivy,plyer,openpyxl,pandas,reportlab

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/icon.png

android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,POST_NOTIFICATIONS

# ------------------------------------------------------------

# Android

# ------------------------------------------------------------

android.api = 33
android.minapi = 24

# NDK r28c = 28.2.13676358

android.ndk = 28c
android.ndk_api = 24

# Chemins contrôlés par le workflow GitHub Actions

android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk
android.ndk_path = /home/runner/.buildozer/android/platform/android-sdk/ndk/28.2.13676358

# Ne pas laisser Buildozer essayer de mettre à jour

# automatiquement le SDK du runner.

android.skip_update = True

# Licence déjà acceptée dans GitHub Actions

android.accept_sdk_license = True

# AndroidX

android.enable_androidx = True

# Architectures

android.arch = arm64-v8a,armeabi-v7a

[buildozer]

log_level = 2
warn_on_root = 1
