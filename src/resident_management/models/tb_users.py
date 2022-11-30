from odoo import models, fields, api

class tb_users(models.Model):
    _inherit = 'res.users'

    phone_number = fields.Char(string='Số điện thoại')
    @api.model
    def create(self, vals):
        vals["password"] = "1"
        return super(tb_users, self).create(vals)
