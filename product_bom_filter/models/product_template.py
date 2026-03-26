from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    has_bom = fields.Boolean(
        compute='_compute_has_bom',
        store=True,
        string='Has BOM'
    )

    def _compute_has_bom(self):
        for template in self:
            boms = self.env['mrp.bom'].search([
                '|',
                ('product_tmpl_id', '=', template.id),
                ('product_id.product_tmpl_id', '=', template.id)
            ], limit=1)
            template.has_bom = bool(boms)
