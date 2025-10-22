from odoo import fields,models

class EstateTags(models.Model):
    _name = "estate.property.tags"
    _description = "Tags for Property"
    _sql_constraints = [('unique_tag_name','UNIQUE(name)', 'The tag name must be unique')]
    _order = "name desc"
    name = fields.Char('Tags',required=True)
    colors = fields.Integer('Color')
    tag_ids = fields.One2many('estate.property','es_tag')