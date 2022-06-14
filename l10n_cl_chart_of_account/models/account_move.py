# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    amount_retencion = fields.Monetary(
        string="Retención",
        default=0.00,
    )
    retencion_account_id = fields.Many2one(
        'account.account',
        string='Tax Account',
        domain=[('deprecated', '=', False)],
    )

    @api.depends('price_unit', 'discount', 'tax_ids', 'quantity',
                 'product_id', 'move_id.partner_id', 'move_id.currency_id',
                 'move_id.company_id', 'move_id.invoice_date', 'move_id.date')
    def _compute_price(self):
        currency = self.move_id and self.move_id.currency_id or None
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = False
        if self.tax_ids:
            taxes = self.tax_ids.compute_all(price, currency, self.quantity,
                                             product=self.product_id,
                                             partner=self.move_id.partner_id,
                                             uom_id=self.product_uom_id)
        self.price_subtotal = price_subtotal_signed = taxes[
            'total_excluded'] if taxes else self.quantity * price
        self.price_total = taxes[
            'total_included'] if taxes else self.price_subtotal
        if self.move_id.currency_id and self.move_id.currency_id != self.move_id.company_id.currency_id:
            currency = self.move_id.currency_id
            date = self.move_id.date or self.move_id.invoice_date
            price_subtotal_signed = currency._convert(price_subtotal_signed,
                                                      self.move_id.company_id.currency_id,
                                                      self.company_id or self.env.user.company_id,
                                                      date or fields.Date.today())
        sign = self.move_id.move_type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign


class AccountMove(models.Model):
    _inherit = 'account.move'

    amount_retencion = fields.Monetary(
        string="Retención",
        default=0.00,
        compute='_compute_amount',
    )

    @api.depends('invoice_line_ids.price_subtotal', 'amount_tax',
                 'currency_id', 'company_id', 'invoice_date', 'move_type')
    def _compute_amount(self):
        # TODO Buscar una mejor forma de aplicar retención
        amount_retencion = 0
        neto = 0
        amount_tax = 0
        included = False
        for tax in self.line_ids:
            if tax.tax_line_id.price_include:
                included = True
            amount_tax += tax.tax_base_amount
            amount_retencion += tax.amount_retencion
        self.amount_retencion = amount_retencion
        if included:
            neto += self.currency_id
            amount_retencion += amount_retencion
        else:
            neto += sum(line.price_subtotal for line in self.invoice_line_ids)
        self.amount_untaxed = neto
        self.amount_tax = amount_tax
        self.amount_total = neto + amount_tax - amount_retencion
        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
            currency_id = self.currency_id
            amount_total_company_signed = currency_id._convert(
                self.amount_total, self.company_id.currency_id, self.company_id,
                self.invoice_date or fields.Date.today())
            amount_untaxed_signed = currency_id._convert(self.amount_untaxed,
                                                         self.company_id.currency_id,
                                                         self.company_id,
                                                         self.invoice_date or fields.Date.today())
        sign = self.move_type in ['in_refund', 'out_refund'] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign

    # def get_taxes_values(self):
    #     tax_grouped = {}
    #     round_curr = self.currency_id.round
    #     for line in self.invoice_line_ids:
    #         price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
    #         taxes = line.tax_line_id.compute_all(price_unit, self.currency_id,
    #                                    line.quantity, line.product_id, self.partner_id)['taxes']
    #         for tax in taxes:
    #             val = self._prepare_tax_line_vals(line, tax)
    #             key = self.env['account.tax'].browse(tax['id']).get_grouping_key(val)
    #
    #             if key not in tax_grouped:
    #                 tax_grouped[key] = val
    #                 tax_grouped[key]['base'] = round_curr(val['base'])
    #             else:
    #                 tax_grouped[key]['amount'] += val['amount']
    #                 tax_grouped[key]['base'] += round_curr(val['base'])
    #     return tax_grouped
