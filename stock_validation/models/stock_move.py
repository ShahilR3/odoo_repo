# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class StockMove(models.Model):
    _inherit = "stock.picking"

    @api.onchange('state')
    def expiry_date(self):
        today = fields.Date.today()
        print(self.expiry_date)
        for line in self.move_ids_without_package:
            exp_date = line.lot_ids.expiration_date
            if today < exp_date and self.state == 'assigned':
                raise ValidationError("Cannot Perform action")