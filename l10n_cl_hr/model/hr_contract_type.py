from odoo import api, fields, models, tools, _


class HrPayrollStructureType(models.Model):
    _inherit = 'hr.payroll.structure.type'
    _description = 'Tipo de Contrato'

    codigo = fields.Char('Codigo')