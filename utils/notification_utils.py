"""
notification_utils.py
Gestion des notifications push (via plyer) et de la logique d'alerte
basée sur le kilométrage ou la date d'échéance.
"""

from database import entretiens_a_venir

try:
    from plyer import notification
    PLYER_DISPONIBLE = True
except Exception:
    # plyer n'est pas toujours disponible (ex: environnement de développement
    # sans backend natif). On dégrade sans planter l'application.
    PLYER_DISPONIBLE = False


def envoyer_notification(titre, message):
    """Envoie une notification push native. Ne lève jamais d'exception."""
    if not PLYER_DISPONIBLE:
        print(f"[Notification simulée] {titre} - {message}")
        return
    try:
        notification.notify(
            title=titre,
            message=message,
            app_name="Suivi Auto",
            timeout=10,
        )
    except Exception as exc:
        print(f"[Notification échouée] {exc}")


def verifier_et_notifier():
    """
    À appeler périodiquement (ex: au lancement de l'app, ou via un job planifié).
    Vérifie les entretiens dont l'échéance est proche (km ou date) et envoie
    une notification pour chacun.
    Retourne la liste des alertes trouvées (pour affichage pop-up dans l'app).
    """
    alertes = entretiens_a_venir()
    for a in alertes:
        parties = []
        if a.get("km_restant") is not None:
            if a["km_restant"] <= 0:
                parties.append("dépassé de %d km" % abs(a["km_restant"]))
            else:
                parties.append(f"dans {a['km_restant']} km")
        if a.get("jours_restants") is not None:
            if a["jours_restants"] <= 0:
                parties.append("date dépassée")
            else:
                parties.append(f"dans {a['jours_restants']} jours")

        message = f"{a['vehicule_nom']} - {a['categorie']} ({', '.join(parties)})"
        envoyer_notification("Entretien à prévoir", message)
    return alertes
