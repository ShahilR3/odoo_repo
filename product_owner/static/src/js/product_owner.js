/** @odoo-module **/

import { patch } from '@web/core/utils/patch';
import { PosOrderline } from '@point_of_sale/app/models/pos_order_line';
import { Orderline } from '@point_of_sale/app/generic_components/orderline/orderline';

patch(PosOrderline.prototype, {
    getDisplayData() {
        return {
            ...(super.getDisplayData?.() || {}),
            productOwnerName: (this.product_id?.product_owner_id?.name || ' '),
        };
    },
});

patch(Orderline, {
    props: {
        ...Orderline.props,
        line: {
            ...Orderline.props.line,
            shape: {
                ...Orderline.props.line.shape,
                productOwnerName: { type: String, optional: true },
            },
        },
    },
});
