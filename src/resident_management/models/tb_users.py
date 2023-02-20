from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessDenied
from odoo.http import request

from odoo.addons.resident_management.models.tb_users_blockhouse_res_groups_rel import USER_GROUP_CODE

str_bql = USER_GROUP_CODE[2][0]
str_bqt = USER_GROUP_CODE[3][0]


class tb_users(models.Model):
    _inherit = 'res.users'

    citizen_identification = fields.Char(string='CMND / CCCD')
    date_of_birth = fields.Date(string='Ngày sinh', copy=False)
    gender = fields.Selection([
        ('Male', 'Nam'), ('Female', 'Nữ'), ('Other', 'Khác'),
    ], default='Male', string="Giới tính", )
    user_type = fields.Selection([
        ('ADMIN', 'Quản trị'), ('RESIDENT', 'Cư dân'), ('OTHER', 'Other'),
    ], default='OTHER', string="Loại tài khoản", )
    push_notifications = fields.One2many('tb_push_notification', 'user_id', string='Push Notification', readonly=True)
    tb_users_blockhouse_res_groups_rel_ids = fields.One2many('tb_users_blockhouse_res_groups_rel', 'user_id',
                                                             string="Quan hệ phân quyền")

    _sql_constraints = [
        ('citizen_identification', 'unique(citizen_identification)', 'Số định danh cá nhân không được trùng lặp')
    ]

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
        # vals["password"] = "1"
        return super(tb_users, self).create(vals)

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

    def open_edit_form(self):
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

    def confirm_delete(self):
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
