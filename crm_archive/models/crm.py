#-*- coding:utf-8 -*-

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def _archive_inactive_records(self):
        """For archiving the inactive leads"""
        leads = self.env['crm.lead'].search([])
        threshold_minutes = int(self.env['ir.config_parameter'].sudo().get_param('crm_archive.chatter_threshold_minutes'))
        if leads and threshold_minutes > 0:
            for lead in leads:
                latest_message = self.env['mail.message'].search(
                    [('model', '=', 'crm.lead'), ('res_id', '=', lead.id)], order='date desc',limit=1 )
                if int((fields.Datetime.now() - latest_message.date).total_seconds() / 60) > threshold_minutes:
                    lead.action_archive()
