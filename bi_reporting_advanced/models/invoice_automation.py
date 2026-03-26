from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def auto_generate_invoice(self):
        orders = self.search([('invoice_status', '=', 'to invoice')])
        for order in orders:
            order._create_invoices()
