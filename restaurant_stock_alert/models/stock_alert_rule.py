from odoo import api, fields, models


class RestaurantStockAlertRule(models.Model):
    _name = 'restaurant.stock.alert.rule'
    _description = 'Règle d\'alerte de stock'
    _order = 'is_below_threshold desc, name'

    name = fields.Char(
        string='Nom',
        compute='_compute_name',
        store=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Produit',
        required=True,
    )
    min_quantity = fields.Float(
        string='Seuil minimum',
        required=True,
        default=5,
    )
    reorder_quantity = fields.Float(
        string='Quantité à recommander',
        default=20,
    )
    current_stock = fields.Float(
        string='Stock actuel',
        compute='_compute_current_stock',
    )
    is_below_threshold = fields.Boolean(
        string='Sous le seuil',
        compute='_compute_is_below_threshold',
        store=True,
    )
    alert_count = fields.Integer(
        string="Nombre d'alertes",
        compute='_compute_alert_count',
    )
    active = fields.Boolean(
        default=True,
    )
    category_id = fields.Many2one(
        comodel_name='product.category',
        related='product_id.categ_id',
        store=True,
        string='Catégorie',
    )
    last_check_date = fields.Datetime(
        string='Dernière vérification',
    )
    alert_line_ids = fields.One2many(
        comodel_name='restaurant.stock.alert.line',
        inverse_name='rule_id',
        string='Alertes',
    )

    @api.depends('product_id')
    def _compute_name(self):
        for rule in self:
            if rule.product_id:
                rule.name = f"Alerte – {rule.product_id.name}"
            else:
                rule.name = 'Nouvelle règle'

    def _compute_current_stock(self):
        for rule in self:
            if rule.product_id:
                rule.current_stock = rule.product_id.qty_available
            else:
                rule.current_stock = 0.0

    @api.depends('current_stock', 'min_quantity')
    def _compute_is_below_threshold(self):
        for rule in self:
            rule.is_below_threshold = rule.current_stock < rule.min_quantity

    def _compute_alert_count(self):
        for rule in self:
            rule.alert_count = len(rule.alert_line_ids)

    def action_check_stock(self):
        for rule in self:
            rule.last_check_date = fields.Datetime.now()
            if rule.current_stock < rule.min_quantity:
                suggested = rule.reorder_quantity - rule.current_stock
                if suggested < 0:
                    suggested = rule.reorder_quantity
                self.env['restaurant.stock.alert.line'].create({
                    'rule_id': rule.id,
                    'current_quantity': rule.current_stock,
                    'suggested_order': suggested,
                    'state': 'new',
                })

    @api.model
    def action_check_all_rules(self):
        rules = self.search([('active', '=', True)])
        rules.action_check_stock()

    def action_view_alerts(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': "Alertes",
            'res_model': 'restaurant.stock.alert.line',
            'view_mode': 'list,form',
            'domain': [('rule_id', '=', self.id)],
            'context': {'default_rule_id': self.id},
        }
