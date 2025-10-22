# -*- coding: utf-8 -*-

import datetime
from markupsafe import Markup

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.fields import Command


class RentLease(models.Model):
    """Creating a model and its fields"""
    _name = "property.rent.lease"
    _description = "Displays the rental and lease properties"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(readonly=True, default='New', copy=False)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    due_date = fields.Date(string="Due Date")
    invoice_count = fields.Integer(compute="_compute_invoice_count")
    total_days = fields.Integer(string="Total Days", compute="_compute_total_days")
    property_line_ids = fields.One2many('property.intermediate', 'intermediate_rent_id',
                                        required=True, ondelete="cascade")
    invoice_ids = fields.One2many('account.move', 'property_rental_id')
    tenant_id = fields.Many2one('res.partner', string="Partner", required=True, store=True)
    owner_id = fields.Many2one(related='property_line_ids.owner_id', string="Owner Name", store=True)
    company_id = fields.Many2one('res.company',
                                 string='Company name',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', string="Currency")
    user_id = fields.Many2one('res.users', string='Responsible User', default=lambda self: self.env.user)
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('submit', 'Submit'),
                                        ('approve', 'Approved'),
                                        ('confirm', 'Confirmed'),
                                        ('return', 'Return'),
                                        ('expired', 'Expired'),
                                        ('closed', 'Closed'),
                                        ('reject', 'Reject'),
                                        ], default='draft', tracking=True)
    property_type = fields.Selection(string="Type", selection=[('rent', 'Rent'), ('lease', 'Lease')],
                                     default='rent')
    total_amount = fields.Monetary(string="Total Amount", compute="_compute_legal_amount", readonly=True, store=True)
    rent_id = fields.Monetary(related='property_line_ids.amount')
    property_name = fields.Char(related='property_line_ids.property_name', string="Property Name")
    vanish_inv = fields.Boolean(compute="_compute_vanish_inv")

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        """To calculate the number of invoices present"""
        for record in self:
            record.invoice_count = len(record.invoice_ids.filtered(lambda inv: inv.state in ['draft', 'posted']))

    @api.depends('start_date', 'end_date')
    def _compute_total_days(self):
        """to calculate the number of days between start and end"""
        for record in self:
            if not record.start_date or not record.end_date:
                record.total_days = 0
            elif record.start_date > record.end_date:
                raise ValidationError("Ending date must be greater than starting date")
            elif record.start_date and record.end_date and record.end_date > record.start_date:
                record.total_days = (record.end_date - record.start_date).days
            else:
                record.total_days = 0

    @api.depends('property_line_ids.quantity', 'property_line_ids.invoiced_qty')
    def _compute_vanish_inv(self):
        """To make the invoice button invisible"""
        for record in self:
            remaining_qty = any(
                line.invoiced_qty < line.quantity
                for line in record.property_line_ids
            )
            record.vanish_inv = not remaining_qty

    @api.depends('property_line_ids')
    def _compute_legal_amount(self):
        """To calculate the total amount"""
        for record in self:
            record.total_amount = sum(prop.total_amount for prop in record.property_line_ids)

    @api.model
    def expire_due_date(self):
        """To change the state based on due date"""
        date = datetime.date.today()
        due = self.env['property.rent.lease'].search([('due_date', '<', date)])
        if due:
            due.write({'state': 'expired'})

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the model """
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('property.rent.lease')
        return super().create(vals_list)

    @api.onchange('end_date')
    def _onchange_end_date(self):
        """To assign the due date value as end date"""
        self.due_date = self.end_date

    def check_attachments(self):
        """To check for attachments"""
        attachments = self.env['ir.attachment'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id)
        ])
        if not attachments:
            raise ValidationError("Please attach files")

    def action_submit(self):
        """To change the state to submit"""
        self.write({'state': 'submit'})

    def action_approve(self):
        """To change the state to approve"""
        self.write({'state': 'approve'})

    def action_reject(self):
        """To change the state to reject"""
        self.write({'state': 'reject'})

    def action_confirm(self):
        """To change the state to confirm"""
        self.check_attachments()
        template = self.env.ref('property_management.confirm_template')
        template.send_mail(self.id, force_send=True)
        rendered_body = template._render_field('body_html', [self.id])
        rendered_html_string = rendered_body.get(self.id)
        if rendered_html_string:
            self.message_post(
                body=Markup(rendered_html_string),
                message_type='comment',
                subtype_xmlid="mail.mt_comment",
            )
        self.write({'state': 'confirm'})

    def action_closed(self):
        """To change the state to closed"""
        template = self.env.ref('property_management.close_email_template')
        template.send_mail(self.id, force_send=True)
        rendered_body = template._render_field('body_html', [self.id])
        rendered_html_string = rendered_body.get(self.id)
        if rendered_html_string:
            self.message_post(
                body=Markup(rendered_html_string),
                message_type='comment',
                subtype_xmlid="mail.mt_comment",
            )
        self.write({'state': 'closed'})

    def action_returns(self):
        """To change the state to return"""
        self.write({'state': 'return'})

    def action_expired(self):
        """To change the state to expire"""
        template = self.env.ref('property_management.expire_email_template')
        template.send_mail(self.id, force_send=True)
        rendered_body = template._render_field('body_html', [self.id])
        rendered_html_string = rendered_body.get(self.id)
        if rendered_html_string:
            self.message_post(
                body=Markup(rendered_html_string),
                message_type='comment',
                subtype_xmlid="mail.mt_comment",
            )
        self.write({'state': 'expired'})

    def action_reset(self):
        """To change the state back to draft"""
        self.write({'state': 'draft'})

    def action_invoice_form(self):
        """To create the invoice for the rent/lease"""
        self.ensure_one()
        draft_invoice = self.invoice_ids.filtered(lambda inv: inv.state == 'draft')
        invoice = draft_invoice if draft_invoice else None
        for prop in self.property_line_ids:
            rem_qty = prop.quantity - prop.invoiced_qty
            if rem_qty <= 0:
                continue
            existing_invoice_line = self.invoice_ids.invoice_line_ids.filtered(
                lambda line: line.property_line_id.id == prop.id
            )
            if existing_invoice_line and any(move.state == 'draft' for move in existing_invoice_line.move_id):
                existing_invoice_line.write({
                    'quantity': rem_qty,
                    'price_unit': prop.amount,
                    'name': prop.property_name,
                })
            else:
                if not invoice:
                    invoice = self.env['account.move'].create({
                        'move_type': 'out_invoice',
                        'partner_id': self.tenant_id.id,
                        'invoice_date': fields.Date.context_today(self),
                        'invoice_date_due': self.due_date,
                        'state': 'draft',
                        'property_rental_id': self.id,
                    })
                    self.invoice_ids = [Command.link(invoice.id)]
                invoice.write({
                    'invoice_line_ids': [Command.create({
                        'name': prop.property_name,
                        'quantity': rem_qty,
                        'price_unit': prop.amount,
                        'property_line_id': prop.id,
                    })]
                })
        return {
            'name': "Customer Invoice",
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

    def action_get_invoice(self):
        """To show the invoices created in the smart button"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.invoice_ids.ids)],
            'context': {'create': False},
            'target': 'current',
        }
