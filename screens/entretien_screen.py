"""Écran Entretiens : ajout, historique et gestion des factures photo."""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.image import Image
from datetime import date

import theme
import database as db


class LigneEntretien(BoxLayout):
    def __init__(self, entretien, on_supprimer, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height="64dp",
                          padding="10dp", spacing="10dp", **kwargs)
        with self.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*theme.BLANC)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=theme.RAYON_COIN)
        self.bind(pos=self._maj_rect, size=self._maj_rect)

        infos = BoxLayout(orientation="vertical")
        infos.add_widget(Label(
            text=f"[b]{entretien['categorie']}[/b]  •  {entretien['date_entretien']}",
            markup=True, font_size=theme.TAILLE_TEXTE, color=theme.GRIS_FONCE,
            halign="left", text_size=(None, None)
        ))
        infos.add_widget(Label(
            text=f"{entretien['kilometrage']:,} km — {entretien['cout']:,.0f} FCFA".replace(",", " "),
            font_size=theme.TAILLE_PETIT, color=theme.GRIS_MOYEN, halign="left"
        ))
        self.add_widget(infos)

        bouton_suppr = Button(text="🗑", size_hint_x=None, width="44dp",
                               background_normal="", background_color=theme.GRIS_CLAIR,
                               color=theme.ROUGE_ALERTE)
        bouton_suppr.bind(on_release=lambda *_: on_supprimer(entretien["id"]))
        self.add_widget(bouton_suppr)

    def _maj_rect(self, *args):
        self._rect.pos = self.pos
        self._rect.size = self.size


class EntretienScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vehicule_selectionne_id = None
        self.chemin_photo_facture = None

        self.layout_principal = BoxLayout(orientation="vertical", padding="16dp", spacing="10dp")
        self.add_widget(self.layout_principal)
        self._construire_interface()

    def _construire_interface(self):
        self.layout_principal.clear_widgets()

        titre = Label(text="Entretiens", font_size=theme.TAILLE_TITRE, bold=True,
                       color=theme.GRIS_FONCE, size_hint_y=None, height="36dp", halign="left")
        titre.bind(size=lambda w, s: setattr(w, "text_size", s))
        self.layout_principal.add_widget(titre)

        vehicules = db.lister_vehicules()
        noms_vehicules = [v["nom"] for v in vehicules] or ["Aucun véhicule"]
        self.spinner_vehicule = Spinner(text=noms_vehicules[0], values=noms_vehicules,
                                         size_hint_y=None, height="44dp",
                                         background_color=theme.GRIS_CLAIR, color=theme.GRIS_FONCE)
        self.spinner_vehicule.bind(text=self._on_vehicule_change)
        self.layout_principal.add_widget(self.spinner_vehicule)
        if vehicules:
            self.vehicule_selectionne_id = vehicules[0]["id"]

        # Formulaire d'ajout rapide
        form = BoxLayout(orientation="vertical", spacing="6dp", size_hint_y=None, height="220dp")
        categories = [c[0] for c in db.CATEGORIES_ENTRETIEN]
        self.spinner_categorie = Spinner(text=categories[0], values=categories,
                                          size_hint_y=None, height="40dp",
                                          background_color=theme.GRIS_CLAIR, color=theme.GRIS_FONCE)
        self.champ_date = TextInput(text=str(date.today()), size_hint_y=None, height="40dp",
                                     hint_text="AAAA-MM-JJ")
        self.champ_km = TextInput(hint_text="Kilométrage", input_filter="int",
                                   size_hint_y=None, height="40dp")
        self.champ_cout = TextInput(hint_text="Coût (FCFA)", input_filter="float",
                                     size_hint_y=None, height="40dp")

        ligne_photo = BoxLayout(size_hint_y=None, height="40dp", spacing="6dp")
        self.label_photo = Label(text="Aucune photo de facture", color=theme.GRIS_MOYEN,
                                  font_size=theme.TAILLE_PETIT)
        bouton_photo = Button(text="📷 Ajouter", size_hint_x=None, width="120dp",
                               background_normal="", background_color=theme.GRIS_CLAIR,
                               color=theme.GRIS_FONCE)
        bouton_photo.bind(on_release=self._ouvrir_selecteur_photo)
        ligne_photo.add_widget(self.label_photo)
        ligne_photo.add_widget(bouton_photo)

        bouton_ajouter = Button(text="Ajouter l'entretien", size_hint_y=None, height="46dp",
                                 background_normal="", background_color=theme.BLEU, color=theme.BLANC)
        bouton_ajouter.bind(on_release=self._ajouter_entretien)

        form.add_widget(self.spinner_categorie)
        form.add_widget(self.champ_date)
        form.add_widget(self.champ_km)
        form.add_widget(self.champ_cout)
        form.add_widget(ligne_photo)
        self.layout_principal.add_widget(form)
        self.layout_principal.add_widget(bouton_ajouter)

        # Historique
        self.layout_principal.add_widget(Label(
            text="Historique", font_size=theme.TAILLE_SOUS_TITRE, bold=True,
            color=theme.GRIS_FONCE, size_hint_y=None, height="28dp", halign="left"
        ))
        self.scroll_historique = ScrollView()
        self.conteneur_historique = BoxLayout(orientation="vertical", spacing="8dp", size_hint_y=None)
        self.conteneur_historique.bind(minimum_height=self.conteneur_historique.setter("height"))
        self.scroll_historique.add_widget(self.conteneur_historique)
        self.layout_principal.add_widget(self.scroll_historique)

        self._rafraichir_historique()

    def _on_vehicule_change(self, spinner, texte):
        vehicules = db.lister_vehicules()
        for v in vehicules:
            if v["nom"] == texte:
                self.vehicule_selectionne_id = v["id"]
                break
        self._rafraichir_historique()

    def _ouvrir_selecteur_photo(self, *args):
        contenu = BoxLayout(orientation="vertical")
        selecteur = FileChooserIconView(filters=["*.png", "*.jpg", "*.jpeg"])
        bouton_valider = Button(text="Sélectionner", size_hint_y=None, height="44dp",
                                 background_normal="", background_color=theme.BLEU, color=theme.BLANC)
        contenu.add_widget(selecteur)
        contenu.add_widget(bouton_valider)
        popup = Popup(title="Choisir une photo de facture", content=contenu, size_hint=(0.9, 0.9))

        def valider(*_):
            if selecteur.selection:
                self.chemin_photo_facture = selecteur.selection[0]
                self.label_photo.text = self.chemin_photo_facture.split("/")[-1]
            popup.dismiss()

        bouton_valider.bind(on_release=valider)
        popup.open()

    def _ajouter_entretien(self, *args):
        if not self.vehicule_selectionne_id:
            self._alerte("Ajoutez d'abord un véhicule dans Paramètres.")
            return
        try:
            km = int(self.champ_km.text or 0)
            cout = float(self.champ_cout.text or 0)
        except ValueError:
            self._alerte("Kilométrage et coût doivent être numériques.")
            return

        # Calcule l'échéance suivante à partir de l'intervalle par défaut de la catégorie.
        categorie = self.spinner_categorie.text
        prochain_km = None
        for nom_cat, intervalle_km, _ in db.CATEGORIES_ENTRETIEN:
            if nom_cat == categorie and intervalle_km:
                prochain_km = km + intervalle_km

        db.ajouter_entretien(
            vehicule_id=self.vehicule_selectionne_id,
            categorie=categorie,
            date_entretien=self.champ_date.text.strip() or str(date.today()),
            kilometrage=km,
            cout=cout,
            photo_facture=self.chemin_photo_facture,
            prochain_km=prochain_km,
        )
        self.champ_km.text = ""
        self.champ_cout.text = ""
        self.chemin_photo_facture = None
        self.label_photo.text = "Aucune photo de facture"
        self._rafraichir_historique()

    def _rafraichir_historique(self):
        self.conteneur_historique.clear_widgets()
        if not self.vehicule_selectionne_id:
            return
        entretiens = db.lister_entretiens(self.vehicule_selectionne_id)
        for e in entretiens:
            self.conteneur_historique.add_widget(
                LigneEntretien(e, on_supprimer=self._supprimer_entretien)
            )

    def _supprimer_entretien(self, entretien_id):
        db.supprimer_entretien(entretien_id)
        self._rafraichir_historique()

    def _alerte(self, message):
        popup = Popup(title="Attention", content=Label(text=message),
                       size_hint=(0.8, 0.3))
        popup.open()

    def on_pre_enter(self, *args):
        self._construire_interface()
