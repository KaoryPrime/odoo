from odoo import models, fields, api
from odoo.exceptions import UserError
import uuid

class ManualReconcileWizard(models.TransientModel):
    _name = 'manual.reconcile.wizard'
    _description = 'Assistant Lettrage Manuel'

    move_ids = fields.Many2many('account.move', string='Factures à lettrer',
                                domain=[('state', '=', 'posted')])
    payment_ids = fields.Many2many('account.payment', string='Paiements à lettrer')
    partner_id = fields.Many2one('res.partner', string='Client', readonly=True)

    @api.onchange('move_ids')
    def _onchange_move_ids(self):
        if self.move_ids:
            self.partner_id = self.move_ids[0].partner_id
        else:
            self.partner_id = False

    def action_create_payment(self):
        if not self.move_ids:
            raise UserError("Veuillez d'abord sélectionner une facture.")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Enregistrer un paiement',
            'res_model': 'account.payment.register',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_model': 'account.move',
                'active_ids': self.move_ids.ids,
            }
        }

    def action_manual_reconcile(self):
        if not self.move_ids or not self.payment_ids:
            raise UserError("Veuillez sélectionner au moins une facture et un paiement.")
        ref = str(uuid.uuid4())[:8].upper()
        self.move_ids.write({'lettrage_ref': ref})
        self.payment_ids.write({'lettrage_ref': ref})