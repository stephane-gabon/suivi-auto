[app]

title = Suivi Auto
package.name = suivi_auto
package.domain = org.suiviauto

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt,ttf,otf

version = 1.0

requirements = python3,kivy,plyer,openpyxl,pandas,reportlab

orientation = portrait

fullscreen = 0


[buildozer]

log_level = 2
warn_on_root = 1


[app:android]

android.api = 33
android.minapi = 24
android.sdk_build_tools = 35.0.0
android.ndk = 28c
android.archs = arm64-v8a,armeabi-v7a

p4a.local_recipes = p4a-recipes

