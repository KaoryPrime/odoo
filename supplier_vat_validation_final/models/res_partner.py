from odoo import models,fields
class ResPartner(models.Model):
 _inherit="res.partner"
 vat_category = fields.Selection([
  ('vat1', 'VAT 1'),
  ('vat2', 'VAT 2'),
  ('vat3', 'VAT 3')
 ], string="Catégorie VAT")