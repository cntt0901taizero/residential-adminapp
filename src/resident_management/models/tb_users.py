from odoo import models, fields, api


class tb_users(models.Model):
    _inherit = 'res.users'

    phone_number = fields.Char(string='Số điện thoại')
    push_notifications = fields.One2many('tb_push_notification', 'user_id', string='Push Notification', readonly=True)
    tb_users_blockhouse_res_groups_rel_ids = fields.One2many('tb_users_blockhouse_res_groups_rel', 'user_id')

    @api.model
    def create(self, vals):
        vals["password"] = "1"
        return super(tb_users, self).create(vals)

    def create_user_blockhouse_groups_rel(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Chọn nhóm quyền',
            'res_model': 'tb_users_blockhouse_res_groups_rel',
            'target': 'new',
            'view_id': self.env.ref('resident_management.view_tb_users_blockhouse_res_groups_rel_form').id,
            'view_mode': 'form',
            'context': {
                'default_user_id': self.id,
            },
        }
