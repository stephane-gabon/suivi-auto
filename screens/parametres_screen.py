"""Écran Paramètres : gestion des véhicules (ajout/suppression), devise."""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

import theme
import database as db

DEVISES_DISPONIBLES = ["FCFA", "EUR", "USD", "MAD", "XOF"]


class LigneVehicule(BoxLayout):
    def __init__(self, vehicule, on_supprimer, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height="56dp",
                          padding="10dp", **kwargs)
        with self.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*theme.BLANC)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=theme.RAYON_COIN)
        self.bind(pos=self._maj_rect, size=self._maj_rect)

        self.add_widget(Label(
            text=f"{vehicule['nom']} ({vehicule.get('marque', '')})",
            color=theme.GRIS_FONCE, font_size=theme.TAILLE_TEXTE
        ))
        bouton = Button(text="Supprimer", size_hint_x=None, width="100dp",
                         background_normal="", background_color=theme.GRIS_CLAIR,
                         color=theme.ROUGE_ALERTE, font_size=theme.TAILLE_PETIT)
        bouton.bind(on_release=lambda *_: on_supprimer(vehicule["id"]))
        self.add_widget(bouton)

    def _maj_rect(self, *args):
        self._rect.pos = self.pos
        self._rect.size = self.size


class ParametresScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout_principal = BoxLayout(orientation="vertical", padding="16dp", spacing="10dp")
        self.add_widget(self.layout_principal)
        self._construire_interface()

    def _construire_interface(self):
        self.layout_principal.clear_widgets()

        titre = Label(text="Paramètres", font_size=theme.TAILLE_TITRE, bold=True,
                       color=theme.GRIS_FONCE, size_hint_y=None, height="36dp", halign="left")
        titre.bind(size=lambda w, s: setattr(w, "text_size", s))
        self.layout_principal.add_widget(titre)

        # Devise
        ligne_devise = BoxLayout(size_hint_y=None, height="44dp", spacing="10dp")
        ligne_devise.add_widget(Label(text="Devise :", color=theme.GRIS_FONCE,
                                       size_hint_x=None, width="80dp"))
        devise_actuelle = db.get_parametre("devise", "FCFA")
        self.spinner_devise = Spinner(text=devise_actuelle, values=DEVISES_DISPONIBLES,
                                       background_color=theme.GRIS_CLAIR, color=theme.GRIS_FONCE)
        self.spinner_devise.bind(text=lambda s, t: db.set_parametre("devise", t))
        ligne_devise.add_widget(self.spinner_devise)
        self.layout_principal.add_widget(ligne_devise)

        # Formulaire nouveau véhicule
        self.layout_principal.add_widget(Label(
            text="Ajouter un véhicule", font_size=theme.TAILLE_SOUS_TITRE, bold=True,
            color=theme.GRIS_FONCE, size_hint_y=None, height="28dp", halign="left"
        ))
        form = BoxLayout(orientation="vertical", spacing="6dp", size_hint_y=None, height="190dp")
        self.champ_nom = TextInput(hint_text="Nom (ex: Voiture principale)",
                                    size_hint_y=None, height="40dp")
        self.champ_marque = TextInput(hint_text="Marque", size_hint_y=None, height="40dp")
        self.champ_modele = TextInput(hint_text="Modèle", size_hint_y=None, height="40dp")
        self.champ_km_initial = TextInput(hint_text="Kilométrage actuel", input_filter="int",
                                           size_hint_y=None, height="40dp")
        bouton_ajouter = Button(text="Ajouter le véhicule", size_hint_y=None, height="44dp",
                                 background_normal="", background_color=theme.BLEU, color=theme.BLANC)
        bouton_ajouter.bind(on_release=self._ajouter_vehicule)

        form.add_widget(self.champ_nom)
        form.add_widget(self.champ_marque)
        form.add_widget(self.champ_modele)
        form.add_widget(self.champ_km_initial)
        self.layout_principal.add_widget(form)
        self.layout_principal.add_widget(bouton_ajouter)

        # Liste des véhicules existants
        self.layout_principal.add_widget(Label(
            text="Mes véhicules", font_size=theme.TAILLE_SOUS_TITRE, bold=True,
            color=theme.GRIS_FONCE, size_hint_y=None, height="28dp", halign="left"
        ))
        self.scroll = ScrollView()
        self.conteneur_vehicules = BoxLayout(orientation="vertical", spacing="6dp", size_hint_y=None)
        self.conteneur_vehicules.bind(minimum_height=self.conteneur_vehicules.setter("height"))
        self.scroll.add_widget(self.conteneur_vehicules)
        self.layout_principal.add_widget(self.scroll)

        self._rafraichir()

    def _ajouter_vehicule(self, *args):
        nom = self.champ_nom.text.strip()
        if not nom:
            return
        try:
            km_initial = int(self.champ_km_initial.text or 0)
        except ValueError:
            km_initial = 0

        db.ajouter_vehicule(
            nom=nom,
            marque=self.champ_marque.text.strip(),
            modele=self.champ_modele.text.strip(),
            kilometrage_actuel=km_initial,
        )
        self.champ_nom.text = ""
        self.champ_marque.text = ""
        self.champ_modele.text = ""
        self.champ_km_initial.text = ""
        self._rafraichir()

    def _supprimer_vehicule(self, vehicule_id):
        db.supprimer_vehicule(vehicule_id)
        self._rafraichir()

    def _rafraichir(self):
        self.conteneur_vehicules.clear_widgets()
        for v in db.lister_vehicules():
            self.conteneur_vehicules.add_widget(
                LigneVehicule(v, on_supprimer=self._supprimer_vehicule)
            )

    def on_pre_enter(self, *args):
        self._construire_interface()
