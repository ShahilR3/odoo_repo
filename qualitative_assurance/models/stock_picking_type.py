# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.fields import Command
from odoo.exceptions import ValidationError


class StockPickingType(models.Model):
    _inherit = "stock.picking"

    quality_alert_count = fields.Integer(string="Quality Alerts", compute="_compute_quality_alert_count")
    quality_alert_ids = fields.Many2many('quality.alert', string="Quality Alerts",
                                         compute="_compute_quality_alert_count")

    @api.depends('move_ids')
    def _compute_quality_alert_count(self):
        """Computing the count of quality assurance"""
        QualityAlert = self.env['quality.alert']
        for picking in self:
            quality_assurance = self.env['quality.assurance'].search_count([
                ('product_id', 'in', picking.move_ids.product_id.ids)
            ])
            if quality_assurance:
                alerts = QualityAlert.search([('source_name', '=', picking.name)])
                picking.quality_alert_count = len(alerts)
                picking.quality_alert_ids = alerts
            else:
                picking.quality_alert_count = 0
                picking.quality_alert_ids = False

    def action_confirm(self):
        """Creating a Quality alert when it is in confirm stage"""
        QualityAlert = self.env['quality.alert']
        QualityAssurance = self.env['quality.assurance']
        for move in self.move_ids:
            quality = QualityAssurance.search([
                ('product_id', '=', move.product_id.id),
                ('quality_line_ids.operation_type_id', '=', self.picking_type_id.id)
            ])
            if not quality:
                continue
            existing_quality_alert = QualityAlert.search([
                ('source_name', '=', self.name),
                ('product_id', '=', move.product_id.id)
            ])
            if existing_quality_alert:
                continue
            else:
                alert_vals = {
                    'product_id': move.product_id.id,
                    'source_name': self.name,
                    'assigned_id': self.env.user.id,
                    'quality_alert_line_ids': [
                        Command.create({
                            'quality_assured_id': quality.id,
                            'assigned_id': self.env.user.id,
                        })
                    ],
                }
                QualityAlert.create(alert_vals)

        res = super().action_confirm()
        return res

    def button_validate(self):
        """Checking the Quality Test"""
        check = []
        length = len(self.move_ids)
        print(length)
        for move in self.move_ids:
            existing_quality_alert = self.env['quality.alert'].search([
                ('source_name', '=', self.name),
                ('product_id', '=', move.product_id.id)
            ])
            if existing_quality_alert.quality_alert_line_ids.result == 'pass':
                check.append("pass")
            elif existing_quality_alert.quality_alert_line_ids.result == 'fail':
                if length > 1:
                    move.quantity = 0.0
                else:
                    raise ValidationError('Quality Test Failed')
            else:
                raise ValidationError("Complete the Quality Test")
        res = super().button_validate()
        return res

    def action_view_quality_alerts(self):
        """Returning the Quality Test view for the button"""
        return {
            'name': 'Quality Alert',
            'type': 'ir.actions.act_window',
            'res_model': 'quality.alert',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.quality_alert_ids.ids)],
        }
