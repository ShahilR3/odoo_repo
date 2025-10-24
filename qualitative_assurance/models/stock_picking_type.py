# -*- coding: utf-8 -*-

from odoo import fields,models

class StockPickingType(models.Model):
    _inherit = "stock.picking"

    quality_assurance_id = fields.Many2one('quality.assurance')

    def button_validate(self):
        """Adding additional performances"""
        for rec in self.move_ids:
            quality = self.env['quality.assurance'].search([('product_id','=',rec.product_id.id),
                                                       ('invoice_line_ids.operation_type_id','=',self.picking_type_id)])
        if quality:
            alert = self.env['quality.alert'].create({
                'product_id':self.move_ids.product_id.id,
                'create_uid':self.env.user.id,
                'source_name':self.name,
                'name':self.quality.name,
                'assigned':self.env.user.id,
            })
            return {
                'name': 'Quality Alert Form',
                'type': 'ir.actions.act_window',
                'res_id': alert.id,
                'res_model': 'quality.alert',
                'view_mode': 'form',
                'target': 'current',
            }
