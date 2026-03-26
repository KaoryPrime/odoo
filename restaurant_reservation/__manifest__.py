{
    'name': 'Restaurant Reservation',
    'version': '18.0.1.0.0',
    'author': 'Kamil',
    'category': 'Restaurant',
    'summary': 'Gestion des réservations de tables pour restaurant',
    'description': """
        Module de gestion des réservations de restaurant :

        - Réservation par client avec créneaux horaires de 11h à 22h
        - Suivi du statut : brouillon, confirmé, installé, terminé, annulé
        - Affectation de table avec gestion de la capacité et des zones
        - Vues liste, formulaire, calendrier et recherche avancée
        - Champs calculés pour le nom et la couleur du kanban

        Compatible Odoo 18 — syntaxe XML stricte (invisible=, readonly=, required=).
    """,
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/reservation_views.xml',
        'views/reservation_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
