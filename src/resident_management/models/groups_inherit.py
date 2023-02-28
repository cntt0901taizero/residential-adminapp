from odoo import models, fields, api
from odoo.exceptions import ValidationError


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
    perm_read_resident_user = fields.Boolean('Xem tài khoản', default=True)
    perm_approve_resident_user = fields.Boolean('Phê duyệt tài khoản')
    perm_change_password_resident_user = fields.Boolean('Đổi mật khẩu')

    perm_create_block_house = fields.Boolean('Tạo dự án')
    perm_delete_block_house = fields.Boolean('Xóa dự án')
    perm_write_block_house = fields.Boolean('Sửa dự án')
    perm_read_block_house = fields.Boolean('Xem dự án', default=True)

    perm_create_building = fields.Boolean('Tạo tòa nhà')
    perm_delete_building = fields.Boolean('Xóa tòa nhà')
    perm_write_building = fields.Boolean('Sửa tòa nhà')
    perm_read_building = fields.Boolean('Xem tòa nhà', default=True)

    perm_create_floor = fields.Boolean('Tạo tầng')
    perm_delete_floor = fields.Boolean('Xóa tầng')
    perm_write_floor = fields.Boolean('Sửa tầng')
    perm_read_floor = fields.Boolean('Xem tầng', default=True)

    perm_create_apartment = fields.Boolean('Tạo căn hộ')
    perm_delete_apartment = fields.Boolean('Xóa căn hộ')
    perm_write_apartment = fields.Boolean('Sửa căn hộ')
    perm_read_apartment = fields.Boolean('Xem căn hộ', default=True)

    perm_create_news = fields.Boolean('Tạo tin tức')
    perm_delete_news = fields.Boolean('Xóa tin tức')
    perm_write_news = fields.Boolean('Sửa tin tức')
    perm_approve_news = fields.Boolean('Phê duyệt tin tức')
    perm_read_news = fields.Boolean('Xem tin tức', default=True)

    perm_create_advertisement = fields.Boolean('Tạo quảng cáo')
    perm_delete_advertisement = fields.Boolean('Xóa quảng cáo')
    perm_write_advertisement = fields.Boolean('Sửa quảng cáo')
    perm_approve_advertisement = fields.Boolean('Phê duyệt quảng cáo')
    perm_read_advertisement = fields.Boolean('Xem quảng cáo', default=True)

    perm_create_notification = fields.Boolean('Tạo thông báo')
    perm_delete_notification = fields.Boolean('Xóa thông báo')
    perm_write_notification = fields.Boolean('Sửa thông báo')
    perm_approve_notification = fields.Boolean('Phê duyệt thông báo')
    perm_read_notification = fields.Boolean('Xem thông báo', default=True)

    perm_create_handbook = fields.Boolean('Tạo cẩm nang')
    perm_delete_handbook = fields.Boolean('Xóa cẩm nang')
    perm_write_handbook = fields.Boolean('Sửa cẩm nang')
    perm_approve_handbook = fields.Boolean('Phê duyệt cẩm nang')
    perm_read_handbook = fields.Boolean('Xem cẩm nang', default=True)

    perm_create_utilities = fields.Boolean('Tạo tiện ích')
    perm_delete_utilities = fields.Boolean('Xóa tiện ích')
    perm_write_utilities = fields.Boolean('Sửa tiện ích')
    perm_approve_utilities = fields.Boolean('Phê duyệt tiện ích')
    perm_read_utilities = fields.Boolean('Xem tiện ích', default=True)

    perm_create_access_card = fields.Boolean('Tạo thẻ ra vào')
    perm_delete_access_card = fields.Boolean('Xóa thẻ ra vào')
    perm_write_access_card = fields.Boolean('Sửa thẻ ra vào')
    perm_approve_access_card = fields.Boolean('Phê duyệt thẻ ra vào')
    perm_read_access_card = fields.Boolean('Xem thẻ ra vào', default=True)

    perm_create_vehicle = fields.Boolean('Tạo thẻ xe')
    perm_delete_vehicle = fields.Boolean('Xóa thẻ xe')
    perm_write_vehicle = fields.Boolean('Sửa thẻ xe')
    perm_approve_vehicle = fields.Boolean('Phê duyệt thẻ xe')
    perm_read_vehicle = fields.Boolean('Xem thẻ xe', default=True)

    perm_create_delivery = fields.Boolean('Tạo ĐK chuyển đồ')
    perm_delete_delivery = fields.Boolean('Xóa ĐK chuyển đồ')
    perm_write_delivery = fields.Boolean('Sửa ĐK chuyển đồ')
    perm_approve_delivery = fields.Boolean('Phê duyệt ĐK chuyển đồ')
    perm_read_delivery = fields.Boolean('Xem ĐK chuyển đồ', default=True)

    perm_create_complain = fields.Boolean('Tạo khiếu nại')
    perm_delete_complain = fields.Boolean('Xóa khiếu nại')
    perm_write_complain = fields.Boolean('Sửa khiếu nại')
    perm_approve_complain = fields.Boolean('Phê duyệt khiếu nại')
    perm_read_complain = fields.Boolean('Xem khiếu nại', default=True)

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

    def open_edit_form(self):
        canwrite = self.check_access_rights('write', raise_exception=False)
        if not canwrite:
            raise ValidationError('Bạn không có quyền chỉnh sửa thông tin.')
        form_id = self.env.ref('resident_management.view_group_form_inherit')

        return {
            'type': 'ir.actions.act_window',
            'name': 'Cập nhật nhóm người dùng',
            'res_model': 'res.groups',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_id.id,
            'context': {'form_view_initial_mode': 'edit'},
            'target': 'current',
        }

    def confirm_delete(self):
        candelete = self.check_access_rights('unlink', raise_exception=False)
        if not candelete:
            raise ValidationError('Bạn không có quyền xóa thông tin tài khoản.')
        message = """Bạn có chắc muốn xóa tài khoản này?"""
        value = self.env['dialog.box.confirm'].sudo().create({'message': message})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Xóa nhóm quyền',
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
