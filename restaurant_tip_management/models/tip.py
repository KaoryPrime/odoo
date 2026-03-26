from odoo import api, fields, models


class RestaurantTip(models.Model):

    _name = 'restaurant.tip'
    _description = 'Pourboire'
    _inherit = ['mail.thread']
    _order = 'tip_date desc, id desc'

    name = fields.Char(
        string='Référence',
        compute='_compute_name',
        store=True,
    )
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employé',
        required=True,
        index=True,
    )
    department_id = fields.Many2one(
        comodel_name='hr.department',
        related='employee_id.department_id',
        store=True,
        string='Département',
    )
    tip_date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.today,
    )
    amount = fields.Float(
        string='Montant (€)',
        required=True,
    )
    source = fields.Selection(
        selection=[
            ('cash', 'Espèces'),
            ('card', 'Carte'),
            ('online', 'En ligne'),
        ],
        string='Source',
        required=True,
        default='cash',
    )
    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Commande associée',
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Brouillon'),
            ('validated', 'Validé'),
            ('paid', 'Payé'),
        ],
        string='Statut',
        default='draft',
        required=True,
        tracking=True,
    )
    note = fields.Text(
        string='Remarque',
    )
    color = fields.Integer(
        string='Couleur',
        compute='_compute_color',
    )

    @api.depends('employee_id', 'tip_date')
    def _compute_name(self):
        for rec in self:
            employee_name = rec.employee_id.name if rec.employee_id else '?'
            date_str = rec.tip_date.strftime('%d/%m/%Y') if rec.tip_date else '?'
            rec.name = f"{employee_name} – {date_str}"

    @api.depends('state')
    def _compute_color(self):
        color_map = {
            'draft': 0,
            'validated': 4,
            'paid': 10,
        }
        for rec in self:
            rec.color = color_map.get(rec.state, 0)

    def action_validate(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'validated'

    def action_mark_paid(self):
        for rec in self:
            if rec.state == 'validated':
                rec.state = 'paid'

    def action_reset_draft(self):
        for rec in self:
            if rec.state in ('validated', 'paid'):
                rec.state = 'draft'


class RestaurantTipPool(models.Model):

    _name = 'restaurant.tip.pool'
    _description = 'Répartition des pourboires'
    _order = 'date_from desc'

    name = fields.Char(
        string='Référence',
        compute='_compute_name',
        store=True,
    )
    date_from = fields.Date(
        string='Du',
        required=True,
    )
    date_to = fields.Date(
        string='Au',
        required=True,
    )
    total_tips = fields.Float(
        string='Total pourboires',
        compute='_compute_total_tips',
        store=True,
    )
    line_ids = fields.One2many(
        comodel_name='restaurant.tip.pool.line',
        inverse_name='pool_id',
        string='Distribution',
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Brouillon'),
            ('calculated', 'Calculé'),
            ('distributed', 'Distribué'),
        ],
        string='Statut',
        default='draft',
        required=True,
    )

    @api.depends('date_from', 'date_to')
    def _compute_name(self):
        for rec in self:
            date_from_str = rec.date_from.strftime('%d/%m/%Y') if rec.date_from else '?'
            date_to_str = rec.date_to.strftime('%d/%m/%Y') if rec.date_to else '?'
            rec.name = f"Pool {date_from_str} → {date_to_str}"

    @api.depends('line_ids.total_amount')
    def _compute_total_tips(self):
        for rec in self:
            rec.total_tips = sum(rec.line_ids.mapped('total_amount'))

    def action_calculate(self):
        for rec in self:
            rec.line_ids.unlink()
            tips = self.env['restaurant.tip'].search([
                ('tip_date', '>=', rec.date_from),
                ('tip_date', '<=', rec.date_to),
                ('state', '=', 'validated'),
            ])
            if not tips:
                rec.state = 'calculated'
                continue
            employee_data = {}
            for tip in tips:
                emp_id = tip.employee_id.id
                if emp_id not in employee_data:
                    employee_data[emp_id] = {'count': 0, 'total': 0.0}
                employee_data[emp_id]['count'] += 1
                employee_data[emp_id]['total'] += tip.amount
            grand_total = sum(d['total'] for d in employee_data.values())
            lines_vals = []
            for emp_id, data in employee_data.items():
                share = (data['total'] / grand_total * 100) if grand_total else 0.0
                lines_vals.append({
                    'pool_id': rec.id,
                    'employee_id': emp_id,
                    'tip_count': data['count'],
                    'total_amount': data['total'],
                    'share_percentage': share,
                    'amount_to_pay': data['total'],
                })
            self.env['restaurant.tip.pool.line'].create(lines_vals)
            rec.state = 'calculated'

    def action_distribute(self):
        for rec in self:
            if rec.state == 'calculated':
                rec.state = 'distributed'


class RestaurantTipPoolLine(models.Model):

    _name = 'restaurant.tip.pool.line'
    _description = 'Ligne de répartition des pourboires'

    pool_id = fields.Many2one(
        comodel_name='restaurant.tip.pool',
        string='Répartition',
        required=True,
        ondelete='cascade',
    )
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employé',
        required=True,
    )
    tip_count = fields.Integer(
        string='Nombre de pourboires',
    )
    total_amount = fields.Float(
        string='Montant total',
    )
    share_percentage = fields.Float(
        string='Part (%)',
    )
    amount_to_pay = fields.Float(
        string='À verser (€)',
    )
