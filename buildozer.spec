```ini
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

[buildozer]

log_level = 2
warn_on_root = 1

[android]

android.api = 33
android.minapi = 24

android.sdk = 33
android.ndk = 28c
android.ndk_api = 24

android.arch = arm64-v8a,armeabi-v7a

android.accept_android_sdk_license = True
android.enable_androidx = True
```
