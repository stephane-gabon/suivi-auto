"""Écran d'accueil : liste des véhicules, alertes d'entretien à venir."""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock

import theme
import database as db
from utils.notification_utils import verifier_et_notifier


class CarteVehicule(BoxLayout):
    def __init__(self, vehicule, **kwargs):
        super().__init__(orientation="vertical", size_hint_y=None, height="90dp",
                          padding="12dp", spacing="4dp", **kwargs)
        with self.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*theme.BLANC)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=theme.RAYON_COIN)
        self.bind(pos=self._maj_rect, size=self._maj_rect)

        self.add_widget(Label(
            text=f"[b]{vehicule['nom']}[/b]", markup=True, font_size=theme.TAILLE_SOUS_TITRE,
            color=theme.GRIS_FONCE, halign="left", size_hint_y=None, height="24dp",
            text_size=(None, None)
        ))
        details = f"{vehicule.get('marque') or ''} {vehicule.get('modele') or ''}".strip()
        self.add_widget(Label(
            text=f"{details}  •  {vehicule['kilometrage_actuel']:,} km".replace(",", " "),
            font_size=theme.TAILLE_PETIT, color=theme.GRIS_MOYEN,
            halign="left", size_hint_y=None, height="20dp"
        ))

    def _maj_rect(self, *args):
        self._rect.pos = self.pos
        self._rect.size = self.size


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout_principal = BoxLayout(orientation="vertical", padding="16dp", spacing="12dp")
        self.add_widget(self.layout_principal)
        self._construire_interface()

    def _construire_interface(self):
        self.layout_principal.clear_widgets()

        titre = Label(
            text="Mes véhicules", font_size=theme.TAILLE_TITRE, bold=True,
            color=theme.GRIS_FONCE, size_hint_y=None, height="40dp",
            halign="left"
        )
        titre.bind(size=lambda w, s: setattr(w, "text_size", s))
        self.layout_principal.add_widget(titre)

        scroll = ScrollView()
        conteneur = BoxLayout(orientation="vertical", spacing="10dp", size_hint_y=None)
        conteneur.bind(minimum_height=conteneur.setter("height"))

        vehicules = db.lister_vehicules()
        if not vehicules:
            conteneur.add_widget(Label(
                text="Aucun véhicule pour le moment.\nAjoutez-en un dans Paramètres.",
                color=theme.GRIS_MOYEN, size_hint_y=None, height="60dp"
            ))
        for v in vehicules:
            conteneur.add_widget(CarteVehicule(v))

        scroll.add_widget(conteneur)
        self.layout_principal.add_widget(scroll)

    def on_pre_enter(self, *args):
        self._construire_interface()
        # Vérifie les alertes d'entretien à chaque arrivée sur l'accueil.
        Clock.schedule_once(lambda dt: self._verifier_alertes(), 0.3)

    def _verifier_alertes(self):
        alertes = verifier_et_notifier()
        if alertes:
            self._afficher_popup_alertes(alertes)

    def _afficher_popup_alertes(self, alertes):
        contenu = BoxLayout(orientation="vertical", padding="12dp", spacing="8dp")
        for a in alertes[:5]:
            texte = f"{a['vehicule_nom']} — {a['categorie']}"
            contenu.add_widget(Label(text=texte, color=theme.GRIS_FONCE, size_hint_y=None, height="28dp"))

        from kivy.uix.button import Button
        fermer = Button(text="OK", size_hint_y=None, height="42dp",
                         background_normal="", background_color=theme.BLEU, color=theme.BLANC)
        contenu.add_widget(fermer)

        popup = Popup(title="⏰ Entretiens à prévoir", content=contenu,
                       size_hint=(0.85, None), height="320dp", auto_dismiss=True)
        fermer.bind(on_release=popup.dismiss)
        popup.open()
