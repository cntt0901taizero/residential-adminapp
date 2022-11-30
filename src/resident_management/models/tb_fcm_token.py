from builtins import print

from odoo import models, fields


class tb_fcm_token(models.Model):
    _name = 'tb_fcm_token'
    _description = 'Quản lý thiết bị'

    name = fields.Char(string='Thiết bị', required=True, copy=False)
    user_id = fields.Integer(string="Người dùng")





