{
    'name': 'Shipday Integration',
    'version': '18.0.1.0.0',
    'summary': 'Intégration Odoo → Shipday : envoi des commandes vers le livreur',
    'description': """
        Ce module permet d'envoyer les commandes Odoo vers Shipday (plateforme de dispatch livraison).

        Fonctionnalités :
        - Bouton d'envoi manuel sur la fiche commande
        - Clé API configurable dans les paramètres système (jamais en dur dans le code)
        - Informations restaurant configurables
        - Gestion des créneaux de livraison (compatible restaurant_order_slots si présent)
        - Traçabilité : statut d'envoi + logs dans le chatter
        - Bouton de renvoi en cas d'erreur
    """,
    'category': 'Sales',
    'author': 'Kamil',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'data/shipday_config_data.xml',
        'views/res_config_settings_views.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
