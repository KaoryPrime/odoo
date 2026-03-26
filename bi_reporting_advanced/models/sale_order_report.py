from odoo import models, fields, tools

class SaleOrderReport(models.Model):
    _name = 'bi.sale.order.report'
    _auto = False

    date_order = fields.Date()
    client = fields.Char()
    total = fields.Float()
    sale_order_type = fields.Char()

    def init(self):
        tools.drop_view_if_exists(self._cr, 'bi_sale_order_report')
        self._cr.execute("""
            CREATE VIEW bi_sale_order_report AS (
                SELECT
                    so.id as id,
                    so.date_order::date,
                    rp.name as client,
                    so.amount_total as total,
                    so.state AS sale_order_type -- On utilise 'state' car 'order_type' n'existe pas nativement
                FROM sale_order so
                JOIN res_partner rp ON rp.id = so.partner_id
                WHERE so.state IN ('sale', 'done')
            )
        """)