{
    'name': 'Restaurant Happy Hour',
    'version': '18.0.1.0.0',
    'author': 'Kamil',
    'category': 'Restaurant',
    'summary': 'Gestion des promotions horaires automatiques pour restaurant',
    'description': """
        Ce module permet de gérer les happy hours dans un restaurant :

        - Définition de créneaux horaires promotionnels par jour de la semaine
        - Application automatique de remises (pourcentage ou montant fixe)
        - Suivi des produits concernés avec calcul du prix remisé
        - Vues Liste, Formulaire et Recherche pour le pilotage des promotions
        - Menu racine autonome avec gestion des promotions et du planning
    """,
    'depends': ['product', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/happy_hour_views.xml',
        'views/happy_hour_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
