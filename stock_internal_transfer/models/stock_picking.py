# -*- coding: utf-8 -*-

from odoo import models
from odoo.exceptions import ValidationError

class StockMove(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        """Assigning a user for confirmation"""
        if self.create_uid == self.env.user and self.picking_type_code == 'internal':
            raise ValidationError("You cannot Validate")
        res = super().button_validate()
        return res