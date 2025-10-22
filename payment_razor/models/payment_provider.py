# -*- coding: utf-8 -*-

import requests

from odoo import _, fields, models
from odoo.exceptions import ValidationError
from odoo.addons.payment_razor import const


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('draco', "draco")], ondelete={'draco': 'set default'})
    razor_key_id = fields.Char(
        string="Razor Key Id",
        help="The key solely used to identify the account with Razorpay.",
        required_if_provider='draco',
    )
    razor_key_secret = fields.Char(
        string="Razor Key Secret",
        required_if_provider='draco',
        groups='base.group_system',
    )

    def _razor_make_request(self, endpoint, payload=None, method='POST'):
        """ Make a request to Razorpay API at the specified endpoint.

        Note: self.ensure_one()

        :param str endpoint: The endpoint to be reached by the request.
        :param dict payload: The payload of the request.
        :param str method: The HTTP method of the request.
        :return The JSON-formatted content of the response.
        :rtype: dict
        :raise ValidationError: If an HTTP error occurs.
        """
        self.ensure_one()
        # TODO: Make api_version a kwarg in master.
        api_version = self.env.context.get('razorpay_api_version', 'v1')
        url = f'https://api.razorpay.com/{api_version}/{endpoint}'
        headers = None
        auth = (self.razor_key_id, self.razor_key_secret) if self.razor_key_id else None
        inr_amount = payload.get('amount')
        other_currency = payload.get('currency')
        try:
            if method == 'GET':
                response = requests.get(
                    url,
                    params=payload,
                    headers=headers,
                    auth=auth,
                    timeout=10,
                )
            else:
                if other_currency != 'INR' and inr_amount:
                    inr_conv_amount = int(self.convert_currency(inr_amount, other_currency))
                    payload.update({'currency': 'INR',
                                    'amount': inr_conv_amount})
                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    auth=auth,
                    timeout=10,
                )
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                raise ValidationError("Razorpay: " + _(
                    "Razorpay gave us the following information: '%s'",
                    response.json().get('error', {}).get('description')
                ))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            raise ValidationError(
                "Razorpay: " + _("Could not establish the connection to the API.")
            )
        return response.json()

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code == 'draco':
            return const.DEFAULT_PAYMENT_METHOD_CODES
        return default_codes

    def _get_validation_amount(self):
        """ Override of `payment` to return the amount for Razorpay validation operations.

        :return: The validation amount.
        :rtype: float
        """
        res = super()._get_validation_amount()
        if self.code != 'draco':
            return res
        return 1.0

    def convert_currency(self, inr_amount, from_currency, to_currency='INR'):
        """Used for converting the amount to INR"""
        access_key = '292750c8dc30e06c9e5147e240c8eed4'
        url = f"http://data.fixer.io/api/latest?access_key={access_key}"
        response = requests.get(url)
        data = response.json()
        to_currency_val = data.get('rates').get(to_currency)
        from_currency_val = data.get('rates').get(from_currency)
        diff = to_currency_val / from_currency_val
        value = round((inr_amount * diff), 2)
        return value
