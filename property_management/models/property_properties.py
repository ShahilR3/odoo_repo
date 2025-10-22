# -*- coding: utf-8 -*-

from odoo import fields, models, api


class PropertyProperties(models.Model):
    """Creating a property model and its fields"""
    _name = "property.properties"
    _description = "Property management details"
    _inherit = ['mail.thread']

    name = fields.Char('Name')
    active = fields.Boolean(default='True')
    address = fields.Char(default='Address')
    street = fields.Char()
    street2 = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one('res.country.state')
    country_id = fields.Many2one(related="state_id.country_id")
    zip = fields.Char()
    image_property = fields.Binary()
    description = fields.Text()
    build_date = fields.Date(string='Build Date')
    sold_option = fields.Boolean(string="Can be Sold", active=True)
    property_inter_ids = fields.One2many('property.intermediate', 'intermediate_management_id',
                                         ondelete='cascade')
    facility_ids = fields.Many2many('property.facility', string="Facilities Available", ondelete="cascade")
    owner_id = fields.Many2one('res.partner', string="Owner")
    company_id = fields.Many2one('res.company',  # pylin disable:line-too-long
                                 string='Company',
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one(related='company_id.currency_id', string="Currency")
    legal_amount = fields.Monetary(string="Legal Amount")
    rent = fields.Monetary(string="Rent")
    state = fields.Selection(
        string="State",
        selection=[('draft', 'Draft'),
                   ('rent', 'Rent'),
                   ('leased', 'Leased'),
                   ('sold', 'Sold')
                   ], default='draft', tracking=True)
    property_count = fields.Integer(string="Details", compute="_compute_property_count")

    @api.depends('property_inter_ids')
    def _compute_property_count(self):
        """To compute the number of count the property is used"""
        for record in self:
            record.property_count = len(record.property_inter_ids)

    def action_get_property(self):
        """To show the list view inside the smart button"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Property Intermediate',
            'res_id': self.id,
            'view_mode': 'list',
            'res_model': 'property.intermediate',
            'domain': (
                ['|', ('default_active_id', '=', self.env.context.get('active_id')),
                 ('intermediate_management_id', '=', self.id)]
                if self.env.context.get('active_id')
                else [('intermediate_management_id', '=', self.id)]
            ),
            'context': {'create': False},
        }
