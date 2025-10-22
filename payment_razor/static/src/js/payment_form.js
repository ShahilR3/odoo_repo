/** @odoo-module **/
/* global Razorpay */

import { _t } from '@web/core/l10n/translation';
import { loadJS } from '@web/core/assets';
import paymentForm from '@payment/js/payment_form';

paymentForm.include({

    // #=== DOM MANIPULATION ===#

    /**
     * Update the payment context to set the flow to 'direct'.
     *
     * @override method from @payment/js/payment_form
     * @private
     * @param {number} providerId - The id of the selected payment option's provider.
     * @param {string} providerCode - The code of the selected payment option's provider.
     * @param {number} paymentOptionId - The id of the selected payment option
     * @param {string} paymentMethodCode - The code of the selected payment method, if any.
     * @param {string} flow - The online payment flow of the selected payment option.
     * @return {void}
     */
    async _prepareInlineForm(providerId, providerCode, paymentOptionId, paymentMethodCode, flow) {
        if (providerCode !== 'draco') {
            this._super(...arguments);
            return;
        }
        // Overwrite the flow of the select payment method.
        this._setPaymentFlow('direct');
    },

    // #=== PAYMENT FLOW ===#

    async _processDirectFlow(providerCode, paymentOptionId, paymentMethodCode, processingValues) {
        if (providerCode !== 'draco') {
            this._super(...arguments);
            return;
        }
        const razorpayOptions = this._prepareRazorpayOptions(processingValues);
        await loadJS('https://checkout.razorpay.com/v1/checkout.js');
        const RazorpayJS = Razorpay(razorpayOptions);
        RazorpayJS.open();
    },
    /**
     * Prepare the options to init the RazorPay SDK Object.
     *
     * @param {object} processingValues - The processing values.
     * @return {object}
     */
    _prepareRazorpayOptions(processingValues) {
        return Object.assign({}, processingValues, {
            'key': processingValues['razor_key_id'],
            'customer_id': processingValues['razor_customer_id'],
            'order_id': processingValues['razor_order_id'],
            'description': processingValues['reference'],
            'handler': response => {
                if (
                    response['razorpay_payment_id']
                    && response['razorpay_order_id']
                ) { // The payment reached a final state; redirect to the status page.
                    window.location = '/payment/status';
                }
            },
            'modal': {
                'ondismiss': () => {
                    window.location.reload();
                }
            },
        });
    },
});
