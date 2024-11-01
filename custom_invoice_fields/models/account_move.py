from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    mileage = fields.Integer(string="Mileage")
    license_plate = fields.Char(string="License Plate")
