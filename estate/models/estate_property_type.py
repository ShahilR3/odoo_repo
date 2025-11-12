from odoo import api
from odoo import fields,models

class EstateType(models.Model):
    _name = "estate.property.type"
    _description = "shows the property types"
    _order = "name desc"

    name = fields.Char("Types", required=True)
    property_type = fields.One2many('estate.property', 'type_id', string="Properties",
                                    store=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order the fields")
    offer_ids = fields.One2many('estate.property.offer','property_type_id')
    offer_count = fields.Integer(compute="_total_offers")

    @api.depends('offer_ids.price')
    def _total_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids.mapped('price'))
