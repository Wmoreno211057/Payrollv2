from odoo import api, models


class payslip_report(models.AbstractModel):
    _inherit = 'report.hr_payroll.report_payslip'

    @api.model
    def _get_report_values(self, docids, data=None):
        payslips = self.env['hr.payslip'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'docs': payslips,
            'data': data,
            # 'get_details_by_rule_category': self.appears_on_payslip(),
            'get_lines_by_contribution_register': self.get_payslip_lines(),
        }

    def convert(self,amount, cur):
        amt_en = cur.amount_to_text(amount)
        return amt_en

    def get_payslip_lines(self):
        payslip_line = self.env['hr.payslip.line']
        res = []
        ids = []
        for rec in self:
            if rec.get_payslip_lines() is True:
                ids.append(rec.id)
        if ids:
            res = payslip_line.browse(ids)
        return res

    def get_leave(self, obj):
        res = []
        ids = []
        for rec in self:
            if rec.type == 'leaves':
                ids.append(rec.id)
            payslip_line = self.env['hr.payslip.line']
            if ids:
                res = payslip_line.browse(ids)
        return res
