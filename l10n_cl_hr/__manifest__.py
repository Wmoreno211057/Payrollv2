{
    'name': 'Chilean Payroll & Human Resources',
    'author': 'Konos',
    'website': 'http://konos.cl',
    'license': 'AGPL-3',
    'depends': [
        'hr',
        'hr_holidays',
        'hr_payroll',
        'hr_payroll_account',
    ],
    'external_dependencies': {
        'python': [
            'num2words'
        ]
    },
    'contributors': [
        "Nelson Ramirez <info@konos.cl>",
        "Daniel Blanco Martin <daniel@blancomartin.com>",
        "Carlos Lopez Mite <celm1990@hotmail.com>",
        "Daniel Santibáñez Polanco <dsantibanez@globalresponse.cl>",
    ],
    'license': 'AGPL-3',
    'version': '14.0.1.0.4',
    'description': """
Chilean Payroll & Human Resources.
==================================
    -Payroll configuration for Chile localization.
    -All contributions rules for Chile payslip.
    * Employee Basic Info
    * Employee Contracts
    * Attendance, Holidays and Sick Licence
    * Employee PaySlip
    * Allowances / Deductions / Company Inputs
    * Extra Time
    * Pention Chilean Indicators
    * Payroll Books
    * Previred Plain Text
    , ...
    Report
  """,
    'category': 'Localization/Chile',
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Menus
        'views/menu_root.xml',
        # Views
        'views/hr_indicadores_previsionales_view.xml',
        'views/hr_salary_rule_view.xml',
        'views/hr_contract_view.xml',
        'views/hr_employee.xml',
        'views/hr_payslip_view.xml',
        'views/hr_afp_view.xml',
        'views/hr_payslip_run_view.xml',
        'views/hr_holiday_views.xml',
        'views/hr_contribution_register_view.xml',
        # Datas
        'data/hr_salary_rule_category.xml',
        'data/hr_centros_costos.xml',
        'data/l10n_cl_hr_indicadores.xml',
        'data/l10n_cl_hr_isapre.xml',
        'data/l10n_cl_hr_afp.xml',
        'data/l10n_cl_hr_mutual.xml',
        'data/l10n_cl_hr_apv.xml',
        'data/hr_type_employee.xml',
        'data/resource_calendar_attendance.xml',
        'data/hr_holidays_status.xml',
        'data/hr_contract_type.xml',
        'data/l10n_cl_hr_ccaf.xml',
        'data/account_journal.xml',
        'data/res_partner.xml',
        'data/l10n_cl_hr_payroll_data.xml',
        # Wizards
        'wizard/wizard_export_csv_previred_views.xml',
        'wizard/hr_form_employee_book_views.xml',
        # Reports
        'report/report_hrsalarybymonth.xml',
        'report/report_payslip.xml',
        'report/hr_salary_books.xml',
    ],
    'demo': [
        # 'demo/l10n_cl_hr_payroll_demo.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
