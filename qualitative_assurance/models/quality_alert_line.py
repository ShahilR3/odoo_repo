# -*- coding: utf-8 -*-

from odoo import fields, models

class QualityAlertLine(models.Model):
    _name = "quality.alert.line"
    _description = "Quality Alert Line"

    quality_assured_id = fields.Many2one('quality.assurance')
    quality_name = fields.Char(related="quality_assured_id.name")
    assigned_id = fields.Many2one('res.users', string="Assigned To", default=lambda self: self.create_uid)
    quantity_result = fields.Float(string="Quantitative Result")
    quality_result = fields.Char(string="Qualitative Result")
    result = fields.Selection(selection=([('pass','Passed'),('fail','Failed')]), string="Result", default='')
    quality_alert_id = fields.Many2one('quality.alert',string="Quality Alert")
