/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
     static props = {
        record: Object,
        name: String,
        readonly: Boolean,
        options: Object,
        id: String,
    };
    setup() {
        this.state = useState({
            count: this.props.record.data[this.props.name] ?? 0,
            min: this.props.options.min?? 0,
            max: this.props.options.max?? 1000,
            step: this.props.options.step?? 10,
        });
    }
    onSlide(ev) {
        const newVal = parseInt(ev.target.value);
        this.state.count = newVal;
        if(!this.props.readonly){
           this.props.record.update({ [this.props.name]: newVal });
        }
    }
}
Counter.template = 'owl.RangeField';
Counter.supportedTypes = ['integer'];
registry.category('fields').add('range_val', {
    component: Counter,
    extractProps: ({options})=>({
        options,
    })
});
