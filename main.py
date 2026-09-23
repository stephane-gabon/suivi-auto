"""
main.py
Point d'entrée de l'application mobile de suivi d'entretien automobile.
Style inspiré d'Apple : sobre, épuré, palette blanc / gris clair / bleu.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.lang import Builder
from kivy.core.window import Window

import theme
import database as db
from screens.home_screen import HomeScreen
from screens.entretien_screen import EntretienScreen
from screens.carburant_screen import CarburantScreen
from screens.rapports_screen import RapportsScreen
from screens.parametres_screen import ParametresScreen

Builder.load_file("car_maintenance.kv")

ONGLETS = [
    ("accueil", "🏠", "Accueil"),
    ("entretiens", "🔧", "Entretiens"),
    ("carburant", "⛽", "Carburant"),
    ("rapports", "📊", "Rapports"),
    ("parametres", "⚙️", "Paramètres"),
]


class RootLayout(BoxLayout):
    pass


class BoutonOnglet(Button):
    """Bouton de navigation inférieure, style plat, icône + libellé."""

    def __init__(self, icone, libelle, actif=False, **kwargs):
        super().__init__(
            text=f"{icone}\n{libelle}",
            font_size="11sp",
            background_normal="",
            background_color=theme.BLANC,
            color=theme.BLEU if actif else theme.GRIS_MOYEN,
            halign="center",
            **kwargs
        )
        self.actif = actif


class SuiviAutoApp(App):
    def build(self):
        self.title = "Suivi Auto"
        Window.clearcolor = theme.GRIS_CLAIR

        db.init_db()

        racine = RootLayout()
        gestionnaire = racine.ids.screen_manager
        gestionnaire.transition = NoTransition()

        gestionnaire.add_widget(HomeScreen(name="accueil"))
        gestionnaire.add_widget(EntretienScreen(name="entretiens"))
        gestionnaire.add_widget(CarburantScreen(name="carburant"))
        gestionnaire.add_widget(RapportsScreen(name="rapports"))
        gestionnaire.add_widget(ParametresScreen(name="parametres"))

        self.gestionnaire = gestionnaire
        self.boutons_navigation = {}
        barre = racine.ids.barre_navigation
        for nom_ecran, icone, libelle in ONGLETS:
            bouton = BoutonOnglet(icone, libelle, actif=(nom_ecran == "accueil"))
            bouton.bind(on_release=lambda b, n=nom_ecran: self._changer_ecran(n))
            barre.add_widget(bouton)
            self.boutons_navigation[nom_ecran] = bouton

        return racine

    def _changer_ecran(self, nom_ecran):
        self.gestionnaire.current = nom_ecran
        for nom, bouton in self.boutons_navigation.items():
            bouton.color = theme.BLEU if nom == nom_ecran else theme.GRIS_MOYEN


if __name__ == "__main__":
    SuiviAutoApp().run()
