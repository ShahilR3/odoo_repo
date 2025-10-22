# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleState(models.Model):
    """New states for delivery status"""
    _inherit = "sale.order"

    new_state = fields.Selection(selection=[('open', 'Open'),
                                            ('close', 'Close'),
                                            ('read', 'read')],
                                 default='open', compute="_compute_all_deliveries_done", inverse="_inverse_state")

    @api.depends('picking_ids.state')
    def _compute_all_deliveries_done(self):
        """Changing the state to close when all deliveries are done"""
        for rec in self:
            all_deliveries_done = rec.picking_ids and all(pick.state == 'done' for pick in rec.picking_ids)
            if all_deliveries_done:
                rec.new_state = 'close'

    def _inverse_state(self):
        for rec in self:
            if rec.new_state == 'open' and rec.picking_ids and all(pick.state == 'done' for pick in rec.picking_ids):
                raise ValidationError("Cannot change state")
