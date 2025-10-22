# -*- coding: utf-8 -*-
import json
import traceback

from odoo import http
from odoo.http import content_disposition, request


class XLSXReportController(http.Controller):
    """To specify the functions and its workings in this particular class"""

    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'], csrf=False)
    def get_report_xlsx(self, model, options, output_format, report_name, token=None, **kwargs):
        """To get the values of our xlsx report"""
        try:
            session_uid = request.session.uid
            report_obj = request.env[model].with_user(session_uid)
            options = json.loads(options)
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition', content_disposition(f"{report_name}.xlsx"))
                    ]
                )
                report_obj.get_xlsx_report(options, response)
                response.set_cookie('fileToken', token or '')
                return response
        except Exception as e:
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': {
                    'name': type(e).__name__,
                    'debug': traceback.format_exc(),
                    'message': str(e),
                }
            }
            return request.make_response(
                json.dumps(error),
                headers={'Content-Type': 'application/json'},
                status=500
            )
