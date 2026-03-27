from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import config

SECTION_LINES = [
    Command.create({
        "name": "Even week",
        "dayofweek": "0",
        "sequence": 0,
        "hour_from": 0,
        "day_period": "morning",
        "week_type": "0",
        "hour_to": 0,
        "display_type": "line_section",
    }),
    Command.create({
        "name": "Odd week",
        "dayofweek": "0",
        "sequence": 25,
        "hour_from": 0,
        "day_period": "morning",
        "week_type": "1",
        "hour_to": 0,
        "display_type": "line_section",
    }),
]

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    comment = fields.Html(string='Notes')

    calendar_ids = fields.One2many(
        comodel_name="hr.employee.calendar",
        inverse_name="employee_id",
        string="Calendar planning",
        copy=True,
    )

    @api.model
    def default_get(self, fields_list):
        """Set calendar_ids default value to cover all use cases."""
        vals = super().default_get(fields_list)
        if "calendar_ids" in fields_list and not vals.get("calendar_ids"):
            vals["calendar_ids"] = [
                Command.create({
                    "calendar_id": self.env.company.resource_calendar_id.id,
                }),
            ]
        return vals

    def _regenerate_calendar(self):
        self.ensure_one()
        vals_list = []
        two_weeks = bool(
            self.calendar_ids.mapped("calendar_id").filtered("two_weeks_calendar")
        )
        if self.resource_id.calendar_id.auto_generate:
            self.resource_calendar_id.attendance_ids.unlink()
            self.resource_calendar_id.two_weeks_calendar = two_weeks
        seq = 0
        for week in (["0", "1"] if two_weeks else ["0"]):
            if two_weeks:
                section = SECTION_LINES[int(week)]
                section_data = dict(section[2])
                section_data["sequence"] = seq
                vals_list.append(Command.create(section_data))
                seq += 1
            for line in self.calendar_ids:
                if line.calendar_id.two_weeks_calendar:
                    attendances = line.calendar_id.attendance_ids.filtered(
                        lambda x, w=week: x.week_type == w
                    )
                else:
                    attendances = line.calendar_id.attendance_ids
                for attendance_line in attendances:
                    if attendance_line.display_type == "line_section":
                        continue
                    data = attendance_line.copy_data(
                        {
                            "calendar_id": self.resource_calendar_id.id,
                            "date_from": line.date_start,
                            "date_to": line.date_end,
                            "week_type": week if two_weeks else False,
                            "sequence": seq,
                        }
                    )[0]
                    seq += 1
                    vals_list.append(Command.create(data))
        if not self.resource_id.calendar_id.auto_generate:
            self.resource_id.calendar_id = (
                self.env["resource.calendar"]
                .create(
                    {
                        "active": False,
                        "company_id": self.company_id.id,
                        "auto_generate": True,
                        "name": _("Auto generated calendar for employee %s") % self.name,
                        "attendance_ids": vals_list,
                        "two_weeks_calendar": two_weeks,
                        "tz": self.tz,
                    }
                )
                .id
            )
        else:
            self.resource_calendar_id.attendance_ids = vals_list
        if self.calendar_ids:
            self.resource_id.calendar_id.hours_per_day = (
                self.calendar_ids[0].calendar_id.hours_per_day
            )
            self.resource_id.calendar_id.global_leave_ids = [
                Command.set(self.copy_global_leaves()),
            ]

    def copy_global_leaves(self):
        self.ensure_one()
        leave_ids = []
        for calendar in self.calendar_ids:
            global_leaves = calendar.calendar_id.global_leave_ids
            if calendar.date_start:
                global_leaves = global_leaves.filtered(
                    lambda x, ds=calendar.date_start: x.date_from.date() >= ds
                )
            if calendar.date_end:
                global_leaves = global_leaves.filtered(
                    lambda x, de=calendar.date_end: x.date_to.date() <= de
                )
            leave_ids += global_leaves.ids
        vals = [
            leave.copy_data({})[0]
            for leave in self.env["resource.calendar.leaves"].browse(leave_ids)
        ]
        return self.env["resource.calendar.leaves"].create(vals).ids

    def regenerate_calendar(self):
        for item in self:
            item._regenerate_calendar()

    def copy(self, default=None):
        self.ensure_one()
        new = super().copy(default)
        new.resource_id.calendar_id = fields.first(new.calendar_ids).calendar_id
        new.filtered("calendar_ids").regenerate_calendar()
        return new

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        if (
            not self.env.context.get("skip_employee_calendars_required")
            and not config["test_enable"]
            and res.filtered(lambda x: not x.calendar_ids)
        ):
            raise UserError(_("You can not create employees without any calendar."))
        res.filtered("calendar_ids").regenerate_calendar()
        return res

class HrEmployeeCalendar(models.Model):
    _name = "hr.employee.calendar"
    _description = "Employee Calendar"
    _order = "date_end desc"

    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")
    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Employee",
        required=True,
        ondelete="cascade",
    )
    company_id = fields.Many2one(related="employee_id.company_id")
    calendar_id = fields.Many2one(
        comodel_name="resource.calendar",
        string="Working Time",
        required=True,
        check_company=True,
        ondelete="restrict",
    )

    _sql_constraints = [
        (
            "date_consistency",
            "CHECK(date_start IS NULL OR date_end IS NULL OR date_start <= date_end)",
            "End date must be greater than or equal to start date.",
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for employee in records.mapped("employee_id"):
            employee._regenerate_calendar()
        return records

    def write(self, vals):
        res = super().write(vals)
        for employee in self.mapped("employee_id"):
            employee._regenerate_calendar()
        return res

    def unlink(self):
        employees = self.mapped("employee_id")
        res = super().unlink()
        for employee in employees:
            employee._regenerate_calendar()
        return res
