{
    'name': 'Restaurant Tip Management',
    'version': '18.0.1.0.0',
    'author': 'Kamil',
    'category': 'Restaurant',
    'summary': 'Gestion des pourboires et répartition entre le personnel du restaurant',
    'description': """
        Module de gestion des pourboires pour restaurant :

        - Enregistrement des pourboires par employé (espèces, carte, en ligne)
        - Lien avec les commandes de vente
        - Calcul automatique de la répartition entre employés
        - Vues Liste, Formulaire, Pivot et Graphique pour le reporting
        - Menu racine autonome avec icône dédiée

        Compatible Odoo 18.
    """,
    'depends': ['hr', 'sale', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/tip_views.xml',
        'views/tip_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
