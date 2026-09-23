"""Écran Carburant : saisie des pleins et suivi de la consommation moyenne."""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from datetime import date

import theme
import database as db


class LignePlein(BoxLayout):
    def __init__(self, plein, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height="56dp",
                          padding="10dp", **kwargs)
        with self.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*theme.BLANC)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=theme.RAYON_COIN)
        self.bind(pos=self._maj_rect, size=self._maj_rect)

        texte = (f"{plein['date_plein']}  •  {plein['litres']} L  •  "
                 f"{plein['prix_total']:,.0f} FCFA  •  {plein['kilometrage']:,} km")
        self.add_widget(Label(text=texte.replace(",", " "), font_size=theme.TAILLE_PETIT,
                               color=theme.GRIS_FONCE))

    def _maj_rect(self, *args):
        self._rect.pos = self.pos
        self._rect.size = self.size


class CarburantScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vehicule_selectionne_id = None
        self.layout_principal = BoxLayout(orientation="vertical", padding="16dp", spacing="10dp")
        self.add_widget(self.layout_principal)
        self._construire_interface()

    def _construire_interface(self):
        self.layout_principal.clear_widgets()

        titre = Label(text="Carburant", font_size=theme.TAILLE_TITRE, bold=True,
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

        self.label_consommation = Label(
            text="Consommation moyenne : —", font_size=theme.TAILLE_SOUS_TITRE,
            color=theme.BLEU, size_hint_y=None, height="30dp", bold=True
        )
        self.layout_principal.add_widget(self.label_consommation)

        form = BoxLayout(orientation="vertical", spacing="6dp", size_hint_y=None, height="230dp")
        self.champ_date = TextInput(text=str(date.today()), hint_text="AAAA-MM-JJ",
                                     size_hint_y=None, height="40dp")
        self.champ_litres = TextInput(hint_text="Litres", input_filter="float",
                                       size_hint_y=None, height="40dp")
        self.champ_prix = TextInput(hint_text="Prix total (FCFA)", input_filter="float",
                                     size_hint_y=None, height="40dp")
        self.champ_km = TextInput(hint_text="Kilométrage au compteur", input_filter="int",
                                   size_hint_y=None, height="40dp")

        ligne_case = BoxLayout(size_hint_y=None, height="36dp", spacing="8dp")
        self.case_plein_complet = CheckBox(active=True, size_hint_x=None, width="30dp")
        ligne_case.add_widget(self.case_plein_complet)
        ligne_case.add_widget(Label(text="Plein complet (réservoir plein)",
                                     color=theme.GRIS_MOYEN, font_size=theme.TAILLE_PETIT))

        bouton_ajouter = Button(text="Enregistrer le plein", size_hint_y=None, height="46dp",
                                 background_normal="", background_color=theme.BLEU, color=theme.BLANC)
        bouton_ajouter.bind(on_release=self._ajouter_plein)

        form.add_widget(self.champ_date)
        form.add_widget(self.champ_litres)
        form.add_widget(self.champ_prix)
        form.add_widget(self.champ_km)
        form.add_widget(ligne_case)
        self.layout_principal.add_widget(form)
        self.layout_principal.add_widget(bouton_ajouter)

        self.layout_principal.add_widget(Label(
            text="Historique des pleins", font_size=theme.TAILLE_SOUS_TITRE, bold=True,
            color=theme.GRIS_FONCE, size_hint_y=None, height="28dp", halign="left"
        ))
        self.scroll_historique = ScrollView()
        self.conteneur_historique = BoxLayout(orientation="vertical", spacing="6dp", size_hint_y=None)
        self.conteneur_historique.bind(minimum_height=self.conteneur_historique.setter("height"))
        self.scroll_historique.add_widget(self.conteneur_historique)
        self.layout_principal.add_widget(self.scroll_historique)

        self._rafraichir()

    def _on_vehicule_change(self, spinner, texte):
        for v in db.lister_vehicules():
            if v["nom"] == texte:
                self.vehicule_selectionne_id = v["id"]
                break
        self._rafraichir()

    def _ajouter_plein(self, *args):
        if not self.vehicule_selectionne_id:
            return
        try:
            litres = float(self.champ_litres.text or 0)
            prix = float(self.champ_prix.text or 0)
            km = int(self.champ_km.text or 0)
        except ValueError:
            return

        db.ajouter_plein(
            vehicule_id=self.vehicule_selectionne_id,
            date_plein=self.champ_date.text.strip() or str(date.today()),
            litres=litres,
            prix_total=prix,
            kilometrage=km,
            plein_complet=self.case_plein_complet.active,
        )
        self.champ_litres.text = ""
        self.champ_prix.text = ""
        self.champ_km.text = ""
        self._rafraichir()

    def _rafraichir(self):
        self.conteneur_historique.clear_widgets()
        if not self.vehicule_selectionne_id:
            self.label_consommation.text = "Consommation moyenne : —"
            return

        conso = db.consommation_moyenne(self.vehicule_selectionne_id)
        self.label_consommation.text = (
            f"Consommation moyenne : {conso} L/100km" if conso
            else "Consommation moyenne : ajoutez au moins 2 pleins complets"
        )

        for p in db.lister_pleins(self.vehicule_selectionne_id):
            self.conteneur_historique.add_widget(LignePlein(p))

    def on_pre_enter(self, *args):
        self._construire_interface()
