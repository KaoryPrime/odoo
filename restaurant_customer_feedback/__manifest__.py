{
    'name': 'Restaurant Customer Feedback',
    'version': '18.0.1.0.0',
    'author': 'Kamil',
    'category': 'Restaurant',
    'summary': "Gestion des avis clients et enquêtes de satisfaction pour restaurant",
    'description': """
        Ce module permet de collecter et analyser les retours clients :

        - Évaluation multi-critères (plats, service, ambiance, rapport qualité/prix)
        - Note globale calculée automatiquement
        - Suivi du statut (nouveau, lu, répondu, archivé)
        - Sources multiples (sur place, Google, site web, téléphone, email)
        - Vues Liste, Formulaire, Pivot et Graphique pour le reporting
        - Menu racine autonome avec sous-menus dédiés

        Compatible Odoo 18 — syntaxe XML stricte (invisible=, readonly=, required=).
    """,
    'depends': ['base', 'sale', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/feedback_views.xml',
        'views/feedback_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
