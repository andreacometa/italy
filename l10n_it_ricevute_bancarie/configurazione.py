# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 OCA (Odoo Community Association)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, orm


class riba_configurazione(orm.Model):

    _name = "riba.configuration"
    _description = "Configuration data for Ricevute Bancarie management"

    _columns = {
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'name': fields.char("Description", size=64, required=True),
        'type': fields.selection(
            (('sbf', 'Salvo buon fine'), ('incasso', 'Al dopo incasso')),
            "Issue mode", required=True),
        'bank_id': fields.many2one(
            'res.partner.bank', "Bank", required=True,
            help="Bank account used for Ri.Ba. issuing"),
        'acceptance_journal_id': fields.many2one(
            'account.journal', "Acceptance journal",
            domain=[('type', '=', 'bank')],
            help="Journal used when Ri.Ba. is accepted by the bank"),
        'acceptance_account_id': fields.many2one(
            'account.account', "Acceptance account",
            domain=[('type', '=', 'receivable')],
            help='Account used when Ri.Ba. is accepted by the bank'),
        'accreditation_journal_id': fields.many2one(
            'account.journal', "Accreditation journal",
            domain=[('type', '=', 'bank')],
            help="Journal used when Ri.Ba. amount is accredited by the bank"),
        'accreditation_account_id': fields.many2one(
            'account.account', "Ri.Ba. bank account",
            help='Account used when Ri.Ba. is accepted by the bank'),
        'bank_account_id': fields.many2one(
            'account.account', "Bank account",
            domain=[('type', '=', 'liquidity')]),
        'bank_expense_account_id': fields.many2one(
            'account.account', "Bank Expenses account"),
        'unsolved_journal_id': fields.many2one(
            'account.journal', "Unsolved journal",
            domain=[('type', '=', 'bank')],
            help="Journal used when Ri.Ba. is unsolved"),
        'overdue_effects_account_id': fields.many2one(
            'account.account', "Overdue Effects account",
            domain=[('type', '=', 'receivable')]),
        'protest_charge_account_id': fields.many2one(
            'account.account', "Protest charge account"),
    }

    _defaults = {
        'company_id': (
            lambda self, cr, uid, c: self.pool[
                'res.company']._company_default_get(cr, uid,
                                                    'riba.configuration',
                                                    context=c)),
    }

    def get_default_value_by_list(self, cr, uid, field_name, context=None):
        if context is None:
            context = {}
        if not context.get('active_id', False):
            return False
        list_obj = self.pool['riba.list']
        list = list_obj.browse(cr, uid, context['active_id'], context=context)
        return list.config[field_name] and list.config[field_name].id or False

    def get_default_value_by_list_line(self, cr, uid, field_name,
                                       context=None):
        if context is None:
            context = {}
        if not context.get('active_id', False):
            return False
        list_line = self.pool['riba.list.line'].browse(cr, uid,
                                                       context['active_id'],
                                                       context=context)
        return (list_line.list_id.config[field_name] and
                list_line.list_id.config[field_name].id or False)
