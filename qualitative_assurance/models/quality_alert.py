# -*- coding: utf-8 -*-

from odoo import api, fields, models

class QualityAlert(models.Model):
    _name = "quality.alert"

    name = fields.Char(readonly=True, default='New', copy=False)
    product_id = fields.Many2one("product.product", string="Products")
    source_name = fields.Char("Source Operation")
    assigned_id = fields.Many2one('res.users', string="Assigned To", default=lambda self: self.create_uid)
    quality_assured_id = fields.Many2one('quality.assurance')
    quality_name = fields.Char(related="quality_assured_id.name")
    quanti_result = fields.Float(string="Quantitative Result")
    quali_result = fields.Char(string="Qualitative Result")
    result = fields.Selection(selection=([('pass','Passed'),('fail','Failed')]), string="Result")

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the model """
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('quality.alert')
        return super().create(vals_list)
