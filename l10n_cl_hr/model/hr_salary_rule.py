from odoo import api, fields, models, tools, _


class hr_salary_rule(models.Model):
    _inherit = 'hr.salary.rule'
    _description = 'Salary Rule'
    
    date_start = fields.Date('Fecha Inicio',  help="Fecha de inicio de la regla salarial")
    date_end = fields.Date('Fecha Fin',  help="Fecha del fin de la regla salarial")
    register_id = fields.Many2one(comodel_name="hr.contribution.register",
                                  string="Registro de Contribución")
    input_ids = fields.One2many('hr.rule.input', 'input_id', string='Inputs',
                                copy=True)


# Antes estaba en Payroll pero fue eliminado
class HrContributionRegister(models.Model):
    _name = 'hr.contribution.register'
    _description = 'Contribution Register'

    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get())
    partner_id = fields.Many2one('res.partner', string='Partner')
    name = fields.Char(required=True)
    register_line_ids = fields.One2many('hr.payslip.line', 'register_id',
        string='Register Line', readonly=True)
    note = fields.Text(string='Description')


# Antes estaba en Payroll pero fue eliminado
class HrRuleInput(models.Model):
    _name = 'hr.rule.input'
    _description = 'Salary Rule Input'

    name = fields.Char(string='Description', required=True)
    code = fields.Char(required=True, help="The code that can be used in the salary rules")
    input_id = fields.Many2one('hr.salary.rule', string='Salary Rule Input', required=True)