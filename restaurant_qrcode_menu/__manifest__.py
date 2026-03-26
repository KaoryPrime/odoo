{
    'name': 'Restaurant QR Code Menu',
    'version': '18.0.1.0.0',
    'author': 'Kamil',
    'category': 'Restaurant',
    'summary': 'Génération de QR codes pour accès au menu digital par table',
    'description': """
        Ce module permet de générer des QR codes pour chaque table du restaurant,
        offrant un accès rapide au menu digital.

        Fonctionnalités :
        - Création de QR codes liés à une URL de menu
        - Suivi du nombre de scans par table
        - Vues Liste, Formulaire et Recherche
        - Menu racine autonome dédié
    """,
    'depends': ['base'],
    'external_dependencies': {'python': ['qrcode']},
    'data': [
        'security/ir.model.access.csv',
        'views/qrcode_views.xml',
        'views/qrcode_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
