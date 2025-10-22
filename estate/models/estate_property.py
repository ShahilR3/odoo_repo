from odoo import models,fields
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare
import datetime
from odoo import api
from odoo.exceptions import UserError, ValidationError


class TestModel(models.Model):
    _name = "estate.property"
    _description = "real estate business"
    _sql_constraints = [('price_expect','CHECK(expected_price > 0.00)','Expected price value must be strictly positive')]
    _order = 'id desc'

    type_id = fields.Many2one('estate.property.type', string = " Property Type")
    es_tag = fields.Many2many('estate.property.tags',string = "Tags")
    active = fields.Boolean(active = False)
    name = fields.Char('Name',default="Unknown")
    description = fields.Text('Description')
    postcode = fields.Char('Post Code')
    date_availability = fields.Date('Date available', default = datetime.date.today() + relativedelta(months=3),copy = False)
    expected_price = fields.Float('Expected Price')
    selling_price = fields.Float("Selling Price", readonly = True,copy = False)
    bedrooms = fields.Integer("Bedrooms", default = 2)
    living_area = fields.Integer("Living Area (sq)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden",active = False)
    garden_area = fields.Integer("Garden Area (sq)")
    orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string='Garden Orientation')
    state = fields.Selection(string = "Status", selection=[('new','New'),('receive','Offer Receive'),('accept','Offer Accepted'),('sold','Sold'),('cancel','Cancelled')])
    salesmen = fields.Many2one('res.users',string = "Salesman")
    vendor = fields.Many2one('res.partner',string = "Buyer")
    Offers = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(compute = '_compute_area')
    best_offer = fields.Float("Best Offer", readonly = True , compute = '_compute_offer')


    @api.depends('Offers.price')
    def _compute_offer(self):
        for record in self:
            if record.Offers:
                record.best_offer = max(record.Offers.mapped('price'))
            else:
                record.best_offer = 0.0


    @api.depends('living_area','garden_area')
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

    def sold(self):
        for record in self:
            if record.state == 'cancel':
                raise UserError("Cannot Perform this action. I am Sorry!! This Property is Cancelled")
            else:
                record.state = 'sold'
        return True

    def cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Cannot Perform this action. I am Sorry!! This Property is Sold")
            else:
                record.state = 'cancel'
        return True

    @api.constrains('selling_price')
    def _check_(self):
        for record in self:
            if float_compare(record.selling_price , ((90/100)*record.expected_price),precision_digits =2) == -1:
                raise ValidationError("Selling price cannot be this low")