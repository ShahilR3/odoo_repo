# -*- coding: utf-8 -*-

from odoo import api, fields, models

class QualityTest(models.Model):
    _name = "quality.test"
    _description = "Quality Test"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(related="quality_assured_id.name")
    quality_assured_id = fields.Many2one('quality.assurance')
    quality_alert_id = fields.Many2one('quality.alert',string="Quality Alert")
    test_type = fields.Selection(related="quality_assured_id.type", string="Test Type")
    measure = fields.Char(related="quality_assured_id.name", string="Measure")
    result = fields.Selection(selection=([('satisfied', 'Satisfied'), ('none', 'Not Satisfied')]), string="Result",
                              tracking=True)
    status = fields.Selection(selection=([('pass','Passed'),('fail','Failed')]), string="Result",
                              compute="_compute_status", inverse="_inverse_status")
    quality_alert = fields.Char(related="quality_alert_id.name", string="Quality Alert")
    product_id = fields.Many2one(related="quality_alert_id.product_id", commodel_name="product.product")
    assigned_id = fields.Many2one('res.users', string="Assigned To", related="quality_alert_id.assigned_id")

    @api.depends('result')
    def _compute_status(self):
        """Changing the status with respect to result"""
        for rec in self:
            if rec.result == "satisfied":
                rec.write({'status': 'pass'})
            else:
                rec.write({'status': 'fail'})

    def _inverse_status(self):
        """Changing the result in the Alert view"""
        for rec in self:
            if rec.status == 'pass':
                rec.quality_alert_id.quality_alert_line_ids.quality_result = 'Satisfied'
                rec.quality_alert_id.quality_alert_line_ids.result = 'pass'
            else:
                rec.quality_alert_id.quality_alert_line_ids.quality_result = 'Not Satisfied'
                rec.quality_alert_id.quality_alert_line_ids.result = 'fail'
