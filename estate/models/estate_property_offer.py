# -*- coding: utf-8 -*-

import datetime
from datetime import timedelta

from odoo import api, fields, models


class EstateOffers(models.Model):
    _name = "estate.property.offer"
    _description = "Offers given to the estate"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection(selection=[('accept', 'Accepted'),('refuse', 'Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    val_date = fields.Integer("Validity Date", default=7)
    dead_line = fields.Datetime("Deadline", compute='_time_cal', inverse='_inverse', store=True)
    property_type_id = fields.Many2one(related="property_id.type_id", store=True)

    @api.depends('val_date')
    def _time_cal(self):
        for record in self:
            if record.create_date:
                record.dead_line = record.create_date + timedelta(days=record.val_date)
            else:
                record.create_date = datetime.date.today()
                record.dead_line = record.create_date + timedelta(days=record.val_date)

    def _inverse(self):
        if self.create_date and self.dead_line:
            self.val_date = (self.dead_line - self.create_date).days

    def action_tick(self):
        self.status = 'accept'
        self.property_id.selling_price = self.price
        self.property_id.vendor = self.partner_id
        self.property_id.state = 'accept'

    def action_wrong(self):
        self.status = 'refuse'
