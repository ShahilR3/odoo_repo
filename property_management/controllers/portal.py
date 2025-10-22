# -*- coding: utf-8 -*-

from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class RentLeasePortal(CustomerPortal):
    """To mention the functions and its performance under this class"""

    def _prepare_home_portal_values(self, counters):
        """To find the count of rent/lease the customer has"""
        values = super()._prepare_home_portal_values(counters)
        if 'rent_lease_count' in counters:
            partner = request.env.user.partner_id
            domain = [('tenant_id', '=', partner.id)]
            count = request.env['property.rent.lease'].sudo().search_count(domain)
            values['rent_lease_count'] = count
        return values

    @route(['/my/rentlease'], type='http', auth="user", website=True)
    def portal_my_rent_lease(self, **kw):
        """to get the details of the rent lease that the particular customer has"""
        partner = request.env.user.partner_id
        orders = request.env['property.rent.lease'].sudo().search([
            ('tenant_id', '=', partner.id)
        ])
        return request.render("property_management.portal_my_rent_lease", {
            'orders': orders,
            'page_name': 'rent_lease',
        })

    @route(['/my/rentlease/<int:order_id>'], type='http', auth='user', website=True)
    def portal_rent_lease_order_page(self, order_id, access_token=None, message=False, **kw):
        """To fetch the details to be viewed in this particular page"""
        rent_lease_order = request.env['property.rent.lease'].sudo().browse(order_id)
        values = {
            'object': rent_lease_order,
            'rent_lease_order': rent_lease_order,
            'message': message,
            'res_model': 'property.rent.lease',
            'res_id': rent_lease_order.id,
            'token': access_token,
            'page_name': 'rentlease_val',
            'partner_id': request.env.user.partner_id.id,
        }
        values = self._get_page_view_values(
            rent_lease_order, access_token=access_token,
            session_history='my_rent_history',
            values=values,
            no_breadcrumbs=False
        )
        return request.render('property_management.rent_lease_order_portal_template', values)
