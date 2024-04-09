# -*- coding: utf-8 -*-
from logging import getLogger

from odoo import api, fields, models


class Brand(models.Model):
    _inherit = "res.brand"

    background_image = fields.Binary(string="Background Image", attachment=True,
                                     help="Upload a background image in pdf/jpeg format for best result. "
                                          "Warning: do not use png with transparent background")
