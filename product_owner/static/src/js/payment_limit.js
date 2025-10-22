/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { patch } from '@web/core/utils/patch';
import { PosOrderline } from '@point_of_sale/app/models/pos_order_line';
import { PaymentScreen } from '@point_of_sale/app/screens/payment_screen/payment_screen';
import { AlertDialog } from '@web/core/confirmation_dialog/confirmation_dialog';

patch(PaymentScreen.prototype,{
    async _finalizeValidation(){
        if(this.currentOrder?.partner_id?.name == undefined)
        {
            this.dialog.add(AlertDialog, {
            title: _t("Validation Error"),
            body: _t(
                "Please select a customer before Validating"
            ),
        });
        }
        else
        {
            const amount_total = this.currentOrder.getTotalDue()
            const max_limit = this.currentOrder.get_partner().max_limit
            const payment_limit = this.currentOrder.get_partner().payment_limit
            if (max_limit == true && amount_total > payment_limit)
            {
                this.dialog.add(AlertDialog, {
                    title: _t("Limit exceeded"),
                    body: _t(
                        "You have exceeded the limit of "+ payment_limit
                    ),
                });
            }
            else
            {
                return{
                ...(super._finalizeValidation())
                }
            }
        }
    }
});