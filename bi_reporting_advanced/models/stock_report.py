from odoo import models, fields, tools

class UnfinishedProductStock(models.Model):
    _name = 'bi.unfinished.product.stock'
    _auto = False

    article = fields.Char()
    categorie = fields.Char()
    stock = fields.Float()

    def init(self):
        tools.drop_view_if_exists(self._cr, 'bi_unfinished_products_stock')
        self._cr.execute("""
            CREATE VIEW bi_unfinished_products_stock AS (
              SELECT
                pt.id as id,
                pt.name as article,
                pc.complete_name as categorie,
                sq.quantity as stock
              FROM product_template pt
              JOIN product_category pc ON pt.categ_id = pc.id
              JOIN product_product pp ON pp.product_tmpl_id = pt.id
              JOIN stock_quant sq ON sq.product_id = pp.id
              WHERE pt.type = 'product' AND pt.sale_ok = true AND pt.purchase_ok = false
            )
        """)
