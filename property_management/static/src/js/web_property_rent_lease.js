/** @odoo-module **/

import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";


publicWidget.registry.PropertyRentLease = publicWidget.Widget.extend({
    selector: '.rent_lease_container, #property_line_template',
    events: {
        'change select[name="property"]': '_onPropertyChange',
        'change input.quantity_input': '_onFieldChange',
        'change #start_date': '_onDateChange',
        'change #end_date': '_onDateChange',
        'click .remove_line': '_onClickRemoveLine',
        'click .add_property': '_onClickAddProperty',
        'click .custom_create': '_onClickSubmit',
    },

     _onClickAddProperty: function (ev) {
        const startDateStr = this.$el.find('#start_date').val();
        const endDateStr = this.$el.find('#end_date').val();
        var c=0;
        if ((startDateStr == '') || (endDateStr==''))
        {
            c=1;
            this.$el.find(".value").text("Please Enter proper dates");
            this.$el.find("#customDialog").modal('show');
        }
        if ((endDateStr <= startDateStr)&&(c==0))
        {
            c=1;
            this.$el.find(".value").text("End date must be greater");
            this.$el.find("#customDialog").modal('show');
        }
        if (c==0)
        {
            this.$el.find("#customDialog").modal('hide');
            const $templateRow = this.$el.find('.property_new_lines').first();
            const $newRow = $templateRow.clone();
            $newRow.removeClass('property_new_lines').show();
            this.$el.find('#property_table tbody').append($newRow);
        }
    },

   _onClickRemoveLine: function (ev) {
       if (this.$el.find('#property_table tbody tr').length > 1) {
           $(ev.target).closest('tr').remove();
       } else {
            this.$el.find(".value").text("At least one property must be selected");
            this.$el.find("#customDialog").modal('show');
       }
   },

    _onPropertyChange: async function (ev) {
    const $row = $(ev.currentTarget).closest('tr');
    const propertyId = ev.target.value;
    try {
            const html = await rpc('/property/details/fetch', {
                property_id: parseInt(propertyId),
            });
            this.$el.find('#property_table tbody').append(html);
            $row.remove();
        } catch (error) {
            console.error('RPC error:', error);
        }
    },

    _onDateChange: function(ev) {
        const startDateStr = this.$el.find('#start_date').val();
        const endDateStr = this.$el.find('#end_date').val();
        let days = 0;
        if (startDateStr && endDateStr) {
            const start = new Date(startDateStr);
            const end = new Date(endDateStr);
            days = Math.max(0, Math.ceil((end - start) / (1000 * 60 * 60 * 24)));
        }
        this.$el.find(".tot_days").text(days);
    },

    _onFieldChange: function (ev) {
        const $row = $(ev.currentTarget).closest('tr');
        this._updateRowTotal($row);
        this._updateOverallTotal();
    },

    _updateRowTotal: function ($row) {
        const quantity = parseFloat($row.find('.quantity_input').val());
        const amount = parseFloat($row.find('.quantity_input').data('amount'));
        const days = this.$el.find('.tot_days').text();
        const total = quantity * amount * days;
        $row.find('.total-amount').text(total.toFixed(2));
        $row.data('computed-total', total);
    },

    _updateOverallTotal: function () {
        let totalAmount = 0;
        this.$el.find('.property_order_line').each(function () {
            const rawTotal = $(this).data('computed-total');
            totalAmount += rawTotal;
        });
        this.$el.find('.total_amnt').text(totalAmount.toFixed(2));
    },

    _onClickSubmit: async function (ev) {
       ev.preventDefault();
       var tenant_id = this.$el.find('#tenant_id').val();
       var start_date = this.$el.find('#start_date').val();
       var end_date = this.$el.find('#end_date').val();
       var tot_days = this.$el.find('.tot_days').text().trim();
       var c = 0;
       var property_type = this.$el.find('#property_type').val();
       var property_line_ids = [];
       var property_list=[]
       var self = this
       $('#property_table tbody tr.property_order_line').each(function () {
           let property = self.$el.find('td.property').text().trim();
           let owner = self.$el.find('td.owner').text().trim();
           let date = self.$el.find('td.build_date').text().trim();
           let quantity = self.$el.find('input[name="quantity"]').val();
           let invoiced = self.$el.find('td.invoiced_qty').text().trim() || 0;
           let amount_text = self.$el.find('td.amount').text().trim();
           let amount = parseFloat(amount_text.replace(/[^0-9.]/g, '')) || 0;
           let total_amountText = self.$el.find('td.total_amount').text().trim();
           let total_amount = parseFloat(total_amountText.replace(/[^0-9.]/g, '')) || 0;
           if (property_list.includes(property)&&(c==0))
           {
                c=1;
                self.$el.find(".value").text("Same property cannot be chosen");
                self.$el.find("#customDialog").modal('show');
           }
           else
           {
                property_list.push(property)
           }
           if ((quantity <= 0)&&(c==0))
           {
                c=1;
                self.$el.find(".value").text("Quantity must be minimum of 1");
                self.$el.find("#customDialog").modal('show');
           }
           property_line_ids.push({
               'intermediate_management_id': property,
               'owner_id':owner,
               'date':date,
               'quantity': quantity,
               'invoiced_qty': invoiced,
               'amount': amount,
               'total_amount': total_amount,
           });
       });
       if (c==0)
       {
           this.$el.find("#customDialog").modal('hide');
           try {
               let response = await rpc('/webform/submit', {
                   tenant_id: tenant_id,
                   property_type: property_type,
                   start_date: start_date,
                   end_date: end_date,
                   total_days: tot_days,
                   property_line_ids: property_line_ids,
               });
               window.location.href = "http://localhost:8017/contactus-thank-you";
           } catch (error) {
               this.$el.find(".value").text("Failed to proceed with the request. Please try again later");
               this.$el.find("#customDialog").modal('show');
           }
       }
    },
});
