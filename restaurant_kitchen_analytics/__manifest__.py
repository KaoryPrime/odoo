{
    'name': 'Restaurant Kitchen Analytics',
    'version': '18.0.1.0.0',
    'author': 'Kamil',
    'category': 'Restaurant',
    'summary': "Tableau de bord dynamique cuisine : temps de préparation, produits vendus vs livrés",
    'description': """
        Ce module fournit un tableau de bord analytique dédié à la cuisine :

        - Suivi de chaque plat commandé et livré
        - Champ calculé (store=True) mesurant la durée exacte entre la commande
          et la livraison de chaque plat
        - Écart entre les quantités commandées et les quantités réellement sorties
        - Vues Liste, Formulaire, Pivot et Graphique pour le reporting croisé
        - Menu racine autonome avec icône dédiée

        Compatible Odoo 18 — syntaxe XML stricte (invisible=, readonly=, required=).
    """,
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/kitchen_analytics_views.xml',
        'views/kitchen_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
