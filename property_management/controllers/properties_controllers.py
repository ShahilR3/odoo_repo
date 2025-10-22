# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request, route
from odoo.addons.web.controllers.binary import Binary

class PublicImageController(Binary):
    """Fixing the image routes"""

    @route(['/property/image/<int:id>'], type='http', auth="public", website=True)
    def property_image(self, id, **kwargs):
        """Making the image accessible to every users"""
        record = request.env['property.properties'].sudo().browse(id)
        if not record.exists():
            return request.not_found()
        image_data = record.image_property
        return request.make_response(
            image_data.decode('base64'),
            headers=[('Content-Type', 'image/jpg')]
        )


class PropertyController(http.Controller):
    """To mention the routes and this workings"""

    @route(['/property/details/<int:order_id>'], type='http', auth="user", website=True)
    def order_detail(self, order_id, **kwargs):
        """Fetches the values that is to be displayed in this page"""
        order = request.env['property.properties'].sudo().browse(order_id)
        if not order.exists():
            return request.not_found()
        return request.render('property_management.template_property_detail', {
            'order': order,
        })

    @route('/property/list/json', type='json', auth='none', website=True)
    def property_list_json(self):
        """passes the values of the property"""
        properties = request.env['property.properties'].sudo().search([], limit=20)
        return [{
            'id': p.id,
            'name': p.name,
            'legal_amount': p.legal_amount,
            'currency': p.currency_id.symbol if p.currency_id else '',
            'image': f"data:image/jpg;base64,{p.image_property.decode()}" if p.image_property else ''
        } for p in properties]
