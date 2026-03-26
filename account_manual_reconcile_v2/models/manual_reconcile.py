from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    lettrage_ref = fields.Char(string='Référence Lettrage', copy=False)

# On ajoute le même champ sur le modèle des paiements
class AccountPayment(models.Model):
    _inherit = 'account.payment'

    lettrage_ref = fields.Char(string='Référence Lettrage', copy=False)