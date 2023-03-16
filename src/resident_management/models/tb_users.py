from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessDenied
from odoo.http import request

from odoo.addons.resident_management.enum import STATUS_TYPES, USER_GROUP_CODE
from odoo.addons.resident_management.common import is_valid_email, is_valid_phone

str_bql = USER_GROUP_CODE[2][0]
str_bqt = USER_GROUP_CODE[3][0]


class tb_users(models.Model):
    _inherit = 'res.users'

    row_number = fields.Integer(string='STT', compute='_compute_row_number', store=False)
    citizen_identification = fields.Char(string='CMND / CCCD')
    date_of_birth = fields.Date(string='Ngày sinh', copy=False)
    gender = fields.Selection([
        ('Male', 'Nam'), ('Female', 'Nữ'), ('Other', 'Khác'),
    ], default='Male', string="Giới tính")
    user_type = fields.Selection([
        ('ADMIN', 'Quản trị'), ('RESIDENT', 'Cư dân'), ('OTHER', 'Other'),
    ], default='OTHER', string="Loại tài khoản")
    status = fields.Selection(string='Trạng thái', selection=STATUS_TYPES, default=STATUS_TYPES[0][0])
    mobile_change_password = fields.Boolean(string='Đổi password trên smartphone', default=False)
    push_notifications = fields.One2many('tb_push_notification', 'user_id', string='Push Notification', readonly=True)
    tb_users_blockhouse_res_groups_rel_ids = fields.One2many('tb_users_blockhouse_res_groups_rel', 'user_id',
                                                             string="Quan hệ phân quyền")

    _sql_constraints = [
        ('citizen_identification', 'unique(citizen_identification)', 'Số định danh cá nhân không được trùng lặp')
    ]

    @api.depends('create_date')
    def _compute_row_number(self):
        index_row = 0
        for record in self:
            index_row += 1
            record.row_number = index_row

    @api.model
    def check_perm_user(self, permission_name):
        check = False
        user = request.env.user
        if user and (user.id == 1 or user.id == 2):
            check = True
        else:
            for item in user.tb_users_blockhouse_res_groups_rel_ids:
                gid = item.group_id.id
                group = request.env["res.groups"].sudo().search([('id', '=', gid)], limit=1)
                if group[permission_name]:
                    check = True
                    break
        return check

    def set_status_active(self):
        per_name = 'perm_approve_resident_user'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            for item in self:
                item.active = True
                item.status = STATUS_TYPES[1][0]
                item.mobile_change_password = False
                users_with_email = item.filtered('email')
                users_with_email.with_context(create_user=True, install_mode=False).action_reset_password()
            return True
        raise ValidationError(error_messenger)

    def set_status_reject(self):
        per_name = 'perm_approve_resident_user'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            for item in self:
                item.active = False
                item.status = STATUS_TYPES[2][0]
            return True
        raise ValidationError(error_messenger)

    def set_status_pending(self):
        per_name = 'perm_approve_resident_user'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            for item in self:
                item.active = False
                item.status = STATUS_TYPES[0][0]
            return True
        raise ValidationError(error_messenger)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        user = request.env.user
        bqt_bh_id = []  # ban quan tri - blockhouse - id
        bqt_bd_id = []  # ban quan tri - building - id
        bql_bh_id = []  # ban quan ly - blockhouse - id
        bql_bd_id = []  # ban quan ly - building - id
        if user and user.id != 1 and user.id != 2:
            for item in user.tb_users_blockhouse_res_groups_rel_ids:
                if item.group_id.name and str_bqt in item.user_group_code:
                    bqt_bh_id.append(int(item.blockhouse_id.id))
                    bqt_bd_id.append(int(item.building_id.id))
                if item.group_id.name and str_bql in item.user_group_code:
                    bql_bh_id.append(int(item.blockhouse_id.id))
                    bql_bd_id.append(int(item.building_id.id))
            domain.append(('tb_users_blockhouse_res_groups_rel_ids.blockhouse_id', 'in',
                           list(set(bqt_bh_id + bql_bh_id))))
            domain.append(('tb_users_blockhouse_res_groups_rel_ids.building_id', 'in',
                           list(set(bqt_bd_id + bql_bd_id))))
        res = super(tb_users, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                               orderby=orderby, lazy=lazy)
        return res

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=10, order=None):
        user = request.env.user
        bqt_bh_id = []  # ban quan tri - blockhouse - id
        bqt_bd_id = []  # ban quan tri - building - id
        bql_bh_id = []  # ban quan ly - blockhouse - id
        bql_bd_id = []  # ban quan ly - building - id
        if user and user.id != 1 and user.id != 2:
            for item in user.tb_users_blockhouse_res_groups_rel_ids:
                if item.group_id.name and str_bqt in item.user_group_code:
                    bqt_bh_id.append(int(item.blockhouse_id.id))
                    bqt_bd_id.append(int(item.building_id.id))
                if item.group_id.name and str_bql in item.user_group_code:
                    bql_bh_id.append(int(item.blockhouse_id.id))
                    bql_bd_id.append(int(item.building_id.id))
            domain.append(('tb_users_blockhouse_res_groups_rel_ids.blockhouse_id', 'in',
                           list(set(bqt_bh_id + bql_bh_id))))
            domain.append(('tb_users_blockhouse_res_groups_rel_ids.building_id', 'in',
                           list(set(bqt_bd_id + bql_bd_id))))
        res = super(tb_users, self).search_read(domain, fields, offset, limit, order)
        return res

    @api.model
    def create(self, vals):
        default_user_type = self._context['default_user_type']
        per_name = 'perm_create_resident_user'
        error_messenger = 'Bạn không có quyền tạo tài khoản cư dân.'
        if default_user_type == 'ADMIN':
            per_name = 'perm_create_admin_user'
            error_messenger = 'Bạn không có quyền tạo tài khoản quản trị.'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            password = vals["password"]
            if password and (len(password) < 7 or len(password) > 35):
                raise ValidationError("Độ dài mật khẩu phải từ 8 đến 35 kí tự!")
                return
            email = vals["email"]
            if email and not is_valid_email(str(email)):
                raise ValidationError("Email chưa đúng định dạng.")
                return
            phone = vals["phone"]
            if phone and not is_valid_phone(str(phone)):
                raise ValidationError("Điện thoại chưa đúng định dạng.")
                return
            if default_user_type != 'ADMIN':
                # self.env.context['install_mode'] = True
                vals["active"] = False
            self.clear_caches()
            return super(tb_users, self).create(vals)
        raise ValidationError(error_messenger)

    @api.model
    def write(self, records, vals):
        user_data = self.env['res.users'].browse(records[0])
        per_name = 'perm_write_resident_user'
        error_messenger = 'Bạn không có quyền cập nhật tài khoản cư dân.'
        if user_data.user_type == 'ADMIN':
            per_name = 'perm_write_admin_user'
            error_messenger = 'Bạn không có quyền cập nhật tài khoản quản trị.'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            password = vals.get("password")
            if password and (len(password) < 7 or len(password) > 35):
                raise ValidationError("Độ dài mật khẩu phải từ 8 đến 35 kí tự!")
                return
            email = vals.get("email")
            if email and not is_valid_email(str(email)):
                raise ValidationError("Email chưa đúng định dạng.")
                return
            phone = vals.get("phone")
            if phone and not is_valid_phone(str(phone)):
                raise ValidationError("Điện thoại chưa đúng định dạng.")
                return
            res = super(tb_users, user_data).write(vals)
            self.clear_caches()
            return res
        raise ValidationError(error_messenger)

    def create_user_blockhouse_groups_rel(self):
        view_id = ''
        name = ''
        context = {
            'default_user_id': self.id,
        }
        if self.user_type != 'RESIDENT':
            name = 'Phân quyền quản lý quản trị'
            view_id = self.env.ref('resident_management.view_tb_users_blockhouse_res_groups_rel_form').id
        else:
            name = 'Phân quyền căn hộ cư dân'
            context['default_group_id'] = self.env['res.groups'].search([('name', 'like', '%[CD]%')]).id
            view_id = self.env.ref('resident_management.view_tb_users_blockhouse_res_groups_rel_form_resident').id
        return {
            'type': 'ir.actions.act_window',
            'name': name,
            'res_model': 'tb_users_blockhouse_res_groups_rel',
            'target': 'new',
            'view_id': view_id,
            'view_mode': 'form',
            'context': context,
        }

    def open_edit_admin_form(self):
        per_name = 'perm_write_admin_user'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            form_id = self.env.ref('resident_management.view_admin_users_form_inherit')
            return {
                'type': 'ir.actions.act_window',
                'name': 'Cập nhật người dùng quản lý quản trị',
                'res_model': 'res.users',
                'res_id': self.id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': form_id.id,
                'context': {'form_view_initial_mode': 'edit'},
                # if you want to open the form in edit mode direclty
                'target': 'current',
            }
        raise ValidationError(error_messenger)

    def open_edit_resident_form(self):
        per_name = 'perm_write_resident_user'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            form_id = self.env.ref('resident_management.view_resident_users_form_inherit')
            return {
                'type': 'ir.actions.act_window',
                'name': 'Cập nhật người dùng cư dân',
                'res_model': 'res.users',
                'res_id': self.id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': form_id.id,
                'context': {'form_view_initial_mode': 'edit'},
                # if you want to open the form in edit mode direclty
                'target': 'current',
            }
        raise ValidationError(error_messenger)

    def open_edit_resident_approve_form(self):
        per_name = 'perm_write_resident_user'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            form_id = self.env.ref('resident_management.view_resident_users_approve_form_inherit')
            return {
                'type': 'ir.actions.act_window',
                'name': 'Cập nhật và phê duyệt người dùng cư dân',
                'res_model': 'res.users',
                'res_id': self.id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': form_id.id,
                'context': {'form_view_initial_mode': 'edit'},
                # if you want to open the form in edit mode direclty
                'target': 'current',
            }
        raise ValidationError(error_messenger)

    def confirm_admin_delete(self):
        per_name = 'perm_delete_admin_user'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
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
        raise ValidationError(error_messenger)

    def confirm_resident_delete(self):
        per_name = 'perm_delete_resident_user'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
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
        raise ValidationError(error_messenger)

    def del_record(self):
        for record in self:
            record.unlink()
            pass
