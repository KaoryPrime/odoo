from odoo import Command, exceptions, fields
from odoo.tests import TransactionCase, new_test_user

from ..hooks import _split_calendars_for_employees

class TestHrEmployeeCalendarPlanning(TransactionCase):
    """
    Odoo 18 : SavepointCase est supprimé → TransactionCase.
    Chaque test tourne dans une transaction rollbackée automatiquement.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                mail_create_nolog=True,
                mail_create_nosubscribe=True,
                mail_notrack=True,
                no_reset_password=True,
                tracking_disable=True,
                test_hr_employee_calendar_planning=True,
            )
        )
        resource_calendar = cls.env["resource.calendar"]
        cls.calendar1 = resource_calendar.create(
            {"name": "Test calendar 1", "attendance_ids": []}
        )
        cls.calendar2 = resource_calendar.create(
            {"name": "Test calendar 2", "attendance_ids": []}
        )
        for day in range(5):
            cls.calendar1.attendance_ids = [
                Command.create({
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": 8,
                    "hour_to": 12,
                }),
                Command.create({
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": 13,
                    "hour_to": 17,
                }),
            ]
            cls.calendar2.attendance_ids = [
                Command.create({
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": 7,
                    "hour_to": 14,
                }),
            ]
        cls.employee = cls.env["hr.employee"].create({"name": "Test employee"})
        cls.leave1 = cls.env["resource.calendar.leaves"].create(
            {
                "name": "Test leave",
                "calendar_id": cls.calendar1.id,
                "resource_id": cls.employee.resource_id.id,
                "date_from": "2019-06-01 08:00:00",
                "date_to": "2019-06-10 17:00:00",
            }
        )
        cls.global_leave1 = cls.env["resource.calendar.leaves"].create(
            {
                "name": "Global Leave 1",
                "date_from": "2019-03-01 08:00:00",
                "date_to": "2019-03-02 17:00:00",
            }
        )
        cls.global_leave2 = cls.env["resource.calendar.leaves"].create(
            {
                "name": "Global Leave 2",
                "date_from": "2020-03-12 08:00:00",
                "date_to": "2020-03-13 17:00:00",
            }
        )
        cls.global_leave3 = cls.env["resource.calendar.leaves"].create(
            {
                "name": "Global Leave 3",
                "date_from": "2020-03-09 08:00:00",
                "date_to": "2020-03-10 17:00:00",
            }
        )
        cls.calendar1.global_leave_ids = [
            Command.set([cls.global_leave1.id, cls.global_leave2.id])
        ]
        cls.calendar2.global_leave_ids = [Command.set([cls.global_leave3.id])]
        cls.employee.write({"calendar_ids": [Command.delete(cls.employee.calendar_ids.id)]})

    def test_calendar_planning(self):
        self.employee.calendar_ids = [
            Command.create({"date_end": "2019-12-31", "calendar_id": self.calendar1.id}),
            Command.create({"date_start": "2020-01-01", "calendar_id": self.calendar2.id}),
        ]
        self.assertTrue(self.employee.resource_calendar_id)
        calendar = self.employee.resource_calendar_id
        self.assertEqual(len(calendar.attendance_ids), 15)
        self.assertEqual(
            len(calendar.attendance_ids.filtered(
                lambda x: x.date_from == fields.Date.to_date("2020-01-01")
            )),
            5,
        )
        self.assertEqual(
            len(calendar.attendance_ids.filtered(
                lambda x: x.date_to == fields.Date.to_date("2019-12-31")
            )),
            10,
        )
        calendar_line = self.employee.calendar_ids[0]
        calendar_line.date_end = "2019-12-30"
        calendar = self.employee.resource_calendar_id
        self.assertEqual(
            len(calendar.attendance_ids.filtered(
                lambda x: x.date_to == fields.Date.to_date("2019-12-30")
            )),
            10,
        )
        calendar_line.unlink()
        self.assertEqual(
            len(calendar.attendance_ids.filtered(
                lambda x: x.date_to == fields.Date.to_date("2019-12-30")
            )),
            0,
        )
        self.assertEqual(len(calendar.attendance_ids), 5)
        self.calendar2.write({
            "attendance_ids": [Command.create({
                "name": "Attendance",
                "dayofweek": "6",
                "hour_from": 8,
                "hour_to": 12,
            })],
        })
        self.assertEqual(len(calendar.attendance_ids), 6)

    def test_post_install_hook(self):
        self.employee.resource_calendar_id = self.calendar1.id
        _split_calendars_for_employees(self.env, self.employee)
        self.assertNotEqual(self.employee.resource_calendar_id, self.calendar1)
        self.assertEqual(len(self.calendar1.attendance_ids), 10)
        self.assertEqual(len(self.employee.calendar_ids), 1)
        self.assertFalse(self.employee.calendar_ids.date_start)
        self.assertFalse(self.employee.calendar_ids.date_end)
        self.assertEqual(
            self.calendar1.leave_ids, self.global_leave1 + self.global_leave2
        )
        self.assertIn(
            self.leave1.id, self.employee.resource_calendar_id.leave_ids.ids
        )

    def test_resource_calendar_constraint(self):
        self.employee.calendar_ids = [
            Command.create({"date_end": "2019-12-31", "calendar_id": self.calendar1.id})
        ]
        with self.assertRaises(exceptions.ValidationError):
            self.calendar1.write({"active": False})
        self.employee.write({
            "calendar_ids": [Command.delete(self.employee.calendar_ids.id)]
        })
        self.calendar1.write({"active": False})
        self.assertFalse(self.calendar1.active)

    def test_employee_with_calendar_ids(self):
        employee = self.env["hr.employee"].create({
            "name": "Test employee 2",
            "calendar_ids": [
                Command.create({
                    "date_start": "2020-01-01",
                    "calendar_id": self.calendar2.id,
                }),
            ],
        })
        self.assertTrue(employee.resource_calendar_id.auto_generate)

    def test_copy_global_leaves(self):
        self.employee.calendar_ids = [
            Command.create({"date_end": "2020-03-03", "calendar_id": self.calendar1.id}),
            Command.create({"date_start": "2020-03-03", "calendar_id": self.calendar2.id}),
        ]
        self.assertEqual(
            {gl.name for gl in self.employee.resource_calendar_id.global_leave_ids},
            {"Global Leave 1", "Global Leave 3"},
        )

    def test_employee_copy(self):
        self.employee.calendar_ids = [
            Command.create({"date_end": "2019-12-31", "calendar_id": self.calendar1.id}),
            Command.create({"date_start": "2020-01-01", "calendar_id": self.calendar2.id}),
        ]
        self.assertTrue(self.employee.resource_calendar_id)
        employee2 = self.employee.copy()
        self.assertIn(self.calendar1, employee2.mapped("calendar_ids.calendar_id"))
        self.assertIn(self.calendar2, employee2.mapped("calendar_ids.calendar_id"))
        self.assertTrue(employee2.resource_calendar_id.auto_generate)
        self.assertNotEqual(
            self.employee.resource_calendar_id, employee2.resource_calendar_id
        )

    def test_user_action_create_employee(self):
        user = new_test_user(self.env, login="test-user-cal")
        user.action_create_employee()
        self.assertIn(
            user.company_id.resource_calendar_id,
            user.employee_id.mapped("calendar_ids.calendar_id"),
        )
