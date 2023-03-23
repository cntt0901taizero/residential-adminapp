from builtins import print

from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo.addons.resident_management.enum import STATUS_TYPES


class tb_banner(models.Model):
    _name = 'tb_banner'
    _description = 'Quảng cáo'

    name = fields.Char(string='Tiêu đề', required=True, copy=False)
    banner_description = fields.Text(string='Nội dung quảng cáo', copy=False, required=True)
    image = fields.Image(string="Ảnh", required=True)
    link = fields.Char(string='Link', size=500, copy=False, required=True)
    sort = fields.Integer(string='Thứ tự', copy=False)
    status = fields.Selection(string='Trạng thái', selection=STATUS_TYPES, default=STATUS_TYPES[0][0])
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="dự án", ondelete="cascade",
                                    domain="[('is_active', '=', True)]")

    def write(self, values):
        per_name = 'perm_approve_advertisement'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            values['status'] = 'ACTIVE'
        else:
            values['status'] = 'PENDING'
        return super(tb_banner, self).write(values)

    def set_status_active(self):
        self.write({'status': 'ACTIVE'})

    def set_status_reject(self):
        self.write({'status': 'REJECT'})

    def set_status_draft(self):
        self.write({'status': 'PENDING'})

    def open_edit_form(self):
        form_id = self.env.ref('apartment_service_support.view_tb_banner_form')
        per_name = 'perm_write_advertisement'
        error_messenger = 'Bạn không có quyền chỉnh sửa quảng cáo.'
        can_do = self.check_permission(per_name, raise_exception=False)
        if not can_do:
            raise ValidationError(error_messenger)
        self.check_access_rights('write')
        # then open the form
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cập nhật quảng cáo',
            'res_model': 'tb_banner',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_id.id,
            'context': {'form_view_initial_mode': 'edit'},
            # if you want to open the form in edit mode direclty
            'target': 'current',
        }

    def confirm_delete(self):
        per_name = 'perm_delete_advertisement'
        error_messenger = 'Bạn không có quyền xóa quảng cáo.'
        can_do = self.check_permission(per_name, raise_exception=False)
        if not can_do:
            raise ValidationError(error_messenger)
        message = """Bạn có chắc muốn xóa bản tin này?"""
        value = self.env['dialog.box.confirm'].sudo().create({'message': message})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Xóa bản tin',
            'res_model': 'dialog.box.confirm',

            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_id': value.id
        }
