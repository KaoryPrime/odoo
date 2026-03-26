{
    'name': 'Restaurant Waste Tracking',
    'version': '18.0.1.0.0',
    'author': 'Kamil',
    'category': 'Restaurant',
    'summary': "Suivi du gaspillage alimentaire pour réduction des coûts et reporting durabilité",
    'description': """
        Module de suivi du gaspillage alimentaire en restaurant :

        - Enregistrement de chaque perte avec produit, quantité et motif
        - Calcul automatique du coût estimé basé sur le prix de revient
        - Workflow brouillon / validé pour contrôle des saisies
        - Vues Liste, Formulaire, Pivot et Graphique pour le reporting
        - Menu racine autonome dédié au suivi du gaspillage

        Compatible Odoo 18 — syntaxe XML stricte (invisible=, readonly=, required=).
    """,
    'depends': ['product', 'hr', 'mail', 'uom'],
    'data': [
        'security/ir.model.access.csv',
        'views/waste_views.xml',
        'views/waste_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
