# -*- coding:utf-8 -*-

from odoo import fields,models


class EstateTags(models.Model):
    _name = "estate.property.tags"
    _description = "Tags for Property"
    _order = "name desc"

    name = fields.Char('Tags', required=True)
    colors = fields.Integer('Color')
    tag_ids = fields.One2many('estate.property', 'es_tag_ids')
