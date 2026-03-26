{
    'name': 'Restaurant Daily Menu',
    'version': '18.0.1.0.0',
    'author': 'Kamil',
    'category': 'Restaurant',
    'summary': 'Gestion des menus du jour et planification hebdomadaire',
    'description': """
        Module de gestion des menus quotidiens pour restaurant.

        - Création de menus par service (midi, soir, brunch, spécial)
        - Lignes de plats avec catégorie, prix et disponibilité
        - Vue calendrier pour la planification hebdomadaire
        - Suivi par responsable avec chatter intégré
    """,
    'depends': ['product', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/daily_menu_views.xml',
        'views/daily_menu_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
