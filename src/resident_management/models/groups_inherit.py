from odoo import models, fields, api


class ResGroupsInherit(models.Model):
    _inherit = 'res.groups'

    perm_create_admin_user = fields.Boolean('Tạo tài khoản')
    perm_delete_admin_user = fields.Boolean('Xóa tài khoản')
    perm_write_admin_user = fields.Boolean('Sửa tài khoản')
    perm_read_admin_user = fields.Boolean('Xem tài khoản')
    perm_change_password_admin_user = fields.Boolean('Đổi mật khẩu')

    perm_create_resident_user = fields.Boolean('Tạo tài khoản')
    perm_delete_resident_user = fields.Boolean('Xóa tài khoản')
    perm_write_resident_user = fields.Boolean('Sửa tài khoản')
    perm_read_resident_user = fields.Boolean('Xem tài khoản')
    perm_change_password_resident_user = fields.Boolean('Đổi mật khẩu')

    def get_application_groups(self, domain):
        group_system = self.env.ref('base.group_system').id
        group_erp_manager = self.env.ref('base.group_erp_manager').id
        group_administration = self.env.ref('resident_management.group_administration').id
        group_management = self.env.ref('resident_management.group_management').id
        set_domain = ''
        if self.env.user.has_group('base.group_system') or self.env.user.has_group('base.group_erp_manager'):
            set_domain = domain + [('id', 'not in', (group_system, group_erp_manager))]
        else:
            set_domain = domain + [('id', 'not in', (group_system, group_erp_manager, group_administration, group_management))]
        return super(ResGroupsInherit, self).get_application_groups(set_domain)
