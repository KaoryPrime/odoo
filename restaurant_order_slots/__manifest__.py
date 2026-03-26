{
    'name': 'Restaurant Order Slots',
    'version': '18.0.1.0.0',
    'depends': ['sale', 'website_sale'],
    'author': 'Kamil',
    'category': 'Sales',
    'summary': 'Créneaux horaires et type de commande pour restaurant (à emporter / livraison)',
    'description': """
        Ce module ajoute sur les commandes de vente :
        - Type de commande : À emporter / Livraison
        - Jour de retrait/livraison : Aujourd'hui / Demain / Après-demain
        - Créneau horaire configurable

        Compatible webshop (website_sale) : les créneaux s'affichent
        sur la page de paiement et sont sauvegardés sur la commande.
        Les informations apparaissent également sur les rapports PDF.
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/templates.xml',
        'views/report_sale_order.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
