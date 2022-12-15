from odoo import models, fields, api

class tb_users(models.Model):
    _inherit = 'res.users'

    phone_number = fields.Char(string='Số điện thoại')
    push_notifications = fields.One2many('tb_push_notification', 'user_id', string='Push Notification', readonly=True)
    tb_users_blochouse_res_groups_rel_id = fields.One2many('tb_users_blochouse_res_groups_rel', 'user_id')
    @api.model
    def create(self, vals):
        vals["password"] = "1"
        return super(tb_users, self).create(vals)
