"""Écran Rapports : synthèse des coûts par catégorie/véhicule, export Excel."""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from datetime import date, timedelta

import theme
import database as db
from utils.export_utils import generer_rapport_excel

PERIODES = {
    "Ce trimestre": 90,
    "Ce semestre": 182,
    "Cette année": 365,
    "Tout": None,
}


class BarreCategorie(BoxLayout):
    """Barre horizontale simple représentant un coût, proportionnelle au maximum."""

    def __init__(self, categorie, montant, montant_max, devise, **kwargs):
        super().__init__(
            orientation="vertical",
            size_hint_y=None,
            height="50dp",
            spacing="2dp",
            **kwargs
        )

        ligne_titre = BoxLayout(size_hint_y=None, height="18dp")

        ligne_titre.add_widget(
            Label(
                text=categorie,
                font_size=theme.TAILLE_PETIT,
                color=theme.GRIS_FONCE,
                halign="left"
            )
        )

        ligne_titre.add_widget(
            Label(
                text=f"{montant:,.0f} {devise}".replace(",", " "),
                font_size=theme.TAILLE_PETIT,
                color=theme.GRIS_MOYEN,
                halign="right"
            )
        )

        self.add_widget(ligne_titre)

        fond = BoxLayout(size_hint_y=None, height="14dp")
        proportion = (montant / montant_max) if montant_max else 0

        with fond.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*theme.GRIS_CLAIR)
            RoundedRectangle(
                pos=fond.pos,
                size=fond.size,
                radius=[6]
            )

        barre = BoxLayout(
            size_hint_x=max(proportion, 0.02)
        )

        with barre.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*theme.BLEU)
            self._rect = RoundedRectangle(
                pos=barre.pos,
                size=barre.size,
                radius=[6]
            )

        barre.bind(
            pos=lambda *a: setattr(self._rect, "pos", barre.pos)
        )
        barre.bind(
            size=lambda *a: setattr(self._rect, "size", barre.size)
        )

        fond.add_widget(barre)
        fond.add_widget(
            BoxLayout(
                size_hint_x=max(1 - proportion, 0.001)
            )
        )

        self.add_widget(fond)


class RapportsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.vehicule_selectionne_id = None

        self.layout_principal = BoxLayout(
            orientation="vertical",
            padding="16dp",
            spacing="10dp"
        )

        self.add_widget(self.layout_principal)

        self._construire_interface()

    def _construire_interface(self):
        self.layout_principal.clear_widgets()

        devise = db.get_parametre("devise", "FCFA")

        titre = Label(
            text="Rapports",
            font_size=theme.TAILLE_TITRE,
            bold=True,
            color=theme.GRIS_FONCE,
            size_hint_y=None,
            height="36dp",
            halign="left"
        )

        titre.bind(
            size=lambda w, s: setattr(w, "text_size", s)
        )

        self.layout_principal.add_widget(titre)

        ligne_filtres = BoxLayout(
            size_hint_y=None,
            height="44dp",
            spacing="8dp"
        )

        vehicules = db.lister_vehicules()

        noms = ["Tous les véhicules"] + [
            v["nom"] for v in vehicules
        ]

        self.spinner_vehicule = Spinner(
            text=noms[0],
            values=noms,
            background_color=theme.GRIS_CLAIR,
            color=theme.GRIS_FONCE
        )

        self.spinner_periode = Spinner(
            text="Cette année",
            values=list(PERIODES.keys()),
            background_color=theme.GRIS_CLAIR,
            color=theme.GRIS_FONCE
        )

        self.spinner_vehicule.bind(
            text=lambda *a: self._rafraichir()
        )

        self.spinner_periode.bind(
            text=lambda *a: self._rafraichir()
        )

        ligne_filtres.add_widget(self.spinner_vehicule)
        ligne_filtres.add_widget(self.spinner_periode)

        self.layout_principal.add_widget(ligne_filtres)

        self.layout_principal.add_widget(
            Label(
                text="Coûts par catégorie",
                font_size=theme.TAILLE_SOUS_TITRE,
                bold=True,
                color=theme.GRIS_FONCE,
                size_hint_y=None,
                height="26dp",
                halign="left"
            )
        )

        self.scroll = ScrollView()

        self.conteneur_barres = BoxLayout(
            orientation="vertical",
            spacing="6dp",
            size_hint_y=None
        )

        self.conteneur_barres.bind(
            minimum_height=self.conteneur_barres.setter("height")
        )

        self.scroll.add_widget(self.conteneur_barres)

        self.layout_principal.add_widget(self.scroll)

        # Export Excel uniquement.
        ligne_export = BoxLayout(
            size_hint_y=None,
            height="46dp",
            spacing="10dp"
        )

        bouton_excel = Button(
            text="📊 Export Excel",
            background_normal="",
            background_color=theme.BLEU_FONCE,
            color=theme.BLANC
        )

        bouton_excel.bind(
            on_release=lambda *_: self._exporter_excel()
        )

        ligne_export.add_widget(bouton_excel)

        self.layout_principal.add_widget(ligne_export)

        self._devise = devise

        self._rafraichir()

    def _dates_periode(self):
        jours = PERIODES[self.spinner_periode.text]

        if jours is None:
            return None, None

        date_debut = (
            date.today() - timedelta(days=jours)
        ).isoformat()

        date_fin = date.today().isoformat()

        return date_debut, date_fin

    def _vehicule_id_selectionne(self):
        if self.spinner_vehicule.text == "Tous les véhicules":
            return None

        for v in db.lister_vehicules():
            if v["nom"] == self.spinner_vehicule.text:
                return v["id"]

        return None

    def _rafraichir(self):
        self.conteneur_barres.clear_widgets()

        vehicule_id = self._vehicule_id_selectionne()

        date_debut, date_fin = self._dates_periode()

        synthese = db.cout_total_par_categorie(
            vehicule_id,
            date_debut,
            date_fin
        )

        if not synthese:
            self.conteneur_barres.add_widget(
                Label(
                    text="Aucune dépense sur cette période.",
                    color=theme.GRIS_MOYEN,
                    size_hint_y=None,
                    height="40dp"
                )
            )
            return

        montant_max = max(synthese.values())

        for categorie, montant in sorted(
            synthese.items(),
            key=lambda kv: -kv[1]
        ):
            self.conteneur_barres.add_widget(
                BarreCategorie(
                    categorie,
                    montant,
                    montant_max,
                    self._devise
                )
            )

    def _exporter_excel(self):
        vehicule_id = self._vehicule_id_selectionne()

        date_debut, date_fin = self._dates_periode()

        try:
            chemin = generer_rapport_excel(
                vehicule_id,
                date_debut,
                date_fin
            )

            message = f"Rapport Excel généré :\n{chemin}"

        except Exception as exc:
            message = f"Erreur lors de l'export :\n{exc}"

        popup = Popup(
            title="Export Excel",
            content=Label(
                text=message,
                color=theme.GRIS_FONCE
            ),
            size_hint=(0.85, 0.35)
        )

        popup.open()

    def on_pre_enter(self, *args):
        self._construire_interface()
