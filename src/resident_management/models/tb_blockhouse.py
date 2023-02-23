from odoo import models, fields, api
from odoo.http import request
from datetime import date
from odoo.exceptions import ValidationError
import random

from odoo.addons.resident_management.models.tb_users_blockhouse_res_groups_rel import USER_GROUP_CODE
str_bql = USER_GROUP_CODE[2][0]
str_bqt = USER_GROUP_CODE[3][0]


class tb_blockhouse(models.Model):
    _name = 'tb_blockhouse'
    _description = 'Dự án'

    row_number = fields.Integer(string='STT', compute='_compute_row_number', store=False)
    name = fields.Char(string='Tên dự án', size=200, required=True, copy=False)
    code = fields.Char(string='Mã', size=50, copy=False, readonly=True)
    investor_name = fields.Char(string='Chủ đầu tư', size=500, copy=False)
    address = fields.Char(string='Địa chỉ', size=500, copy=False)
    image = fields.Image(string='Ảnh', copy=False)
    website = fields.Char(string='Website', size=200, copy=False)
    phone = fields.Char(string='Điện thoại', size=50, copy=False)
    location_link = fields.Char(string='Link vị trí', size=500, copy=False)
    is_active = fields.Boolean(string='Có hiệu lực', default=True)

    building_ids = fields.One2many(comodel_name='tb_building', inverse_name='blockhouse_id', string="Khu / Tòa nhà")

    _sql_constraints = [
        ('name', 'unique(name)', 'Tên dự án không được trùng lặp'),
        ('code', 'unique(code)', 'Mã dự án không được trùng lặp')
    ]

    @api.depends('create_date')
    def _compute_row_number(self):
        index_row = 0
        for record in self:
            index_row += 1
            record.row_number = index_row

    def set_status_active(self):
        self.is_active = True

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        user = request.env.user
        if user and user.id != 1 and user.id != 2:
            bh_ids = []
            for item in user.tb_users_blockhouse_res_groups_rel_ids:
                if item.group_id.name and (str_bql in item.user_group_code or str_bqt in item.user_group_code):
                    bh_ids.append(int(item.blockhouse_id.id))
            domain.append(('id', 'in', bh_ids))
        res = super(tb_blockhouse, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                    orderby=orderby, lazy=lazy)
        return res

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=10, order=None):
        user = request.env.user
        if user and user.id != 1 and user.id != 2:
            bh_ids = []
            for item in user.tb_users_blockhouse_res_groups_rel_ids:
                if item.group_id.name and (str_bql in item.user_group_code or str_bqt in item.user_group_code):
                    bh_ids.append(int(item.blockhouse_id.id))
            domain.append(('id', 'in', bh_ids))

        res = super(tb_blockhouse, self).search_read(domain, fields, offset, limit, order)
        return res

    @api.model
    def create(self, vals):
        per_name = 'perm_create_block_house'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            today = date.today()
            d = today.strftime('%d%m%y')
            vals["code"] = 'BH' + str(d) + str(random.randint(1000, 9999))
            return super(tb_blockhouse, self).create(vals)
        raise ValidationError(error_messenger)

    def create_building(self):
        per_name = 'perm_create_building'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Tạo mới khu / tòa nhà',
                'res_model': 'tb_building',
                'target': 'new',
                'view_id': self.env.ref('apartment_project.view_tb_building_form').id,
                'view_mode': 'form',
                'context': {
                    'default_blockhouse_id': self.id,
                },
            }
        raise ValidationError(error_messenger)

    def create_building_house(self):
        per_name = 'perm_create_apartment'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Tạo mới Căn hộ',
                'res_model': 'tb_building_house',
                'target': 'new',
                'view_id': self.env.ref('apartment_project.view_tb_building_house_form').id,
                'view_mode': 'form',
                'context': {
                    'default_blockhouse_id': self.id,
                },
            }
        raise ValidationError(error_messenger)

    def create_apartment_utilities(self):
        per_name = 'perm_create_utilities'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Tạo mới tiện ích',
                'res_model': 'tb_apartment_utilities',
                'target': 'new',
                'view_id': self.env.ref('apartment_service_support.view_tb_apartment_utilities_form').id,
                'view_mode': 'form',
                'context': {
                    'default_blockhouse_id': self.id,
                },
            }
        raise ValidationError(error_messenger)

    def open_edit_form(self):
        per_name = 'perm_write_block_house'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Sửa dự án ' + self.name,
                'res_model': 'tb_blockhouse',
                'res_id': self.id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('apartment_project.view_tb_blockhouse_form').id,
                'context': {'form_view_initial_mode': 'edit'},
                'target': 'current',
            }
        raise ValidationError(error_messenger)

    def confirm_delete(self):
        per_name = 'perm_delete_block_house'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            message = """Bạn có chắc muốn xóa bản ghi này?"""
            value = self.env['dialog.box.confirm'].sudo().create({'message': message})
            return {
                'type': 'ir.actions.act_window',
                'name': 'Xóa bản ghi',
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


