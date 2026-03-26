# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrShiftConfig(models.Model):
    _name = 'hr.shift.config'
    _description = 'Configuration des règles RH pour les shifts'
    _rec_name = 'name'

    name = fields.Char(
        string='Nom de la configuration',
        required=True,
        default='Configuration par défaut',
    )
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Société',
        default=lambda self: self.env.company,
        required=True,
    )

    # ── Règles configurables ───────────────────────────────────────────────────
    min_break_minutes = fields.Integer(
        string='Pause minimale entre shifts (minutes)',
        default=30,
        help="Durée minimale de pause obligatoire entre deux shifts d'un même employé.",
    )
    max_hours_per_day = fields.Float(
        string='Heures max par jour',
        default=8.0,
        help="Nombre maximum d'heures de travail autorisées par jour et par employé.",
    )
    min_shift_duration = fields.Float(
        string='Durée minimale d\'un shift (heures)',
        default=2.0,
        help="Durée minimale en heures qu'un shift doit avoir.",
    )
    max_shift_duration = fields.Float(
        string='Durée maximale d\'un shift (heures)',
        default=4.0,
        help="Durée maximale en heures qu'un shift peut avoir.",
    )
    enforce_max_hours = fields.Boolean(
        string='Bloquer si dépassement heures/jour',
        default=True,
        help="Si activé, empêche la création d'un shift si le total journalier dépasse le maximum.",
    )
    enforce_min_break = fields.Boolean(
        string='Bloquer si pause insuffisante',
        default=True,
        help="Si activé, empêche la création d'un shift si la pause avec le précédent est insuffisante.",
    )

    @api.constrains('min_break_minutes', 'max_hours_per_day', 'min_shift_duration', 'max_shift_duration')
    def _check_config_values(self):
        for config in self:
            if config.min_break_minutes < 0:
                raise ValidationError(_("La pause minimale ne peut pas être négative."))
            if config.max_hours_per_day <= 0:
                raise ValidationError(_("Les heures max par jour doivent être positives."))
            if config.min_shift_duration < 0:
                raise ValidationError(_("La durée minimale ne peut pas être négative."))
            if config.max_shift_duration <= 0:
                raise ValidationError(_("La durée maximale doit être positive."))
            if config.min_shift_duration > config.max_shift_duration:
                raise ValidationError(_(
                    "La durée minimale d'un shift ne peut pas dépasser la durée maximale."
                ))

    @api.model
    def get_config(self):
        """Retourne la configuration active pour la société courante."""
        config = self.search([
            ('company_id', '=', self.env.company.id),
            ('active', '=', True),
        ], limit=1)
        if not config:
            # Créer une config par défaut si aucune n'existe
            config = self.create({
                'name': 'Configuration par défaut',
                'company_id': self.env.company.id,
            })
        return config
