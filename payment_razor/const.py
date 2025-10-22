# -*- coding: utf-8 -*-

# The codes of the payment methods to activate when Razorpay is activated.
DEFAULT_PAYMENT_METHOD_CODES = {
    # Primary payment methods.
    'card',
    'netbanking',
    'upi',
    # Brand payment methods.
    'visa',
    'mastercard',
    'amex',
    'discover',
}

# The codes of payment methods that are not recognized by the orders API.
FALLBACK_PAYMENT_METHOD_CODES = {
    'wallets_india',
    'paylater_india',
    'emi_india',
}

# Mapping of payment method codes to Razorpay codes.
PAYMENT_METHODS_MAPPING = {
    'wallets_india': 'wallet',
    'paylater_india': 'paylater',
    'emi_india': 'emi',
}
# Mapping of transaction states to Razorpay's payment statuses.
# See https://razorpay.com/docs/payments/payments#payment-life-cycle.
PAYMENT_STATUS_MAPPING = {
    'pending': ('created', 'pending'),
    'authorized': ('authorized',),
    'done': ('captured', 'refunded', 'processed'),  # refunded is included to discard refunded txs.
    'error': ('failed',),
}
# Events that are handled by the webhook.
HANDLED_WEBHOOK_EVENTS = [
    'payment.authorized',
    'payment.captured',
    'payment.failed',
    'refund.failed',
    'refund.processed',
]
