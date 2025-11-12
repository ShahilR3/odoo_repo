# -*- coding: utf-8 -*-


import datetime
from dateutil.relativedelta import relativedelta

from odoo import api,models,fields
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError, ValidationError


class TestModel(models.Model):
    _name = "estate.property"
    _description = "real estate business"
    _order = 'id desc'

    type_id = fields.Many2one('estate.property.type', string=" Property Type")
    es_tag_ids = fields.Many2many('estate.property.tags', string="Tags")
    active = fields.Boolean(default=False)
    name = fields.Char('Name')
    description = fields.Text('Description')
    postcode = fields.Char('Post Code')
    date_availability = fields.Date('Date available', default=datetime.date.today() + relativedelta(months=3),
                                    copy=False)
    expected_price = fields.Float('Expected Price')
    selling_price = fields.Float("Selling Price", readonly=True,
                                 copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sq)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden", default=False)
    garden_area = fields.Integer("Garden Area (sq)")
    orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string='Garden Orientation')
    state = fields.Selection(string="Status",
                             selection=[('new', 'New'), ('receive', 'Offer Receive'), ('accept', 'Offer Accepted'),
                                        ('sold', 'Sold'), ('cancel', 'Cancelled')])
    salesmen_id = fields.Many2one('res.users', string="Salesman")
    vendor_id = fields.Many2one('res.partner', string="Buyer")
    Offers_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(compute='_compute_area')
    best_offer = fields.Float("Best Offer", readonly=True, compute='_compute_offer')

    @api.depends('Offers_ids')
    def _compute_offer(self):
        for record in self:
            if record.Offers_ids:
                record.best_offer = max(record.Offers_ids.mapped('price'))
            else:
                record.best_offer = 0.0

    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.orientation = 'west'
        else:
            self.garden_area = 0
            self.orientation = ''

    def action_sold(self):
        if self.state == 'cancel':
            raise UserError("Cannot Perform this action. I am Sorry!! This Property is Cancelled")
        else:
            self.state = 'sold'

    def action_cancel(self):
        if self.state == 'sold':
            raise UserError("Cannot Perform this action. I am Sorry!! This Property is Sold")
        else:
            self.state = 'cancel'

    @api.constrains('selling_price')
    def _check_(self):
        for record in self:
            if float_compare(record.selling_price , ((90/100)*record.expected_price),precision_digits =2) == -1:
                raise ValidationError("Selling price cannot be this low")
