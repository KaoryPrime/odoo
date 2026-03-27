from odoo import models, fields, _
from odoo.exceptions import AccessError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    x_validated_by_ringeard = fields.Boolean(copy=False)
    vat_category = fields.Selection(related='partner_id.vat_category', store=True)

    def button_confirm(self):
        for order in self:
            if order.vat_category == 'vat2':
                first_day = fields.Date.context_today(self).replace(month=1, day=1)
                orders = self.env['purchase.order'].search([
                    ('partner_id', '=', order.partner_id.id),
                    ('state', 'in', ['purchase', 'done']),
                    ('date_order', '>=', fields.Datetime.to_datetime(first_day)),
                ])
                total = sum(o.amount_total for o in orders) + order.amount_total
                if total > 100000:
                    raise ValidationError(_('Dépassement 100000€'))
            if order.vat_category == 'vat3' and not order.x_validated_by_ringeard:
                raise ValidationError(_('Validation membre du personnel RH requise'))
        return super().button_confirm()

    def action_validate_ringeard(self):
        self.ensure_one()
        if not self.env.user.has_group('supplier_vat_validation_final.group_validateur'):
            raise AccessError(_('Seul un validateur peut effectuer cette action.'))
        self.x_validated_by_ringeard = True
