# -*- coding: utf-8 -*-

import io
import json
import xlsxwriter
import datetime
from xlsxwriter.utility import xl_col_to_name, xl_rowcol_to_cell

from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.tools import json_default


class MakePropertyRentLease(models.TransientModel):
    """Creating a Wizard Model for Report"""
    _name = "make.property.rent.lease"
    _description = "Property management wizard"

    property_id = fields.Many2one('property.properties', string="Property")
    from_date = fields.Date(string="From date")
    to_date = fields.Date(string='To date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approved'),
        ('confirm', 'Confirmed'),
        ('return', 'Return'),
        ('expired', 'Expired'),
        ('closed', 'Closed'),
        ('reject', 'Reject'),
    ], string='State')
    type = fields.Selection(selection=[('rent', 'Rent'), ('lease', 'Lease')], String="Type")
    owner_id = fields.Many2one('res.partner', string="Owner")
    tenant_id = fields.Many2one('res.partner', string="Tenant")
    today_date = fields.Date(default=datetime.date.today())

    def _get_values(self):
        """To create the data of the transient model"""
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError("To date should be Greater than From Date")
        param = []
        query = """
                SELECT 
                    pi.property_name as property_name,
                    ro.name as owner_name,
                    l.property_type,
                    rt.name as tenant_name,
                    l.start_date,
                    l.end_date,
                    pi.total_amount as in_total_amount,
                    l.name as id,
                    l.state,
                    rc.symbol as symbol
                    FROM property_rent_lease l
                    JOIN property_intermediate pi ON pi.intermediate_rent_id = l.id
                    JOIN res_partner ro ON ro.id = pi.owner_id
                    JOIN res_partner rt ON rt.id = l.tenant_id
                    JOIN res_company c ON c.id = l.company_id
                    JOIN res_currency rc ON rc.id = c.currency_id
                    """
        conditions = []
        if self.property_id:
            conditions.append("""pi.property_name = %s""")
            param.append(self.property_id.name)
        if self.from_date:
            conditions.append("""l.start_date >= %s""")
            param.append(self.from_date)
        if self.to_date:
            conditions.append("""l.end_date <= %s""")
            param.append(self.to_date)
        if self.state:
            conditions.append("""l.state = %s""")
            param.append(self.state)
        if self.tenant_id:
            conditions.append("""rt.name = %s""")
            param.append(self.tenant_id.name)
        if self.owner_id:
            conditions.append("""ro.name = %s""")
            param.append(self.owner_id.name)
        if self.type:
            conditions.append("""l.property_type = %s""")
            param.append(self.type)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        self.env.cr.execute(query, param)
        colnames = [desc[0] for desc in self.env.cr.description]
        rows = self.env.cr.fetchall()
        result = [dict(zip(colnames, row)) for row in rows]
        if not result:
            raise ValidationError("Given filter does not have any records. Please change the filters and try again")
        STATE_SELECTION = {
            'draft': 'Draft',
            'submit': 'Submit',
            'approve': 'Approved',
            'confirm': 'Confirmed',
            'return': 'Return',
            'expired': 'Expired',
            'closed': 'Closed',
            'reject': 'Reject',
        }
        TYPE_SELECTION = {
            'rent': 'Rent',
            'lease': 'Lease',
        }
        for record in result:
            record['state_display'] = STATE_SELECTION.get(record.get('state'))
            record['property_type_display'] = TYPE_SELECTION.get(record.get('property_type'))
        type_label = dict(self._fields['type'].selection).get(self.type)
        state_label = dict(self._fields['state'].selection).get(self.state)
        data = {
            'records': result,
            'property_id': self.property_id.name,
            'owner_id': self.owner_id.name,
            'tenant_id': self.tenant_id.name,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'type': type_label,
            'state': state_label,
            'today_date': self.today_date,
        }
        return data

    def action_create_pdf(self):
        """An Action button for printing the report"""
        data = self._get_values()
        return (self.env.ref('property_management.action_rent_lease_report_pdf').report_action
                (self, data=data))

    def action_create_xlsx(self):
        """Passes the data to the action manager"""
        datas = self._get_values()
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'make.property.rent.lease',
                     'options': json.dumps(datas, default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Property Rent Lease Report',
                     },
            'report_type': 'xlsx',
        }

    def merge_label(self, sheet, row, col, label, format, span=3):
        """For merging the columns of wizard fields"""
        start_cell = f"{xl_col_to_name(col)}{row + 1}"
        end_cell = f"{xl_col_to_name(col + span - 1)}{row + 1}"
        sheet.merge_range(f"{start_cell}:{end_cell}", label, format)

    def merge_labels(self, sheet, row, col, label, format):
        """For merging the columns of records"""
        start_cell = xl_rowcol_to_cell(row, col)
        end_cell = xl_rowcol_to_cell(row, col + 1)
        sheet.merge_range(f"{start_cell}:{end_cell}", label, format)

    def get_xlsx_report(self, data, response):
        """Creation of the Excel report"""
        records = data.get('records')
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        header_format = workbook.add_format(
            {'bold': True, 'border': 1, 'align': 'center'})
        table_format = workbook.add_format(
            {'font_size': '10px', 'border': 1, 'align': 'center'})
        cell_format = workbook.add_format(
            {'font_size': '10px', 'bold': True, 'align': 'center'})
        merge_format = workbook.add_format(
            {'font_size': '10px', 'align': 'left'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        currency_format = workbook.add_format(
            {'border': 1, 'font_size': '10px', 'align': 'right'})
        txt = workbook.add_format(
            {'font_size': '10px', 'align': 'center'})
        sheet.merge_range('R1:U3', ' ')
        sheet.insert_image('R1', '/home/cybrosys/odoo18/odoo/addons/base/static/img/res_company_logo.png',
                           {'x_scale': 0.5, 'y_scale': 0.5})
        company = self.env.user.company_id
        company_info = (f"{company.name or ''},\n"
                        f"{company.street or ''},\n"
                        f"{company.city or ''},\n"
                        f"{company.zip or ''}")
        sheet.merge_range('R4:U6', company_info, merge_format)
        sheet.merge_range('B11:U13', 'PROPERTY RENT/LEASE REPORT', head)
        col_val = 1
        row_val = 15
        field = 0
        if data.get('tenant_id'):
            self.merge_label(sheet, row_val, col_val, 'Tenant:', cell_format)
            col_val += 3
            self.merge_label(sheet, row_val, col_val, data['tenant_id'], txt)
            col_val += 4
            field += 1
        if data.get('property_id'):
            self.merge_label(sheet, row_val, col_val, 'Property:', cell_format)
            col_val += 3
            self.merge_label(sheet, row_val, col_val, data['property_id'], txt)
            col_val += 4
            field += 1
        if data.get('owner_id'):
            if row_val == 15 and col_val >= 9:
                row_val += 2
                col_val = 1
            self.merge_label(sheet, row_val, col_val, 'Owner:', cell_format)
            col_val += 3
            self.merge_label(sheet, row_val, col_val, data['owner_id'], txt)
            col_val += 4
            field += 1
        if data.get('from_date'):
            if row_val == 15 and col_val >= 9:
                row_val += 2
                col_val = 1
            self.merge_label(sheet, row_val, col_val, 'From Date:', cell_format)
            col_val += 3
            self.merge_label(sheet, row_val, col_val, data['from_date'], txt)
            col_val += 4
            field += 1
        if data.get('to_date'):
            if row_val == 15 and col_val >= 9:
                row_val += 2
                col_val = 1
            self.merge_label(sheet, row_val, col_val, 'To Date:', cell_format)
            col_val += 3
            self.merge_label(sheet, row_val, col_val, data['to_date'], txt)
            col_val += 4
            field += 1
        if data.get('type'):
            if (row_val == 15 and col_val >= 9) or (row_val == 17 and col_val >= 14):
                row_val += 2
                col_val = 1
            self.merge_label(sheet, row_val, col_val, 'Type:', cell_format)
            col_val += 3
            self.merge_label(sheet, row_val, col_val, data['type'], txt)
            col_val += 4
            field += 1
        if data.get('state'):
            if (row_val == 15 and col_val >= 9) or (row_val == 17 and col_val >= 15):
                row_val += 2
                col_val = 1
            self.merge_label(sheet, row_val, col_val, 'State:', cell_format)
            col_val += 3
            self.merge_label(sheet, row_val, col_val, data['state'], txt)
            col_val += 4
            field += 1
        if field > 2:
            self.merge_label(sheet, 15, 15, 'Report Date:', cell_format)
            self.merge_label(sheet, 15, 18, data['today_date'], txt)
        else:
            self.merge_label(sheet, row_val, col_val, 'Report Date:', cell_format)
            col_val += 3
            self.merge_label(sheet, row_val, col_val, data['today_date'], txt)
            col_val += 4
        columns = [('ID', 'id')]
        if not data.get('tenant_id'):
            columns.append(('Tenant', 'tenant_name'))
        if not data.get('property_id'):
            columns.append(('Property', 'property_name'))
        if not data.get('type'):
            columns.append(('Type', 'property_type_display'))
        if not data.get('owner_id'):
            columns.append(('Owner', 'owner_name'))
        if not data.get('start_date'):
            columns.append(('Start Date', 'start_date'))
        if not data.get('to_date'):
            columns.append(('End Date', 'end_date'))
        columns.append(('Total Amount', 'in_total_amount'))
        if not data.get('state'):
            columns.append(('State', 'state_display'))
        for col_index, (label, _) in enumerate(columns):
            col = 2 + col_index * 2
            self.merge_labels(sheet, 23, col, label, header_format)
        for row_index, rec in enumerate(records):
            row = 24 + row_index
            for col_index, (_, field) in enumerate(columns):
                col = 2 + col_index * 2
                values = rec.get(field)
                if field == 'in_total_amount':
                    amount = rec.get('in_total_amount') or 0.0
                    symbol = rec.get('symbol') or ''
                    values = f"{symbol} {amount:,.2f}"
                    format_type = currency_format
                else:
                    format_type = currency_format if 'date' in field else table_format
                self.merge_labels(sheet, row, col, values, format_type)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
