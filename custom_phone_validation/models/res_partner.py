from odoo import models, api, _
from odoo.exceptions import ValidationError
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('phone')
    def _check_phone_format(self):
        phone_regex = r'^(0|\+33)[1-9]\d{8}$'

        for partner in self:
            if partner.phone:
                phone_clean = partner.phone.replace(' ', '')
                if not re.match(phone_regex, phone_clean):
                    raise ValidationError(
                        _('Numéro de téléphone invalide. Il doit comporter exactement 10 chiffres et commencer par 0 ou +33.'))