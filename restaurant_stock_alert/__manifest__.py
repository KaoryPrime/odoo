{
    'name': 'Restaurant Stock Alert',
    'version': '18.0.1.0.0',
    'author': 'Kamil',
    'category': 'Restaurant',
    'summary': 'Alertes de stock intelligentes avec seuils minimums et suggestions de réapprovisionnement',
    'description': """
        Module d'alertes de stock pour restaurant.

        - Définition de règles avec seuils minimums par produit
        - Détection automatique des stocks sous le seuil
        - Suggestions de quantités à commander
        - Suivi des alertes avec états (nouveau, acquitté, commandé, résolu)
        - Analyse pivot des alertes par produit et par mois
    """,
    'depends': ['stock', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_alert_views.xml',
        'views/stock_alert_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
