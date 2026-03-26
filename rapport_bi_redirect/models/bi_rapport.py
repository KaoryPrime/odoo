from odoo import models, fields

class BIRapport(models.TransientModel):
    _name = 'bi.rapport'
    _description = 'Rapport BI Affichage'

    name = fields.Char("Nom du rapport", readonly=True)
    rapport_type = fields.Selection([
        ('stocks', 'Stocks'),
        ('inventaire', 'Inventaire'),
        ('factures', 'Factures'),
        ('vente', 'Vente'),
    ], string="Type de rapport", readonly=True)
