# -*- coding: utf-8 -*-

from odoo import api, models


class StockRule(models.Model):
    _inherit="stock.rule"

    @api.model
    def _run_pull(self, procurements):
        """Creating Auto Manufacture"""
        for procurement, rule in procurements:
            product = procurement.product_id
            location = procurement.location_id
            stock_available = product.with_context(location=location.id).qty_available
            lower_name = [r.lower() for r in product.route_ids.mapped('name')]
            vendor_delays = min(product.seller_ids.mapped('delay')) if product.seller_ids else 0
            if stock_available < product.reordering_min_qty and 'buy' in lower_name and 'manufacture' in lower_name:
                if vendor_delays > product.bom_ids.produce_delay:
                    manufacture_rule = self.env['stock.rule'].search([
                        ('action', '=', 'manufacture'),
                        ('route_id', 'in', product.route_ids.ids)
                    ], limit=1)
                    if manufacture_rule:
                        return manufacture_rule._run_manufacture([(procurement, manufacture_rule)])

        return super()._run_pull(procurements)