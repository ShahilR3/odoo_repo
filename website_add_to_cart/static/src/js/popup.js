/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { renderToElement } from "@web/core/utils/render";

publicWidget.registry.PopUp = publicWidget.Widget.extend({
    selector: '.container',
    events: {
        'click #add_cart': '_onClickAdd',
    },
    async _onClickAdd(ev) {
        console.log("ABCCC")
        ev.preventDefault();
        console.log(this)
        const productId = this.$el.find("#product_id").val()
        const qty = this.$el.find("#add_qty").val()
        const suggested = []
         const ctx = {
            added_product: { id: productId || 0 },
            added_quantity: qty || 1,
            suggested_products: Array.isArray(suggested) ? suggested : [],
        };

        console.log("Add to Cart context:", ctx);

        const $modal = await renderToElement('website_sale.addToCartNotification', ctx);
        console.log($modal)

    },
});