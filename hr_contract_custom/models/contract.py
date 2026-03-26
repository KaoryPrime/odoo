from odoo import models, fields

class HrContract(models.Model):
    _inherit = 'hr.contract'

    name = fields.Char(string="Contract Reference", required=True)

    def action_print_contract(self):
        return self.env.ref('hr_contract_custom.action_report_contract_html').report_action(self)