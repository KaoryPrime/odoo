from collections import defaultdict

from odoo import SUPERUSER_ID, Command, api

def post_init_hook(env):
    """
    Odoo 18 : post_init_hook reçoit directement l'env, plus besoin de
    api.Environment.manage() ni de construire l'env manuellement.

    Split current calendars by date ranges and assign new ones for
    having proper initial data.
    """
    employees = env["hr.employee"].search([])
    _split_calendars_for_employees(env, employees)

def _split_calendars_for_employees(env, employees):
    """Logique extraite pour être réutilisable depuis les tests."""
    calendars = employees.mapped("resource_calendar_id")
    calendar_obj = env["resource.calendar"]
    line_obj = env["resource.calendar.attendance"]

    groups = line_obj.read_group(
        [("calendar_id", "in", calendars.ids)],
        ["calendar_id", "date_from", "date_to"],
        ["calendar_id", "date_from:day", "date_to:day"],
        lazy=False,
    )

    calendar_mapping = defaultdict(list)
    for group in groups:
        calendar = calendar_obj.browse(group["calendar_id"][0])
        lines = line_obj.search(group["__domain"])
        if len(calendar.attendance_ids) == len(lines):
            new_calendar = calendar
        else:
            name = "{} {}-{}".format(
                calendar.name,
                lines[0].date_from,
                lines[0].date_to,
            )
            attendances = []
            for line in lines:
                data = line.copy_data({"date_from": False, "date_to": False})[0]
                data.pop("calendar_id")
                attendances.append(Command.create(data))
            new_calendar = calendar_obj.create(
                {"name": name, "attendance_ids": attendances}
            )
        calendar_mapping[calendar].append(
            (lines[0].date_from, lines[0].date_to, new_calendar),
        )

    for employee in employees.filtered("resource_calendar_id"):
        calendar_lines = []
        for data in calendar_mapping[employee.resource_calendar_id]:
            calendar_lines.append(Command.create({
                "date_start": data[0],
                "date_end": data[1],
                "calendar_id": data[2].id,
            }))
        leaves = employee.resource_calendar_id.leave_ids.filtered(
            lambda x: x.resource_id == employee.resource_id
        )
        employee.calendar_ids = calendar_lines
        employee.resource_calendar_id.active = False
        leaves.write({"calendar_id": employee.resource_calendar_id.id})
