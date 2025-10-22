# -*- coding: utf-8 -*-

from odoo import api, models


class PropertyManagementWizard(models.AbstractModel):
    """Creating a Model for Report"""
    _name = "report.property_management.property_rent_lease_templates"

    @api.model
    def _get_report_values(self, docids, data=None):
        """Customized report creation for getting the view as such"""
        tenant_id = data.get('tenant_id')
        property_id = data.get('property_id')
        today_date = data.get('today_date')
        owner_id = data.get('owner_id')
        type = data.get('type')
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        state = data.get('state')
        filters = [
            {'label': 'Tenant', 'value': tenant_id},
            {'label': 'Property', 'value': property_id},
            {'label': 'Owner', 'value': owner_id},
            {'label': 'Type', 'value': type},
            {'label': 'From Date', 'value': from_date},
            {'label': 'To Date', 'value': to_date},
            {'label': 'State', 'value': state},
        ]
        non_empty = [values for values in filters if values['value']]
        non_empty.insert(
            2 if len(non_empty) >= 2 else len(non_empty),
            {'label': 'Report Date', 'value': today_date}
        )
        return {
            'docs': docids,
            'filters': non_empty,
        }
