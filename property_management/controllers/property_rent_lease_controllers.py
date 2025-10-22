# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request, route


class WebFormController(http.Controller):
    """To mention the routes and its contents"""

    @route('/webform', auth='user', website=True)
    def web_form(self, **kwargs):
        """The contents to be displayed in this url"""
        property_id = request.env['property.properties'].sudo().search([])
        rent_lease_id = request.env['property.rent.lease'].sudo().search([])
        currency_id = rent_lease_id.currency_id
        partners = request.env['res.partner'].sudo().search([])
        print(partners)
        datas = {
            'partners': partners,
            'lease': None,
            'property_id': property_id,
            'currency_id': currency_id,
        }
        return request.render('property_management.rent_lease_template', datas)

    @route('/webform/submit', type='json', auth='user', website=True, methods=['POST'])
    def web_form_submit(self, **post):
        """The function for passing the values from website to the application"""
        model_name = 'property.rent.lease'
        model_fields = request.env['ir.model.fields'].sudo().search([('model', '=', model_name)])
        values = {}
        for key, val in post.items():
            field = model_fields.filtered(lambda f: f.name == key)
            if not field:
                continue
            if field.ttype == 'many2one':
                try:
                    val = int(val) if val else False
                except (ValueError, TypeError):
                    related_model = request.env[field.relation].sudo()
                    related_record = related_model.search([('name', '=', val)], limit=1)
                    val = related_record.id if related_record else False
            elif field.ttype == 'one2many':
                relation_fields = request.env['ir.model.fields'].sudo().search([
                    ('model', '=', field.relation)
                ])
                one2many_lines = []
                for line in val:
                    line_data = {}
                    for sub_key, sub_val in line.items():
                        sub_field = relation_fields.filtered(lambda f: f.name == sub_key)
                        if sub_field:
                            if sub_field.ttype == 'many2one':
                                related_model = request.env[sub_field.relation].sudo()
                                related_record = related_model.search([('name', '=', sub_val)], limit=1)
                                sub_val = related_record.id if related_record else False
                            elif sub_field.ttype in ['integer', 'float']:
                                sub_val = float(sub_val) if sub_val else 0
                            elif sub_field.ttype == 'boolean':
                                sub_val = str(sub_val).lower() in ['true', '1', 'yes']
                        line_data[sub_key] = sub_val
                    one2many_lines.append((0, 0, line_data))
                val = one2many_lines
            elif field.ttype in ['integer', 'float']:
                val = float(val) if val else 0
            elif field.ttype == 'boolean':
                val = str(val).lower() in ['true', '1', 'yes']
            values[key] = val
        record = request.env[model_name].sudo().create(values)
        return {'success': True, 'record_id': record.id}

    @route('/property/details/fetch', type='json', auth='public')
    def fetch_property_lines(self, property_id):
        """To fetch the details of the One 2 many field"""
        if not property_id:
            return ""
        property_record = request.env['property.properties'].sudo().browse(int(property_id))
        lines = property_record.property_inter_ids[:1]
        return request.env['ir.ui.view']._render_template(
            'property_management.property_line_template',
            {'lines': lines}
        )
