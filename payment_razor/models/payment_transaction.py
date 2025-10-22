#-*- coding: utf-8 -*-

from odoo import _, models
from odoo.exceptions import ValidationError

from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment_razor import const


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_processing_values(self, processing_values):
        """ Override of `payment` to return razorpay-specific processing values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic and specific processing values of the
                                       transaction.
        :return: The provider-specific processing values.
        :rtype: dict
        """
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != 'draco':
            return res
        customer_id = self._razor_create_customer()['id']
        order_id = self._razor_create_order(customer_id)['id']
        return {
            'razor_key_id': self.provider_id.razor_key_id,
            'razor_customer_id': customer_id,
            'razor_order_id': order_id,
        }

    def _razor_create_customer(self):
        """ Create and return a Customer object.

        :return: The created Customer.
        :rtype: dict
        """
        payload = {
            'name': self.partner_name,
            'email': self.partner_email or '',
            'contact': self.partner_phone or '',
            'fail_existing': '0',  # Don't throw an error if the customer already exists.
        }
        customer_data = self.provider_id._razor_make_request('customers', payload=payload)
        return customer_data

    def _razor_create_order(self, customer_id=None):
        """ Create and return an Order object to initiate the payment.

        :param str customer_id: The ID of the Customer object to assign to the Order for
                                non-subsequent payments.
        :return: The created Order.
        :rtype: dict
        """
        payload = self._razor_prepare_order_payload(customer_id=customer_id)
        order_data = self.provider_id._razor_make_request('orders', payload=payload)
        return order_data

    def _razor_prepare_order_payload(self, customer_id=None):
        """ Prepare the payload for the order request based on the transaction values.

        :param str customer_id: The ID of the Customer object to assign to the Order for
                                non-subsequent payments.
        :return: The request payload.
        :rtype: dict
        """
        converted_amount = payment_utils.to_minor_currency_units(self.amount, self.currency_id)
        pm_code = (self.payment_method_id.primary_payment_method_id or self.payment_method_id).code
        payload = {
            'amount': converted_amount,
            'currency': self.currency_id.name,
            **({'method': pm_code} if pm_code not in const.FALLBACK_PAYMENT_METHOD_CODES else {}),
        }
        if self.operation in ['online_direct', 'validation']:
            payload['customer_id'] = customer_id  # Required for only non-subsequent payments.
        else:
            payload['payment_capture'] = not self.provider_id.capture_manually
        if self.provider_id.capture_manually:  # The related payment must be only authorized.
            payload.update({
                'payment': {
                    'capture': 'manual',
                    'capture_options': {
                        'manual_expiry_period': 7200,  # The default value for this required option.
                        'refund_speed': 'normal',  # The default value for this required option.
                    }
                },
            })
        return payload

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of `payment` to find the transaction based on razorpay data.

        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The normalized notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'draco':
            return tx
        entity_type = notification_data.get('entity_type', 'payment')
        if entity_type == 'payment':
            reference = notification_data.get('description')
            if not reference:
                raise ValidationError("Razorpay: " + _("Received data with missing reference."))
            tx = self.search([('reference', '=', reference), ('provider_code', '=', 'draco')])
        if not tx:
            raise ValidationError(
                "Razorpay: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_notification_data(self, notification_data):
        """ Override of `payment` to process the transaction based on Razorpay data.

        Note: self.ensure_one()

        :param dict notification_data: The notification data sent by the provider
        :return: None
        """
        super()._process_notification_data(notification_data)
        if self.provider_code != 'draco':
            return
        if not notification_data:
            self._set_canceled(state_message=_("The customer left the payment page."))
            return
        payment_status = notification_data.get('status')
        if payment_status in const.PAYMENT_STATUS_MAPPING['pending']:
            self._set_pending(state_message=notification_data.get('pending_reason'))
        elif payment_status in const.PAYMENT_STATUS_MAPPING['done']:
            self._set_done()
        elif payment_status in const.PAYMENT_STATUS_MAPPING['cancel']:
            self._set_canceled()
        else:
            self._set_error(
                "Razor: " + _("Received data with invalid payment status: %s", payment_status)
            )
