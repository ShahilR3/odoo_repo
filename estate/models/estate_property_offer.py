import datetime
from datetime import timedelta
from odoo import fields,models
from odoo import api

class EstateOffers(models.Model):
    _name = "estate.property.offer"
    _description = "Offers given to the estate"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection(selection=[('accept','Accepted'),('refuse','Refused')])
    partner_id = fields.Many2one('res.partner', required = True)
    property_id = fields.Many2one('estate.property',required = True)
    val_date = fields.Integer("Validity Date", default = 7)
    dead_line = fields.Datetime("Deadline", compute = '_time_cal', inverse = '_inverse',store = True)
    property_type_id = fields.Many2one(related = "property_id.type_id", stored = True)

    @api.depends('val_date')
    def _time_cal(self):
        for record in self:
            if record.create_date:
                record.dead_line = record.create_date + timedelta(days = record.val_date)
                print(record.dead_line)
            else:
                record.create_date = datetime.date.today()
                record.dead_line = record.create_date + timedelta(days=record.val_date)

    def _inverse(self):
        for record in self:
            if record.create_date and record.dead_line:
                record.val_date = (record.dead_line - record.create_date).days

    def tick(self):
        for record in self:
            record.status = 'accept'
            record.property_id.selling_price = record.price
            record.property_id.vendor = record.partner_id
            record.property_id.state = 'accept'
        return True

    def wrong(self):
        for record in self:
            record.status = 'refuse'
        return True
