from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    signup_token = fields.Char(copy=False, groups="resident_management.group_administration, resident_management.group_management, base.group_erp_manager")
    signup_type = fields.Char(string='Signup Token Type', copy=False, groups="resident_management.group_administration, resident_management.group_management, base.group_erp_manager")
    signup_expiration = fields.Datetime(copy=False, groups="resident_management.group_administration, resident_management.group_management, base.group_erp_manager")
