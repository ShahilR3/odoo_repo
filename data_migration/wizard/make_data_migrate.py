#-*- coding: utf-8 -*-

import xmlrpc.client

from odoo import fields, models
from odoo.exceptions import ValidationError


class DataMigrate(models.TransientModel):
    """Wizard for Migrating the data"""
    _name = "make.data.migrate"

    url_db1 = fields.Char("Source URl")
    db_1 = fields.Char("Source Database name")
    username_db_1 = fields.Char("Source Username")
    password_db_1 = fields.Char("Source Password")
    url_db2 = fields.Char("Destination URl")
    db_2 = fields.Char("Destination Database name")
    username_db_2 = fields.Char("Destination Username")
    password_db_2 = fields.Char("Destination Password")

    def action_configuration(self):
        """Migration Proccess begins"""
        common_1 = xmlrpc.client.ServerProxy(f'{self.url_db1}/xmlrpc/2/common')
        models_1 = xmlrpc.client.ServerProxy(f'{self.url_db1}/xmlrpc/2/object')
        common_2 = xmlrpc.client.ServerProxy(f'{self.url_db2}/xmlrpc/2/common')
        models_2 = xmlrpc.client.ServerProxy(f'{self.url_db2}/xmlrpc/2/object')
        uid_db_1 = common_1.authenticate(self.db_1, self.username_db_1, self.password_db_1, {})
        uid_db2 = common_2.authenticate(self.db_2, self.username_db_2, self.password_db_2, {})
        print(uid_db_1)
        print(uid_db2)
        if not uid_db_1 or not uid_db2:
            raise ValidationError("Wrong Credentials")
        moves_src = models_1.execute_kw(self.db_1, uid_db_1, self.password_db_1, 'account.move', 'search_read', [[]],
                                        {'fields': ['id', 'name', 'journal_id', 'partner_id', 'date', 'ref', 'move_type'
                                            , 'invoice_date']})
        lines_src = models_1.execute_kw(self.db_1, uid_db_1, self.password_db_1, 'account.move.line', 'search_read',
                                        [[]], {'fields': ['move_id', 'account_id', 'name', 'quantity', 'price_unit',
                                                          'price_subtotal']})
        journals_dst = models_2.execute_kw(self.db_2, uid_db2,self.password_db_2, 'account.journal', 'search_read', [[]],
                                           {'fields': ['id', 'code', 'name']})
        partners_dst = models_2.execute_kw(self.db_2, uid_db2,self.password_db_2, 'res.partner', 'search_read', [[]],
                                           {'fields': ['id', 'name']})
        journal_map = {}
        for js in journals_dst:
            journal_map[js['name']] = js['id']
            if js.get('code'):
                journal_map[js['code']] = js['id']
        partner_map = {p['name']: p['id'] for p in partners_dst}
        move_map = {}
        for move in moves_src:
            old_partner_id = move.get('partner_id', False)
            new_journal_id = None
            new_partner_id = None
            if move['journal_id']:
                journal_name = move['journal_id'][1]
                new_journal_id = journal_map.get(journal_name)
            if old_partner_id:
                partner_name = move['partner_id'][1]
                new_partner_id = partner_map.get(partner_name)
                if not new_partner_id:
                    new_partner_id = models_2.execute_kw(
                        self.db_2, uid_db2,self.password_db_2,
                        'res.partner', 'create',
                        [{'name': partner_name}]
                    )
                    partner_map[partner_name] = new_partner_id
            vals = {
                'name': move['name'],
                'ref': move.get('ref', ''),
                'journal_id': new_journal_id or list(journal_map.values())[0],
                'partner_id': new_partner_id or False,
                'date': move.get('date'),
                'move_type': move.get('move_type', 'entry'),
                'invoice_date': move.get('invoice_date'),
            }
            try:
                existing = models_2.execute_kw(
                    self.db_2, uid_db2,self.password_db_2,
                    'account.move', 'search',
                    [[('name', '=', move.get('name'))]],
                    {'limit': 1}
                )
                if existing:
                    move_map[move['id']] = existing
                    print("existing")
                    continue
                new_move_id = models_2.execute_kw(
                    self.db_2, uid_db2,self.password_db_2,
                    'account.move', 'create',
                    [vals]
                )
                move_map[move['id']] = new_move_id
            except Exception as e:
                print(f"Failed to create move {move['id']}: {e}")
        accounts_src = models_1.execute_kw(self.db_1, uid_db_1, self.password_db_1, 'account.account', 'search_read', [[]],
                                           {'fields': ['id', 'code', 'name', 'account_type']})
        accounts_dst = models_2.execute_kw(self.db_2, uid_db2,self.password_db_2, 'account.account', 'search_read', [[]],
                                           {'fields': ['id', 'code', 'name', 'account_type']})
        account_map = {}
        for src in accounts_src:
            match = next(
                (dst for dst in accounts_dst if dst.get('code') == src.get('code')),
                None
            )
            if match:
                account_map[src['id']] = match['id']
        for src in accounts_src:
            existing = models_2.execute_kw(
                self.db_2, uid_db2,self.password_db_2,
                'account.account', 'search',
                [[('code', '=', src.get('code'))]],
                {'limit': 1}
            )
            if existing:
                account_map[src['id']] = existing[0]
                continue
            new_account_id = models_2.execute_kw(
                self.db_2, uid_db2,self.password_db_2,
                'account.account', 'create',
                [{
                    'name': src['name'],
                    'code': src.get('code') or '',
                    'account_type': src.get('account_type'),
                }]
            )
            account_map[src['id']] = new_account_id
        for line in lines_src:
            old_move_id = line['move_id'][0] if isinstance(line.get('move_id'), list) else line.get('move_id')
            new_move_id = move_map.get(old_move_id)
            line['move_id'] = new_move_id[0] if isinstance(new_move_id, list) else new_move_id
            existing = models_2.execute_kw(self.db_2, uid_db2,self.password_db_2,'account.move.line', 'search',
                                           [[
                                               ('move_id', '=', line['move_id']),
                                               ('name', '=', line.get('name', '')),
                                               ('quantity', '=', line.get('quantity', 0)),
                                               ('price_unit', '=', line.get('price_unit', 0)),
                                           ]],
                                           {'limit': 1})
            if existing or not new_move_id:
                continue
            old_account_id = line['account_id'][0] if isinstance(line['account_id'], list) else line['account_id']
            line['account_id'] = account_map.get(old_account_id)
            models_2.execute_kw(self.db_2, uid_db2,self.password_db_2, 'account.move.line', 'create', [line])
