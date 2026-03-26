from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from datetime import date
class PurchaseOrder(models.Model):
 _inherit="purchase.order"
 x_validated_by_ringeard=fields.Boolean()
 vat_category=fields.Selection(related='partner_id.vat_category',store=True)
 def button_confirm(self):
  for order in self:
   if order.vat_category=='vat2':
    orders=self.env['purchase.order'].search([('partner_id','=',order.partner_id.id),('state','in',['purchase','done']),('date_order','>=',date.today().replace(month=1,day=1))])
    if sum(o.amount_total for o in orders)+order.amount_total>100000:
     raise ValidationError('Dépassement 100000€')
   if order.vat_category=='vat3' and not order.x_validated_by_ringeard:
    raise ValidationError('Validation membre du personnel RH requise')
  return super().button_confirm()
 def action_validate_ringeard(self):
  self.x_validated_by_ringeard=True