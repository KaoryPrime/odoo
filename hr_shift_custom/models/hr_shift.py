# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import Command, _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)


class HrShift(models.Model):
    _name = 'hr.shift'
    _description = 'Shift employé'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_time desc'
    _rec_name = 'name'

    # ── Champs principaux ─────────────────────────────────────────────────────

    name = fields.Char(
        string='Nom du shift',
        required=True,
        tracking=True,
    )
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employé',
        required=True,
        tracking=True,
        index=True,
    )
    department_id = fields.Many2one(
        comodel_name='hr.department',
        string='Département',
        related='employee_id.department_id',
        store=True,
    )
    start_time = fields.Datetime(
        string='Heure de début',
        required=True,
        tracking=True,
    )
    end_time = fields.Datetime(
        string='Heure de fin',
        required=True,
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Brouillon'),
            ('confirmed', 'Confirmé'),
            ('done', 'Terminé'),
            ('cancelled', 'Annulé'),
        ],
        string='Statut',
        default='draft',
        required=True,
        tracking=True,
    )
    color = fields.Integer(
        string='Couleur',
        compute='_compute_color',
        store=True,
    )
    note = fields.Text(string='Notes')
    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company,
        required=True,
    )

    # ── Champs calculés ───────────────────────────────────────────────────────

    duration = fields.Float(
        string='Durée (heures)',
        compute='_compute_duration',
        store=True,
        help="Durée du shift en heures.",
    )
    duration_display = fields.Char(
        string='Durée',
        compute='_compute_duration',
        store=True,
    )
    warning_message = fields.Char(
        string='Avertissement',
        compute='_compute_warning_message',
    )

    # ── Compute ───────────────────────────────────────────────────────────────

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for shift in self:
            if shift.start_time and shift.end_time and shift.end_time > shift.start_time:
                delta = (shift.end_time - shift.start_time).total_seconds()
                hours = delta / 3600
                shift.duration = hours
                h = int(hours)
                m = int((hours - h) * 60)
                shift.duration_display = f"{h}h{m:02d}"
            else:
                shift.duration = 0.0
                shift.duration_display = '—'

    @api.depends('state')
    def _compute_color(self):
        color_map = {
            'draft': 0,       # gris
            'confirmed': 4,   # bleu
            'done': 10,       # vert
            'cancelled': 1,   # rouge
        }
        for shift in self:
            shift.color = color_map.get(shift.state, 0)

    @api.depends('start_time', 'end_time', 'employee_id')
    def _compute_warning_message(self):
        """
        Calcule les avertissements non bloquants pour l'affichage dans la vue.
        Distinct des contraintes bloquantes.
        """
        for shift in self:
            if not shift.start_time or not shift.end_time:
                shift.warning_message = False
                continue
            config = self.env['hr.shift.config'].get_config()
            duration = (shift.end_time - shift.start_time).total_seconds() / 3600
            warnings = []
            if duration < config.min_shift_duration:
                warnings.append(
                    _("⚠️ Durée inférieure au minimum recommandé (%.1fh).") % config.min_shift_duration
                )
            if duration > config.max_shift_duration:
                warnings.append(
                    _("⚠️ Durée supérieure au maximum recommandé (%.1fh).") % config.max_shift_duration
                )
            shift.warning_message = ' '.join(warnings) if warnings else False

    # ── Contraintes ───────────────────────────────────────────────────────────

    @api.constrains('start_time', 'end_time', 'employee_id', 'company_id')
    def _check_shift_rules(self):
        for shift in self:
            if not shift.start_time or not shift.end_time:
                continue

            # 1. Cohérence début/fin
            if shift.start_time >= shift.end_time:
                raise ValidationError(
                    _("L'heure de début doit être antérieure à l'heure de fin.")
                )

            config = self.env['hr.shift.config'].get_config()

            # 2. Pause minimale entre shifts (configurable)
            if config.enforce_min_break:
                last_shift = self.search([
                    ('employee_id', '=', shift.employee_id.id),
                    ('end_time', '<=', shift.start_time),
                    ('state', 'not in', ['cancelled']),
                    ('id', '!=', shift.id),
                ], order='end_time desc', limit=1)

                if last_shift:
                    pause = shift.start_time - last_shift.end_time
                    min_break = timedelta(minutes=config.min_break_minutes)
                    if pause < min_break:
                        raise ValidationError(_(
                            "Pause insuffisante : il doit y avoir au moins %(min)d minutes "
                            "de pause entre deux shifts (pause actuelle : %(actual)d min)."
                        ) % {
                            'min': config.min_break_minutes,
                            'actual': int(pause.total_seconds() / 60),
                        })

                # Vérifier aussi le shift suivant
                next_shift = self.search([
                    ('employee_id', '=', shift.employee_id.id),
                    ('start_time', '>=', shift.end_time),
                    ('state', 'not in', ['cancelled']),
                    ('id', '!=', shift.id),
                ], order='start_time asc', limit=1)

                if next_shift:
                    pause = next_shift.start_time - shift.end_time
                    min_break = timedelta(minutes=config.min_break_minutes)
                    if pause < min_break:
                        raise ValidationError(_(
                            "Pause insuffisante avec le shift suivant : "
                            "%(min)d minutes requises (actuelle : %(actual)d min)."
                        ) % {
                            'min': config.min_break_minutes,
                            'actual': int(pause.total_seconds() / 60),
                        })

            # 3. Durée maximale par jour (UTC-safe)
            if config.enforce_max_hours:
                # Bornes de la journée en UTC à partir du datetime du shift
                day_start = shift.start_time.replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                day_end = shift.start_time.replace(
                    hour=23, minute=59, second=59, microsecond=999999
                )
                day_shifts = self.search([
                    ('employee_id', '=', shift.employee_id.id),
                    ('start_time', '>=', day_start),
                    ('start_time', '<=', day_end),
                    ('state', 'not in', ['cancelled']),
                    ('id', '!=', shift.id),
                ])
                total_worked = sum(s.duration for s in day_shifts)
                total_worked += (shift.end_time - shift.start_time).total_seconds() / 3600

                if total_worked > config.max_hours_per_day:
                    raise ValidationError(_(
                        "Dépassement du maximum journalier : %(total).1fh prévues "
                        "pour %(employee)s ce jour (max : %(max).1fh)."
                    ) % {
                        'total': total_worked,
                        'employee': shift.employee_id.name,
                        'max': config.max_hours_per_day,
                    })

            # 4. Chevauchement de shifts
            overlapping = self.search([
                ('employee_id', '=', shift.employee_id.id),
                ('state', 'not in', ['cancelled']),
                ('id', '!=', shift.id),
                ('start_time', '<', shift.end_time),
                ('end_time', '>', shift.start_time),
            ])
            if overlapping:
                raise ValidationError(_(
                    "Ce shift chevauche un shift existant de %(employee)s "
                    "(%(shift)s)."
                ) % {
                    'employee': shift.employee_id.name,
                    'shift': overlapping[0].name,
                })

    # ── Actions de workflow ───────────────────────────────────────────────────

    def action_confirm(self):
        for shift in self:
            if shift.state == 'draft':
                shift.state = 'confirmed'
                shift.message_post(body=_("Shift confirmé."))

    def action_done(self):
        for shift in self:
            if shift.state == 'confirmed':
                shift.state = 'done'
                shift.message_post(body=_("Shift marqué comme terminé."))

    def action_cancel(self):
        for shift in self:
            if shift.state in ('draft', 'confirmed'):
                shift.state = 'cancelled'
                shift.message_post(body=_("Shift annulé."))

    def action_reset_draft(self):
        for shift in self:
            if shift.state == 'cancelled':
                shift.state = 'draft'
                shift.message_post(body=_("Shift remis en brouillon."))

    # ── ORM ───────────────────────────────────────────────────────────────────

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        return records

    def write(self, vals):
        # Empêcher la modification d'un shift terminé ou annulé
        for shift in self:
            if shift.state in ('done', 'cancelled') and any(
                k in vals for k in ('start_time', 'end_time', 'employee_id')
            ):
                raise ValidationError(_(
                    "Impossible de modifier un shift terminé ou annulé. "
                    "Remettez-le en brouillon d'abord."
                ))
        return super().write(vals)
