from odoo import models, api
from odoo.exceptions import ValidationError
import re

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.constrains('partner_id')
    def _check_partner_phone(self):
        phone_regex = re.compile(r'^(\+?\d{8,15})$')
        for order in self:
            partner = order.partner_id
            phone = partner.phone or ''
            if phone and not phone_regex.match(phone):
                raise ValidationError("Le format du numéro de téléphone est invalide. "
                                      "Format attendu : +33612345678")
