from odoo import models, fields, api
from odoo.exceptions import UserError


class LoyaltyCard(models.Model):
    _name = 'restaurant.loyalty.card'
    _description = 'Carte de fidélité restaurant'

    name = fields.Char(
        string='Nom',
        compute='_compute_name',
        store=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True,
        ondelete='cascade',
    )
    card_number = fields.Char(
        string='Numéro de carte',
        readonly=True,
        copy=False,
    )
    points_balance = fields.Float(
        string='Solde de points',
        default=0,
        readonly=True,
    )
    total_points_earned = fields.Float(
        string='Total points gagnés',
        readonly=True,
    )
    total_points_spent = fields.Float(
        string='Total points dépensés',
        readonly=True,
    )
    tier = fields.Selection(
        [
            ('bronze', 'Bronze'),
            ('silver', 'Silver'),
            ('gold', 'Gold'),
            ('platinum', 'Platinum'),
        ],
        string='Niveau',
        compute='_compute_tier',
        store=True,
    )
    active = fields.Boolean(default=True)
    history_ids = fields.One2many(
        'restaurant.loyalty.points.history',
        'card_id',
        string='Historique',
    )

    @api.depends('partner_id', 'card_number')
    def _compute_name(self):
        for rec in self:
            partner_name = rec.partner_id.name or ''
            card_num = rec.card_number or ''
            rec.name = f"{partner_name} - {card_num}" if partner_name else card_num

    @api.depends('total_points_earned')
    def _compute_tier(self):
        for rec in self:
            if rec.total_points_earned >= 5000:
                rec.tier = 'platinum'
            elif rec.total_points_earned >= 2000:
                rec.tier = 'gold'
            elif rec.total_points_earned >= 500:
                rec.tier = 'silver'
            else:
                rec.tier = 'bronze'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('card_number'):
                vals['card_number'] = self._generate_card_number()
        return super().create(vals_list)

    def _generate_card_number(self):
        return self.env['ir.sequence'].next_by_code('restaurant.loyalty.card') or 'LOY-00000'

    def add_points(self, points, description=False, sale_order_id=False):
        for rec in self:
            rec.write({
                'points_balance': rec.points_balance + points,
                'total_points_earned': rec.total_points_earned + points,
            })
            self.env['restaurant.loyalty.points.history'].create({
                'card_id': rec.id,
                'points': points,
                'operation': 'earn',
                'description': description or 'Gain de points',
                'sale_order_id': sale_order_id,
            })

    def redeem_points(self, points, description=False):
        for rec in self:
            if rec.points_balance < points:
                raise UserError(
                    f"Solde insuffisant. Solde actuel : {rec.points_balance}, demandé : {points}"
                )
            rec.write({
                'points_balance': rec.points_balance - points,
                'total_points_spent': rec.total_points_spent + points,
            })
            self.env['restaurant.loyalty.points.history'].create({
                'card_id': rec.id,
                'points': points,
                'operation': 'redeem',
                'description': description or 'Utilisation de points',
            })

    def action_view_history(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Historique des points',
            'res_model': 'restaurant.loyalty.points.history',
            'view_mode': 'list,form',
            'domain': [('card_id', '=', self.id)],
            'context': {'default_card_id': self.id},
        }


class LoyaltyPointsHistory(models.Model):
    _name = 'restaurant.loyalty.points.history'
    _description = 'Historique des points de fidélité'
    _order = 'date desc'

    card_id = fields.Many2one(
        'restaurant.loyalty.card',
        string='Carte',
        required=True,
        ondelete='cascade',
    )
    partner_id = fields.Many2one(
        related='card_id.partner_id',
        string='Client',
        store=True,
    )
    date = fields.Datetime(
        string='Date',
        default=fields.Datetime.now,
    )
    points = fields.Float(
        string='Points',
        required=True,
    )
    operation = fields.Selection(
        [
            ('earn', 'Gain'),
            ('redeem', 'Utilisation'),
        ],
        string='Opération',
        required=True,
    )
    description = fields.Char(string='Description')
    sale_order_id = fields.Many2one(
        'sale.order',
        string='Commande associée',
    )
