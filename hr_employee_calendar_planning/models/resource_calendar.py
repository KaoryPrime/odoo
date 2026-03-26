from odoo import Command, _, api, fields, models
from odoo.exceptions import ValidationError

class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    active = fields.Boolean(default=True)
    auto_generate = fields.Boolean(
        string="Auto Generated",
        help="Indicates this calendar is automatically generated for an employee "
             "and should not be edited manually.",
    )
    employee_calendar_ids = fields.One2many(
        comodel_name="hr.employee.calendar",
        inverse_name="calendar_id",
        string="Employee Plannings",
    )
    employee_count = fields.Integer(
        string="Employees using this calendar",
        compute="_compute_employee_count",
    )

    def _compute_employee_count(self):
        for record in self:
            record.employee_count = self.env["hr.employee.calendar"].search_count(
                [("calendar_id", "=", record.id)]
            )

    def action_view_employees(self):
        self.ensure_one()
        employee_ids = self.env["hr.employee.calendar"].search(
            [("calendar_id", "=", self.id)]
        ).mapped("employee_id").ids
        return {
            "type": "ir.actions.act_window",
            "name": _("Employees — %s") % self.name,
            "res_model": "hr.employee",
            "view_mode": "list,form",
            "domain": [("id", "in", employee_ids)],
        }

    @api.constrains("active")
    def _check_active(self):
        for item in self:
            total_items = self.env["hr.employee.calendar"].search_count(
                [
                    ("calendar_id", "=", item.id),
                    "|",
                    ("date_end", "=", False),
                    ("date_end", "<=", fields.Date.today()),
                ]
            )
            if total_items:
                raise ValidationError(
                    _("%(name)s is used in %(count)s employee(s). "
                      "You should change them first.")
                    % {"name": item.name, "count": total_items}
                )

    @api.constrains("company_id")
    def _check_company_id(self):
        for item in self.filtered("company_id"):
            total_items = self.env["hr.employee.calendar"].search_count(
                [
                    ("calendar_id.company_id", "=", item.company_id.id),
                    ("employee_id.company_id", "!=", item.company_id.id),
                    ("employee_id.company_id", "!=", False),
                ]
            )
            if total_items:
                raise ValidationError(
                    _("%(name)s is used in %(count)s employee(s) "
                      "related to another company.")
                    % {"name": item.name, "count": total_items}
                )

    def write(self, vals):
        res = super().write(vals)
        if "attendance_ids" in vals or "global_leave_ids" in vals:
            for record in self.filtered(lambda x: not x.auto_generate):
                calendars = self.env["hr.employee.calendar"].search(
                    [("calendar_id", "=", record.id)]
                )
                for employee in calendars.mapped("employee_id"):
                    employee._regenerate_calendar()
        return res
