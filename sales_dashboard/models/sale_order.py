# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def get_dashboard_data(self, period="", country="", category=""):
        filters = self._get_filter_conditions(period, country, category)
        return {
            'sales_team': self.sales_team(filters),
            'sales_team_prod': self.sales_team_product(filters),
            'sales_person': self.sales_person(filters),
            'top_customers': self.top_customers(filters),
            'top_customers_prod': self.top_customers_product(filters),
            'ls_product': self.ls_product(filters),
            'hs_product': self.hs_product(filters),
            'order_state': self.order_state(filters),
            'invoice_state': self.invoice_state(filters),
            'quotation': self.quotation(filters),
            'amount': self.revenue(filters),
            'expected_amount': self.expected_revenue(filters),
            'currency_symbol': self.currency(),
            'country': self.country(),
            'category': self.category(),
        }

    def quotation(self, filters):
        where_clause = f" AND {filters['where']}" if filters['where'] else ''
        query = f"""Select 
        Count( Distinct so.name) 
        from sale_order so
        join sale_order_line sol on sol.order_id = so.id
        join res_partner rp on rp.id = so.partner_id
        join product_product pp on pp.id = sol.product_id
        join product_template pt on pt.id = pp.product_tmpl_id
        {where_clause}"""
        self.env.cr.execute(query, filters['params'])
        return self.env.cr.fetchall()

    def country(self):
        self.env.cr.execute("""SELECT rc.name ->> 'en_US'
                FROM res_country rc
                """)
        return self.env.cr.fetchall()

    def category(self):
        self.env.cr.execute("""Select complete_name from product_category""")
        return self.env.cr.fetchall()

    def currency(self):
        self.env.cr.execute("""SELECT DISTINCT rc.symbol AS symbol
        FROM sale_order so
        JOIN res_currency rc ON rc.id = so.currency_id
        JOIN res_company c ON c.id = so.company_id;
        """)
        return self.env.cr.fetchall()

    def top_customers(self, filters, limit=10):
        where_clause = f" AND {filters['where']}" if filters['where'] else ""
        query = f""" Select 
        so.partner_id, 
        rp.name, 
        SUM(so.amount_total) as sales 
        from sale_order so
        Join res_partner rp On rp.id = so.partner_id
        join sale_order_line sol on sol.order_id = so.id
        JOIN product_product pp ON sol.product_id = pp.id
        JOIN product_template pt ON pp.product_tmpl_id = pt.id
        Where so.state in ('sale','done') {where_clause}
        group by so.partner_id, rp.name
        order by sales desc
        Limit %s
        """
        self.env.cr.execute(query, filters['params'] + [limit])
        return self.env.cr.fetchall()

    def top_customers_product(self, filters, limit=10):
        where_clause = f" AND {filters['where']}" if filters['where'] else ""
        query = f"""Select
        so.partner_id,
        rp.name,
        SUM(sol.product_uom_qty) as sales
        from sale_order so
        Join res_partner rp On rp.id = so.partner_id
        join sale_order_line sol on sol.order_id = so.id
        JOIN product_product pp ON sol.product_id = pp.id
        JOIN product_template pt ON pp.product_tmpl_id = pt.id
        Where so.state in ('sale', 'done') {where_clause}
        group by so.partner_id, rp.name
        order by sales desc
        Limit %s
        """
        self.env.cr.execute(query, filters['params'] + [limit])
        return self.env.cr.fetchall()

    def sales_team(self, filters):
        where_clause = f" AND {filters['where']}" if filters['where'] else ""
        query = f"""Select 
        team_id,
        ct.name ->> 'en_US' as team_name,
        SUM(so.amount_total) as sales
        from sale_order so
        join crm_team ct on ct.id = so.team_id
        Join res_partner rp On rp.id = so.partner_id
        Join sale_order_line sol on sol.order_id = so.id
        JOIN product_product pp ON sol.product_id = pp.id
        JOIN product_template pt ON pp.product_tmpl_id = pt.id
        where so.state in ('sale','done') {where_clause}
        group by team_id, team_name
        order by sales desc
        """
        self.env.cr.execute(query, filters['params'])
        return self.env.cr.fetchall()

    def sales_team_product(self, filters):
        where_clause = f" AND {filters['where']}" if filters['where'] else ""
        query = f"""Select 
        team_id,
        ct.name ->> 'en_US' as team_name,
        SUM(sol.product_uom_qty) as sales 
        from sale_order so
		join crm_team ct on ct.id = so.team_id
		join res_users ru on ru.id = so.user_id
		join res_partner rp on rp.id = ru.partner_id
		join sale_order_line sol on sol.order_id = so.id
		JOIN product_product pp ON sol.product_id = pp.id
        JOIN product_template pt ON pp.product_tmpl_id = pt.id
        Where so.state in ('sale','done') {where_clause}
        group by team_id, team_name
        order by sales desc"""
        self.env.cr.execute(query, filters['params'])
        result = self.env.cr.fetchall()
        return result

    def sales_person(self, filters):
        where_clause = f" AND {filters['where']}" if filters['where'] else ""
        query = f"""Select 
        so.user_id,
        sal.name,
        SUM(so.amount_total) as sales 
        from sale_order so
        join sale_order_line sol on sol.order_id = so.id
        join res_users ru on ru.id = so.user_id
        join res_partner sal on sal.id = ru.partner_id
        join res_partner rp on rp.id = so.partner_id
        JOIN product_product pp ON sol.product_id = pp.id
        JOIN product_template pt ON pp.product_tmpl_id = pt.id
        where so.state in ('sale','done') {where_clause}
        group by so.user_id, sal.name
        order by sales desc
        """
        self.env.cr.execute(query, filters['params'])
        return self.env.cr.fetchall()

    def ls_product(self, filters):
        where_clause = f" AND {filters['where']}" if filters['where'] else ""
        query = f"""Select 
        pt.name ->> 'en_US'as pp_name, 
        SUM(sol.product_uom_qty) as qty 
        from sale_order_line sol
        JOIN product_product pp ON sol.product_id = pp.id
        JOIN product_template pt ON pp.product_tmpl_id = pt.id
        join sale_order so on so.id = sol.order_id
        JOIN res_partner rp ON so.partner_id = rp.id
        where so.state in('sale','done') {where_clause}
        Group by pt.name
        order by qty asc
        """
        self.env.cr.execute(query, filters['params'])
        return self.env.cr.fetchall()

    def hs_product(self, filters):
        where_clause = f" AND {filters['where']}" if filters['where'] else ""
        query = f"""Select 
        pt.name ->> 'en_US'as pp_name, 
        SUM(sol.product_uom_qty) as qty 
        from sale_order_line sol
        JOIN product_product pp ON sol.product_id = pp.id
        JOIN product_template pt ON pp.product_tmpl_id = pt.id
        join sale_order so on so.id = sol.order_id
        JOIN res_partner rp ON so.partner_id = rp.id
        where so.state in('sale','done') {where_clause}
        Group by pt.name
        order by qty desc
        """
        self.env.cr.execute(query, filters['params'])
        return self.env.cr.fetchall()

    def order_state(self, filters):
        where_clause = f" AND {filters['where']}" if filters['where'] else ""
        query = f"""Select 
        sol.state, 
        SUM(so.amount_total) as qty 
        from sale_order_line sol
		join sale_order so on so.id = sol.order_id
		JOIN product_product pp ON sol.product_id = pp.id
        JOIN product_template pt ON pp.product_tmpl_id = pt.id
        JOIN res_partner rp ON so.partner_id = rp.id {where_clause}
        Group by sol.state
        order by qty
        """
        self.env.cr.execute(query, filters['params'])
        return self.env.cr.fetchall()

    def invoice_state(self, filters):
        where_clause = f" AND {filters['where']}" if filters['where'] else ""
        query = f"""Select
        so.invoice_status as apm,
        SUM(so.amount_total) as qty
        from sale_order so
        join sale_order_line sol on sol.order_id = so.id
        JOIN product_product pp ON sol.product_id = pp.id
        JOIN product_template pt ON pp.product_tmpl_id = pt.id
        JOIN res_partner rp ON so.partner_id = rp.id {where_clause}
        Group by apm 
        order by qty desc
        """
        self.env.cr.execute(query, filters['params'])
        return self.env.cr.fetchall()

    def revenue(self, filters):
        where_clause = f" AND {filters['where']}" if filters['where'] else ""
        query = f"""Select 
        SUM(so.amount_total)
        from sale_order so
		join sale_order_line sol on sol.order_id = so.id
		JOIN product_product pp ON sol.product_id = pp.id
        JOIN product_template pt ON pp.product_tmpl_id = pt.id
		JOIN res_partner rp ON so.partner_id = rp.id
		where so.state in ('sale') {where_clause}
		"""
        self.env.cr.execute(query, filters['params'])
        result = self.env.cr.fetchall()
        if result == [(None,)]:
            result = [(0.0,)]
        return result

    def expected_revenue(self, filters):
        where_clause = f" AND {filters['where']}" if filters['where'] else ""
        query = f"""Select 
        SUM(so.amount_total)
        from sale_order so
        join sale_order_line sol on sol.order_id = so.id
        JOIN product_product pp ON sol.product_id = pp.id
        JOIN product_template pt ON pp.product_tmpl_id = pt.id
        JOIN res_partner rp ON so.partner_id = rp.id
        where so.state in ('draft','sent') {where_clause}
        """
        self.env.cr.execute(query, filters['params'])
        result = self.env.cr.fetchall()
        if result == [(None,)]:
            result = [(0.0,)]
        return result

    def _get_filter_conditions(self, period, country, category):
        today = fields.Date.today()
        where_clauses = []
        params = []
        domain = []
        if period:
            if period == 'year_to_date':
                start_date = today.replace(month=1, day=1)
            elif period == 'last_week':
                start_date = today - timedelta(days=7)
            elif period == 'last_month':
                start_date = today - timedelta(days=30)
            elif period == 'last_three_months':
                start_date = today - timedelta(days=90)
            elif period == 'last_six_months':
                start_date = today - timedelta(days=180)
            elif period == 'last_year':
                start_date = today - timedelta(days=365)
            elif period == 'last_three_years':
                start_date = today - timedelta(days=3 * 365)
            else:
                start_date = None
            where_clauses.append("so.date_order >= %s")
            params.append(start_date)
            domain.append(('date_order', '>=', start_date))
        if country:
            where_clauses.append("rp.country_id IN (SELECT id FROM res_country WHERE name->>'en_US' ILIKE %s)")
            params.append(f'%{country}%')
            domain.append(('country_id.name', 'ilike', country))
        if category:
            where_clauses.append("pt.categ_id IN (SELECT id FROM product_category WHERE complete_name::text ILIKE %s)")
            params.append(f'%{category}%')
            domain.append(('order_line.product_id.categ_id.name', 'ilike', category))
        return {
            'where': ' AND '.join(where_clauses),
            'params': params,
            'domain': domain,
        }
