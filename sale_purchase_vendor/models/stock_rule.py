# -*- coding: utf-8 -*-

from odoo import api, models


class StockRule(models.Model):
    _inherit = "stock.rule"

    @api.model
    def _run_buy(self, procurements):
        """Automatically choose best vendor when stock is empty."""
        for procurement, rule in procurements:
            product = procurement.product_id
            location = procurement.location_id
            stock_available = product.with_context(location=location.id).qty_available
            lower_names = [r.lower() for r in product.route_ids.mapped('name')]
            best_vendor = None
            if (stock_available <= 0.0 and 'buy' in lower_names and 'replenish on order (mto)' in lower_names):
                if product.seller_ids:
                    sorted_vendors = sorted(product.seller_ids, key=lambda v: ((v.price / v.min_qty), v.delay))
                    best_vendor = sorted_vendors[0]
            if best_vendor:
                procurement.values['supplierinfo_id'] = best_vendor
            return super()._run_buy(procurements)
