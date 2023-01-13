from odoo import models, fields, api
from odoo.exceptions import ValidationError


class tb_users(models.Model):
    _inherit = 'res.users'

    phone_number = fields.Char(string='Số điện thoại')
    push_notifications = fields.One2many('tb_push_notification', 'user_id', string='Push Notification', readonly=True)
    tb_users_blockhouse_res_groups_rel_ids = fields.One2many('tb_users_blockhouse_res_groups_rel', 'user_id')
    # display_building = fields.Char('Tòa nhà', related='tb_users_blockhouse_res_groups_rel_ids.building_id.name')
    # display_apartment = fields.Char('Căn hộ', related='tb_users_blockhouse_res_groups_rel_ids.building_house_id.name')

    @api.model
    def create(self, vals):
        vals["password"] = "1"
        return super(tb_users, self).create(vals)

    def create_user_blockhouse_groups_rel(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Thêm nhóm quyền',
            'res_model': 'tb_users_blockhouse_res_groups_rel',
            'target': 'new',
            'view_id': self.env.ref('resident_management.view_tb_users_blockhouse_res_groups_rel_form').id,
            'view_mode': 'form',
            'context': {
                'default_user_id': self.id,
            },
        }

    def open_edit_form_user(self):
        # first you need to get the id of your record
        # you didn't specify what you want to edit exactly
        # rec_id = self.env.context.get('active_id').exists()
        # then if you have more than one form view then specify the form id
        canwrite = self.check_access_rights('write', raise_exception=False)
        if not canwrite:
            raise ValidationError('Bạn không có quyền chỉnh sửa thông tin tài khoản.')
        form_id = self.env.ref('base.view_users_form')

        # then open the form
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cập nhật người dùng',
            'res_model': 'res.users',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_id.id,
            'context': {'form_view_initial_mode': 'edit'},
            # if you want to open the form in edit mode direclty
            'target': 'current',
        }

    def confirm_delete_user(self):
        candelete = self.check_access_rights('unlink', raise_exception=False)
        if not candelete:
            raise ValidationError('Bạn không có quyền xóa thông tin tài khoản.')
        message = """Bạn có chắc muốn xóa tài khoản này?"""
        value = self.env['dialog.box.confirm'].sudo().create({'message': message})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Xóa tài khoản',
            'res_model': 'dialog.box.confirm',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_id': value.id
        }

    def del_record(self):
        for record in self:
            record.unlink()
            pass