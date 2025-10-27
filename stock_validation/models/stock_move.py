# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import ValidationError

class StockMove(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        today = fields.Date.today()
        for line in self.move_ids:
            exp_date = line.lot_ids.expiration_date
            if today > exp_date:
                raise ValidationError("Cannot Perform action")
        res = super().button_validate()
        return res
