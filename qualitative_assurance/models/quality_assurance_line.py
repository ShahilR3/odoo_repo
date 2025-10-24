# -*- coding:utf-8 -*-

from odoo import fields, models


class QualityOperationLine(models.Model):
    _name = 'quality.assurance.line'
    _description = 'Quality Assurance Line'

    quality_assurance_id = fields.Many2one('quality.assurance', string="Quality Assurance", ondelete="cascade")
    operation_type_id = fields.Many2one('stock.picking.type', string="Operation Type")
    warehouse_id = fields.Many2one(related='operation_type_id.warehouse_id', string="Warehouse")
    sequence_id = fields.Many2one(related='operation_type_id.sequence_id', string="Sequence")
