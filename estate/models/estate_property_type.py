from odoo import api
from odoo import fields,models

class EstateType(models.Model):
    _name = "estate.property.types"
    _description = "shows the property types"
    _sql_constraints = [('unique_type_name', 'UNIQUE(name_type)', 'The property type name must be unique')]
    _order = "name desc"

    name = fields.Char("Types",required=True)
    property_type = fields.One2many('estate.property', 'type_id', string = "Properties", store = True)
    sequence = fields.Integer('Sequence',default =1, help ="Used to order the fields")
    offer_ids = fields.One2many('estate.property.offer','property_type_id')
    offer_count =fields.Integer(compute = "_total_offers")


    @api.depends('offer_ids.price')
    def _total_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids.mapped('price'))

