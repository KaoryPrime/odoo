from odoo import api, fields, models


class CustomerFeedback(models.Model):

    _name = 'restaurant.customer.feedback'
    _description = 'Avis Client Restaurant'
    _inherit = ['mail.thread']
    _order = 'feedback_date desc, id desc'

    name = fields.Char(
        string='Référence',
        compute='_compute_name',
        store=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Client',
        index=True,
    )
    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Commande associée',
        index=True,
    )
    feedback_date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
    )
    rating_food = fields.Selection(
        selection=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        ],
        string='Qualité des plats',
        required=True,
    )
    rating_service = fields.Selection(
        selection=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        ],
        string='Qualité du service',
        required=True,
    )
    rating_ambiance = fields.Selection(
        selection=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        ],
        string='Ambiance',
    )
    rating_value = fields.Selection(
        selection=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        ],
        string='Rapport qualité/prix',
    )
    rating_overall = fields.Float(
        string='Note globale',
        compute='_compute_rating_overall',
        store=True,
        digits=(3, 2),
        group_operator='avg',
    )
    comment = fields.Text(
        string='Commentaire client',
    )
    response = fields.Text(
        string='Réponse du restaurant',
    )
    state = fields.Selection(
        selection=[
            ('new', 'Nouveau'),
            ('read', 'Lu'),
            ('responded', 'Répondu'),
            ('archived', 'Archivé'),
        ],
        string='Statut',
        default='new',
        required=True,
        tracking=True,
    )
    source = fields.Selection(
        selection=[
            ('on_site', 'Sur place'),
            ('google', 'Google'),
            ('website', 'Site web'),
            ('phone', 'Téléphone'),
            ('email', 'Email'),
        ],
        string='Source',
    )
    would_recommend = fields.Boolean(
        string='Recommanderait ?',
    )
    color = fields.Integer(
        string='Couleur',
        compute='_compute_color',
        store=True,
    )

    @api.depends('partner_id', 'feedback_date')
    def _compute_name(self):
        for rec in self:
            partner = rec.partner_id.name if rec.partner_id else 'Anonyme'
            date = rec.feedback_date or fields.Date.context_today(rec)
            rec.name = f"{partner} – {date}"

    @api.depends('rating_food', 'rating_service', 'rating_ambiance', 'rating_value')
    def _compute_rating_overall(self):
        for rec in self:
            ratings = []
            for field_name in ('rating_food', 'rating_service', 'rating_ambiance', 'rating_value'):
                val = rec[field_name]
                if val:
                    ratings.append(int(val))
            rec.rating_overall = sum(ratings) / len(ratings) if ratings else 0.0

    @api.depends('rating_overall')
    def _compute_color(self):
        for rec in self:
            if rec.rating_overall >= 4:
                rec.color = 10
            elif rec.rating_overall >= 3:
                rec.color = 2
            else:
                rec.color = 1

    def action_mark_read(self):
        for rec in self:
            if rec.state == 'new':
                rec.state = 'read'

    def action_respond(self):
        for rec in self:
            if rec.state in ('new', 'read'):
                rec.state = 'responded'

    def action_archive_feedback(self):
        for rec in self:
            if rec.state != 'archived':
                rec.state = 'archived'
