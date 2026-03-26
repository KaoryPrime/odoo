{
    'name': 'Restaurant Table Layout',
    'version': '18.0.1.0.0',
    'author': 'Kamil',
    'category': 'Restaurant',
    'summary': "Gestion du plan de salle : zones, tables et suivi en temps réel",
    'description': """
        Ce module permet de gérer l'organisation des tables et zones
        d'un restaurant avec plan de salle et suivi en temps réel :

        - Définition de zones (intérieur, terrasse, bar, VIP, privé)
        - Gestion des tables avec capacité, forme et statut
        - Suivi en temps réel du statut des tables
        - Vue Kanban colorée pour visualiser l'occupation
        - Assignation des serveurs et suivi des commandes

        Compatible Odoo 18 — syntaxe XML stricte (invisible=, readonly=, required=).
    """,
    'depends': ['base', 'sale', 'hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/table_views.xml',
        'views/table_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
