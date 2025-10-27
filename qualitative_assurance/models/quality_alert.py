# -*- coding: utf-8 -*-

from odoo import api, fields, models

class QualityAlert(models.Model):
    _name = "quality.alert"
    _description = "Quality Alert"

    name = fields.Char(readonly=True, default='New', copy=False)
    product_id = fields.Many2one("product.product", string="Products")
    quality_assure_id = fields.Many2one('quality.assure', string="Quality Assure")
    source_name = fields.Char("Source Operation")
    assigned_id = fields.Many2one('res.users', string="Assigned To", default=lambda self: self.create_uid)
    picking_id = fields.Many2one('stock.picking', string="Transfer")
    quality_alert_line_ids = fields.One2many('quality.alert.line','quality_alert_id')

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the model """
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('quality.alert')
        return super().create(vals_list)

    def action_validate(self):
        """To Validate the button"""
        for move in self.quality_alert_line_ids:
            test = self.env['quality.test'].search([('product_id','=',self.product_id.id),
                                                    ('measure','=',move.quality_name),
                                                    ('quality_alert','=',self.name)])
            if test:
                return{
                    'name': "Quality Test",
                    'view_mode': 'form',
                    'res_model': 'quality.test',
                    'res_id': test.id,
                    'type': 'ir.actions.act_window',
                    'target': 'current',
                }
            else:
                test = self.env['quality.test'].create({
                    'quality_assured_id':move.quality_assured_id.id,
                    'quality_alert_id': self.id,
                    'product_id':self.product_id.id,
                    'assigned_id':self.assigned_id.id,
                })
                return {
                    'name': "Quality Test",
                    'view_mode': 'form',
                    'res_model': 'quality.test',
                    'res_id': test.id,
                    'type': 'ir.actions.act_window',
                    'target': 'current',
                }
