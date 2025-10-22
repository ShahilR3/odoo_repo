/** @odoo-model **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { useService} from "@web/core/utils/hooks";

const actionRegistry = registry.category("actions");


class SaleDashboard extends Component {
    setup() {
         super.setup()
         this.orm = useService('orm')
         this._fetch_data();
         this.state = useState({
            countries: [],
            selected: '',
         });
         this.category = useState({
            categories: [],
            selected: '',
         });
    };
    async _fetch_data(period = "", country = "", category = ""){
        let result = await this.orm.call("sale.order", "get_dashboard_data", [period, country, category], {})
        this.result = result
        this.sales_team = result.sales_team
        this.salesBarGraph()
        this.sales_person = result.sales_person
        this.personPieGraph()
        this.top_customers = result.top_customers
        this.topBarGraph()
        this.ls_product = this.result.ls_product
        this.LSPLineGraph()
        this.order_state = this.result.order_state
        this.OSGraph()
        this.quotation = this.result.quotation
        this.Quote()
    };
    Quote()
    {
        document.getElementById('quote').value = String(this.quotation)
        document.getElementById('rev').value = String(this.result.currency_symbol)+String(this.result.amount)
        document.getElementById('exrev').value = String(this.result.currency_symbol)+String(this.result.expected_amount)
        this.state.countries = this.result.country.map(c => c[0])
        this.category.categories = this.result.category.map(c=>c[0])
    }
    onClear(ev){
        document.getElementById('period').value = ""
        this._fetch_data("",country.value,category.value)
    }
    onChangeCountry(ev) {
        this.state.selected = ev.target.value;
    }
    onChangeCategory(ev){
        this.category.selected = ev.target.value;
    }
    onClickApply(){
        const period = document.getElementById('period').value;
        const country = document.getElementById('country').value;
        const category = document.getElementById('category').value;
        this._fetch_data(period, country, category);
    };
    onClickTeam(ev)
    {
        const btn = String(ev.target.value);
        if (btn === 'product')
        {
            this.sales_team = this.result.sales_team_prod;
            this.salesBarGraph()
        }
        else
        {
            this.sales_team = this.result.sales_team;
        }
        this.salesBarGraph()
    }
    onClickCus(ev)
    {
        const btn = String(ev.target.value);
        if (btn === 'product')
        {
            this.top_customers = this.result.top_customers_prod;
            this.topBarGraph()
        }
        else
        {
            this.top_customers = this.result.top_customers;
        }
        this.topBarGraph()
    }
    onClickBtn(ev)
    {
        const btn = String(ev.target.value);
        if (btn === 'invoice')
        {
            this.order_state = this.result.invoice_state;
            this.OSGraph()
        }
        else
        {
            this.order_state = this.result.order_state;
        }
        this.OSGraph()
    }
    onSelectChange(ev)
    {
        const op = ev.target.value;
        if (op === "highest") {
            this.ls_product = this.result.hs_product;
        } else {
            this.ls_product = this.result.ls_product;
        }
        this.LSPLineGraph();
    }
    salesBarGraph() {
        const ctx = document.getElementById('sales');
        if(!this.sbChart)
        {
            this.sbChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: this.sales_team.map(c=>c[1]),
                    datasets: [{
                        label: "Sales Amount",
                        data: this.sales_team.map(c=>c[2]),
                        backgroundColor: ['#FF2C66','cyan','maroon'],
                        borderColor:'black',
                        borderWidth: 2
                    }]
                },
                options: {
                    scales: {
                        x:{
                            ticks:{
                                color: 'white'
                            },
                            grid:{
                                color: 'rgba(255, 255, 255, 0.1)'
                            }
                        },
                        y:{
                            ticks:{
                                color: 'white'
                            },
                            grid:{
                                color: 'rgba(255, 255, 255, 0.1)'
                            }
                        },
                    },
                    plugins:{
                        legend:{
                            labels:{
                                color:'#FFFFFF'
                            }
                        }
                    },
                },
            });
        }
        else
        {
           this.sbChart.data.labels = this.sales_team.map(c=>c[1])
           this.sbChart.data.datasets[0].data = this.sales_team.map(c=>c[2])
           this.sbChart.update()
        }
   }
   personPieGraph() {
        const ctx = document.getElementById('sales_person');
        if(!this.ppChart){
            this.ppChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: this.sales_person.map(c => c[1]),
                    datasets: [{
                        data: this.sales_person.map(c => c[2]),
                        backgroundColor: ['#00C2A8','#5C5CFF'],
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            labels: {
                                color: "white",
                            }
                        },
                    },
                },
            });
        }else
        {
           this.ppChart.data.labels = this.sales_person.map(c=>c[1])
           this.ppChart.data.datasets[0].data = this.sales_person.map(c=>c[2])
           this.ppChart.update()
        }
   }
   topBarGraph() {
        const ctx = document.getElementById('top_cus');
        if (!this.tbChart)
        {
            this.tbChart= new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: this.top_customers.map(c => c[1]),
                    datasets: [{
                        label: 'Total Sales',
                        data: this.top_customers.map(c => c[2]),
                        backgroundColor: '#E6BE8A',
                        borderColor:'black',
                        borderWidth: 2
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    scales: {
                        x:{
                            beginAtZero: true,
                            ticks:{
                                color: 'white'
                            },
                            grid:{
                                color: 'rgba(255, 255, 255, 0.1)'
                            }
                        },
                        y:{
                            ticks:{
                                color: 'white'
                            },
                            grid:{
                                color: 'rgba(255, 255, 255, 0.1)'
                            }
                        },
                    },
                    plugins:{
                        legend:{
                            labels:{
                                color:'#FFFFFF'
                            }
                        }
                    }
                },
            });
        }
        else{
            this.tbChart.data.labels = this.top_customers.map(c => c[1]);
            this.tbChart.data.datasets[0].data = this.top_customers.map(c => c[2]);
            this.tbChart.update();
        }
   }
   LSPLineGraph() {
        const ctx = document.getElementById('ls_product');
        if (!this.lsChart) {
            this.lsChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: this.ls_product.map(c => c[0]),
                    datasets: [{
                        data: this.ls_product.map(c => c[1]),
                        label: "Products sold",
                        borderColor: '#3D8BFF',
                        backgroundColor: '#3D8BFF',
                        pointBackgroundColor: '#1c1c1c',

                    }]
                },
                options: {
                    responsive: true,
                    indexAxis: 'y',
                    animation: {
                        duration: 1000,
                        easing: 'easeOutCubic'
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: {
                                color: '#FFFFFF'
                            },
                         },
                        y: {
                            ticks: {
                                color: '#FFFFFF'
                            },
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: {
                                color: '#FFFFFF'
                            }
                        }
                    },
                }
            });
        } else {
            this.lsChart.data.labels = this.ls_product.map(c => c[0]);
            this.lsChart.data.datasets[0].data = this.ls_product.map(c => c[1]);
            this.lsChart.update();
        }
   }
   OSGraph()
   {
        const ctx = document.getElementById("os")
        if (!this.osChart)
        {
            this.osChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: this.order_state.map(c => c[0]),
                    datasets: [{
                        data: this.order_state.map(c => c[1]),
                        label: "Total Amount",
                        borderColor: '#009081',
                        backgroundColor: '#009081',
                        pointBackgroundColor: '#009081',
                    }]
                },
                options: {
                    responsive: true,
                    indexAxis: 'y',
                    animation: {
                        duration: 1000,
                        easing: 'easeOutCubic'
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: {
                                color: '#FFFFFF'
                            },
                        },
                        y: {
                            ticks: {
                                color: '#FFFFFF'
                            },
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: {
                                color: '#FFFFFF'
                            }
                        }
                    },
                }
            });
        } else {
            this.osChart.data.labels = this.order_state.map(c => c[0]);
            this.osChart.data.datasets[0].data = this.order_state.map(c => c[1]);
            this.osChart.update();
        }
   }
}
SaleDashboard.template = "sales_dashboard.SaleDashboard";
actionRegistry.add("sale_dashboard_tag", SaleDashboard);
