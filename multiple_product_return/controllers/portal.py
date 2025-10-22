# -*- coding: utf-8 -*-

from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class ReturnOrderPortal(CustomerPortal):
    """To mention the functions and its performance under this class"""

    def _prepare_home_portal_values(self, counters):
        """To find the count of return order the customer has"""
        values = super()._prepare_home_portal_values(counters)
        if 'return_order_count' in counters:
            partner = request.env.user.partner_id
            domain = [('partner_id', '=', partner.id)]
            count = request.env['website.return'].sudo().search_count(domain)
            values['return_order_count'] = count
        return values

    @route(['/my/returnorder'], type='http', auth="user", website=True)
    def portal_return_order(self, **kw):
        """to get the details of the return order that the particular customer has"""
        partner = request.env.user.partner_id
        orders = request.env['website.return'].sudo().search([
            ('partner_id', '=', partner.id)
        ])
        return request.render("multiple_product_return.portal_my_return_order", {
            'orders': orders,
            'page_name': 'return_order',
        })

    @route(['/my/returnorder/<int:order_id>'], type='http', auth='user', website=True)
    def portal_return_order_page(self, order_id, access_token=None, message=False, **kw):
        """To fetch the details to be viewed in this particular page"""
        return_order = request.env['website.return'].sudo().browse(order_id)
        values = {
            'object': return_order,
            'return_order': return_order,
            'message': message,
            'res_model': 'website.return',
            'res_id': return_order.id,
            'token': access_token,
            'page_name': 'returnorder_val',
            'partner_id': request.env.user.partner_id.id,
        }
        values = self._get_page_view_values(
            return_order, access_token=access_token,
            session_history='my_return_history',
            values=values,
            no_breadcrumbs=False
        )
        return request.render('multiple_product_return.return_order_portal_template', values)
